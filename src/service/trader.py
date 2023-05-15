import logging
from datetime import datetime
from cryptolib.model import OrderModel, CurrencyPairConfigModel
from cryptolib.enums import Signal, OrderType, OrderStatus, OrderSide, ExchangeType


class TraderService:
    def __init__(self, exchange):
        self.exchange = exchange

    def create_order(
        self, session, signal: Signal, config: CurrencyPairConfigModel
    ) -> OrderModel:
        """Put an order

        :param session: The database session
        :param signal: The signal

        :return: The order

        :rtype: OrderModel
        """

        # TODO: Add asset allocation feature
        # TODO: Add implementation with Binance API and store the order in the database

        # Get the last price of the symbol
        last_price = self.exchange.get_symbol_ticker(config.currency_pair).get("price")

        cost = 0
        amount = 0

        # Check if the user has enough funds to place the order
        if signal == Signal.BUY:
            cost = config.currency_free  # The cost is the amount of currency
            amount = cost / float(
                last_price
            )  # The amount is the amount of asset gained
            config.currency_free = 0
            config.currency_locked += cost  # The currency is now locked
        else:
            cost = config.asset_free  # The cost is the amount of asset
            amount = cost * float(
                last_price
            )  # The amount is the amount of currency gained
            config.asset_free = 0
            config.asset_locked += cost  # The currency is now locked

        if cost <= 0:
            logging.info(
                f"Not enough funds to place {signal.name} order for symbol {config.currency_pair}"
            )
            return

        logging.info(
            f"Creating order for symbol {config.currency_pair} with side {signal.name}."
        )

        order = OrderModel(
            user_id=config.user_id,
            bot_id=config.id,
            currency_pair=config.currency_pair,
            exchange=ExchangeType(config.exchange),
            cost=cost,
            last_price=last_price,
            amount=amount,
            side=OrderSide[signal.name],
            status=OrderStatus.NEW,
            type=OrderType.LIMIT,
            limit_price=last_price,
            is_autotraded=True,
            is_simulated=config.is_simulated,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        session.add(order)
        session.flush()

        logging.info(
            f"Order created {config.currency_pair} with side {signal.name} - order_id: {order.order_id}"
        )

        return order

    def update_order(
        self, session, order: OrderModel, config: CurrencyPairConfigModel
    ) -> OrderModel:
        """Update an order

        :param session: The database session
        :param order: The order

        :return: The order

        :rtype: dict
        """

        # TODO: Add implementation with Binance API and update the order in the database

        logging.info(
            f"Updating order for symbol {order.currency_pair} with order_id {order.order_id}."
        )

        # Check if the user has enough funds to place the order
        if order.side == OrderSide.BUY:
            # Updates the currency balance in both the portfolio and the bot
            config.currency_locked = 0
            config.asset_free += order.amount
            config.earnings -= order.cost
        else:
            # Updates the currency balance in both the portfolio and the bot
            config.asset_locked = 0
            config.currency_free += order.amount
            config.earnings += order.amount

        order.status = OrderStatus.FILLED
        order.updated_at = datetime.now()
        session.flush()

        logging.info(
            f"Finished updating order for symbol {order.currency_pair} with order_id {order.order_id}."
        )

        return order
