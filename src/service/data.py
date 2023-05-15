from cryptolib.model import (
    CurrencyPairConfigModel,
    SignalModel,
    OrderModel,
    ApiKeyModel,
    UserModel,
    PortfolioModel,
    PortfolioHistoryModel,
    BalanceModel,
    BalanceHistoryModel,
    CurrencyPairModel,
)
from cryptolib.schema import ApiKeySchema
from cryptolib.utils import interval_to_seconds
from cryptolib.enums import Interval, OrderStatus, Signal


class DataService:

    def get_interval_seconds(self, interval: Interval) -> int:
        """Get the interval in seconds

        :param interval: The interval

        :return: The interval in seconds

        :rtype: int
        """
        return interval_to_seconds(interval)

    def get_api_key(self, session, user_id, exchange_type) -> dict:
        """Get the API key for the user
        #IMPORTANT: This is a temporary solution. It should be replaced with a proper authentication mechanism
        in the future. Storing the api secret in the database is not a good idea. So will use a
        single API key for all users for now.

        :param user_id: The user ID
        :param exchange: The exchange
        :param session: The database session

        :return: The API key

        :rtype: dict
        """
        data: ApiKeyModel = (
            session.query(ApiKeyModel)
            .filter_by(user_id=user_id, exchange=exchange_type)
            .first()
        )
        return ApiKeySchema().dump(data)

    def get_user(self, session, user_id) -> list[UserModel]:
        """Get the users

        :param session: The database session

        :return: The users

        :rtype: list
        """
        return session.query(UserModel).filter_by(id=user_id).first()

    def get_users(self, session) -> list[UserModel]:
        """Get the users

        :param session: The database session

        :return: The users

        :rtype: list
        """
        return session.query(UserModel).order_by(UserModel.id).all()

    def get_bots(self, session, user_id=None) -> list[CurrencyPairConfigModel]:
        """Get the currency pairs that are enabled for autotrade

        :param session: The database session

        :return: The currency pairs that are enabled for autotrade

        :rtype: list
        """

        if user_id:
            return (
                session.query(CurrencyPairConfigModel).filter_by(user_id=user_id).all()
            )

        return session.query(CurrencyPairConfigModel).all()

    def get_active_bots(self, session, user_id=None) -> list[CurrencyPairConfigModel]:
        """Get the currency pairs that are enabled for autotrade

        :param session: The database session

        :return: The currency pairs that are enabled for autotrade

        :rtype: list
        """

        if user_id:
            return (
                session.query(CurrencyPairConfigModel)
                .filter_by(user_id=user_id, is_active=True)
                .all()
            )

        return session.query(CurrencyPairConfigModel).filter_by(is_active=True).all()

    def get_currency_pair(self, session, currency_pair) -> str:
        """Get the asset from the currency pair

        :param session: The database session
        :param currency_pair: The currency pair

        :return: The asset

        :rtype: str
        """
        return (
            session.query(CurrencyPairModel)
            .filter_by(currency_pair=currency_pair)
            .first()
        )

    def get_currency_pair_config(self, session, id) -> CurrencyPairConfigModel:
        """Get the user's autotrade config for a currency pair

        :param session: The database session
        :param id: The currency pair config id

        :return: The user's autotrade config for the currency pair

        :rtype: dict
        """
        return session.query(CurrencyPairConfigModel).filter_by(id=id).first()

    def get_portfolio(self, session, user_id) -> PortfolioModel:
        """Get the user's portfolio

        :param session: The database session

        :return: The user's portfolio

        :rtype: dict
        """
        return session.query(PortfolioModel).filter_by(user_id=user_id).first()

    def get_portfolio_history(
        self, session, portfolio_id
    ) -> list[PortfolioHistoryModel]:
        """Get the user's portfolio history

        :param session: The database session
        :param portfolio_id: The portfolio id

        :return: The user's portfolio history

        :rtype: dict
        """
        return (
            session.query(PortfolioHistoryModel)
            .filter_by(portfolio_id=portfolio_id)
            .all()
        )

    def get_portfolios(self, session) -> list[PortfolioModel]:
        """Get the user's portfolio

        :param session: The database session

        :return: The user's portfolio

        :rtype: dict
        """
        return session.query(PortfolioModel).order_by(PortfolioModel.id).all()

    def get_balance(self, session, portfolio_id, asset) -> BalanceModel:
        """Get the balance of an asset for a portfolio

        :param session: The database session
        :param portfolio_id: The portfolio id
        :param asset: The asset

        :return: The balance of an asset for a portfolio

        :rtype: dict
        """
        return (
            session.query(BalanceModel)
            .filter_by(portfolio_id=portfolio_id, asset=asset)
            .first()
        )

    def get_balance_history(self, session, balance_id) -> list[BalanceHistoryModel]:
        """Get the balance history for a balance

        :param session: The database session
        :param balance_id: The balance id

        :return: The balance history for a balance

        :rtype: dict
        """
        return session.query(BalanceHistoryModel).filter_by(balance_id=balance_id).all()

    def get_orders(self, session, user_id=None, bot_id=None) -> list[OrderModel]:
        """Get the user's orders for a bot

        :param session: The database session
        :param user_id: The user id
        :param bot_id: The bot id

        :return: The user's orders for a bot

        :rtype: list
        """

        if not user_id and not bot_id:
            raise Exception("Either user_id or bot_id must be provided")

        if user_id and bot_id:
            return (
                session.query(OrderModel)
                .filter_by(user_id=user_id, bot_id=bot_id)
                .all()
            )

        elif user_id:
            return session.query(OrderModel).filter_by(user_id=user_id).all()

        elif bot_id:
            return session.query(OrderModel).filter_by(bot_id=bot_id).all()

    def get_open_orders(self, session, user_id) -> list[OrderModel]:
        """Get the user's open orders

        :param session: The database session

        :return: The user's open orders

        :rtype: list
        """
        return (
            session.query(OrderModel)
            .filter_by(user_id=user_id, status=OrderStatus.NEW.value)
            .all()
        )

    def update_signal(self, session, id: int, signal: str) -> SignalModel:
        """Update the autotrade signal for the currency pairs

        :param session: The database session
        :param id: The currency pair config id
        :param signal: The signal

        :return: The signal model

        :rtype: list
        """

        result: SignalModel = session.query(SignalModel).filter_by(id=id).first()
        result.signal = Signal[signal]
        return result

    def update_last_trade_time(self, session, id, last_trade_time) -> SignalModel:
        """Update the autotrade last trade time for the currency pairs

        :param session: The database session
        :param id: The currency pair config id
        :param last_trade_time: The last trade time

        :return: The signal model

        :rtype: list
        """

        result: SignalModel = session.query(SignalModel).filter_by(id=id).first()
        result.last_trade_time = last_trade_time
        return result

    def update_balance(
        self, session, portfolio_id, asset, free, locked, exchange
    ) -> BalanceModel:
        """Update the balance of an asset for a portfolio

        :param session: The database session
        :param portfolio_id: The portfolio id
        :param asset: The asset
        :param free: The free balance
        :param locked: The locked balance

        :return: The balance model

        :rtype: list
        """

        result: BalanceModel = (
            session.query(BalanceModel)
            .filter_by(portfolio_id=portfolio_id, asset=asset)
            .first()
        )
        if result is None:
            result = BalanceModel()
            result.portfolio_id = portfolio_id
            result.asset = asset
            result.free = free
            result.locked = locked
            result.total = free + locked
            session.add(result)
        else:
            result.free += free
            result.locked += locked
            result.total += free + locked

        session.flush()
        return result
