import logging
from datetime import datetime

from .celery import app
from config import config as app_config
from cryptolib.model import (
    CurrencyPairConfigModel,
    UserModel,
    CurrencyPairModel,
    BalanceModel,
    PortfolioModel,
    PortfolioHistoryModel,
    BalanceHistoryModel,
)
from cryptolib.model import OrderModel
from cryptolib.schema import CurrencyPairConfigSchema
from cryptolib.enums import Signal, ExchangeType, OrderStatus
from service import SignalService, DataService, ExchangeService, TraderService

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

ENGINE = create_engine(
    app_config.SQLALCHEMY_DATABASE_URI, echo=False, pool_size=20, max_overflow=0
)


@app.task
def do_scheduled_autotrade():
    rows = []
    with Session(ENGINE) as session:
        # Fetch the currency pairs that are enabled for autotrade
        rows: list[CurrencyPairConfigModel] = DataService().get_active_bots(session)

        # Generate signals for each currency pair
        for row in rows:
            signal = row.signal
            interval = row.interval

            # Check if the last trade was made within the interval
            interval_seconds = DataService().get_interval_seconds(interval)
            if (
                datetime.now() - signal.last_trade_time
            ).total_seconds() < interval_seconds:
                logging.info("Not enough time has passed since last trade")
                continue

            do_buy_sell.delay(CurrencyPairConfigSchema().dump(row))


@app.task
def do_scheduled_update_balance():
    users = []
    with Session(ENGINE) as session:
        # Fetch the currency pairs that are enabled for autotrade
        users: list[UserModel] = DataService().get_users(session)

        # For each exchange we need to retrieve the balance
        for user in users:
            # only update the balance if the user has an active bot
            # TODO: convert this into a boolean check
            active_bots = False
            for bot in user.currency_pair_configs:
                if bot.is_active:
                    active_bots = True
                    break

            if not active_bots:
                continue

            portfolio_id = user.portfolio.id
            exchanges = {}
            for api in user.api_keys:
                exchange_type = api.exchange.value
                api_key_pair = {"api_key": api.api_key, "api_secret": api.api_secret}
                exchanges[exchange_type] = api_key_pair

            # Reset balances
            for balance in user.portfolio.balances:
                balance.free = 0.0
                balance.locked = 0.0
                balance.total = 0.0
            session.commit()

            update_balance.delay(user.id, portfolio_id, exchanges)
            update_portfolio.delay(user.id)


@app.task
def update_portfolio(user_id):
    with Session(ENGINE) as session:
        user: UserModel = DataService().get_user(session, user_id)

        bots: list[CurrencyPairConfigModel] = DataService().get_bots(session, user_id)
        portfolio: PortfolioModel = user.portfolio

        total_earnings = 0
        for bot in bots:
            total_earnings += bot.earnings

        # Update the portfolio history
        portfolio_history = PortfolioHistoryModel(
            portfolio_id=portfolio.id,
            total_earnings=total_earnings,
        )

        session.add(portfolio_history)

        # Update the total earnings
        portfolio.total_earnings = total_earnings
        session.commit()


@app.task
def update_balance(user_id, portfolio_id, exchanges):
    with Session(ENGINE) as session:
        # Gets the real balance from the exchanges and updates the database
        for exchange_type, api_key_pair in exchanges.items():
            exchange = ExchangeService().get_exchange(exchange_type, **api_key_pair)
            balances = exchange.get_balance()
            for balance in balances:
                asset = balance.get("asset")
                free = balance.get("free")
                locked = balance.get("locked")
                DataService().update_balance(
                    session,
                    portfolio_id,
                    asset,
                    free,
                    locked,
                    ExchangeType(exchange_type),
                )

        # Iterate through active bots and update the balance
        bots: list[CurrencyPairConfigModel] = DataService().get_bots(session, user_id)
        for bot in bots:
            pair: CurrencyPairModel = DataService().get_currency_pair(
                session, bot.currency_pair
            )
            if not pair:
                logging.warning(
                    f"Currency pair {bot.currency_pair} does not exist. Skipping."
                )
                continue

            asset = pair.symbol
            currency = pair.pair

            # Free up locked balance if the bot has been decommissioned
            if bot.is_decommissioned:
                asset_balance = DataService().get_balance(session, portfolio_id, asset)
                currency_balance = DataService().get_balance(
                    session, portfolio_id, currency
                )
                asset_balance.free += bot.asset_free + bot.asset_locked
                asset_balance.locked -= bot.asset_free + bot.asset_locked
                currency_balance.free += bot.currency_free + bot.currency_locked
                currency_balance.locked -= bot.currency_free + bot.currency_locked
                bot.asset_free = 0
                bot.asset_locked = 0
                bot.currency_free = 0
                bot.currency_locked = 0

            # Only update the balance if the bot is simulated since
            # the balance of the bot won't be reflected in the exchange
            if bot.is_simulated:
                asset_balance = bot.asset_free + bot.asset_locked
                currency_balance = bot.currency_free + bot.currency_locked
                DataService().update_balance(
                    session, portfolio_id, asset, 0, asset_balance, bot.exchange
                )
                DataService().update_balance(
                    session, portfolio_id, currency, 0, currency_balance, bot.exchange
                )

        session.flush()

        # Update the balance history
        for balance in (
            session.query(BalanceModel).filter_by(portfolio_id=portfolio_id).all()
        ):
            balance_history = BalanceHistoryModel(
                balance_id=balance.id,
                asset=balance.asset,
                free=balance.free,
                locked=balance.locked,
                total=balance.total,
            )
            session.add(balance_history)

        session.commit()


@app.task
def do_buy_sell(currency_pair_config: CurrencyPairConfigModel):
    with Session(ENGINE) as session:
        config = CurrencyPairConfigSchema().load(currency_pair_config, session=session)
        user_id = config.user_id
        exchange_type = config.exchange.value

        # Fetch api keys
        api_key_pair = DataService().get_api_key(session, user_id, exchange_type)
        if len(api_key_pair) == 0:
            logging.warning(f"No api key found for user_id: {user_id}")
            return

        # Fetch the exchange service
        exchange = ExchangeService().get_exchange(exchange_type, **api_key_pair)

        # Generate the signal
        signal: Signal = SignalService(exchange, currency_pair_config).generate_signal()
        if signal is None:
            logging.warning(
                f"Failed to generate signal for user_id {user_id} with strategy {config.strategy}"
            )
            return

        logging.info(
            f"Generated signal {signal.name} for currency pair: {config.currency_pair}."
        )

        # Update the autotrade table with the signal
        update_signal.delay(currency_pair_config.get("signal").get("id"), signal.name)

        # Trade if the signal is not HOLD
        if signal == Signal.HOLD:
            return

        # Create the order
        trader = TraderService(exchange)
        order: OrderModel = trader.create_order(session, signal, config)

        # Invalid balance and so failed to create order
        if order is None:
            return

        # If the order is filled, update the order and the balance
        if order.status == OrderStatus.FILLED:
            trader.update_order(session, order, config)

        session.commit()


@app.task
def update_signal(id: int, signal: str):
    with Session(ENGINE) as session:
        DataService().update_signal(session, id, signal)
        if signal != Signal.HOLD.name:
            DataService().update_last_trade_time(session, id, datetime.now())
        session.commit()
