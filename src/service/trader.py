import logging
import json
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

        logging.info(
            f"Creating order for symbol {config.currency_pair} with side {signal.name}."
        )
        
        # Get the last price
        last_price = self.exchange.get_last_price(config.currency_pair)
        if last_price == 0.0:
            logging.warning(
                f"Failed to get last price for symbol {config.currency_pair}"
            )
            return

        order = None
        # Handles the balance check for the order
        order_params = self.exchange.create_order_params(config, signal, last_price)
        if order_params is None:
            logging.info(
                    f"Not enough funds to place {signal.name} order for symbol {config.currency_pair}"
                )
            return

        # if the bot is simulated, then we will not place an order
        # but instead create our own order
        if config.is_simulated:
            # Simulated order
            order = {
                "cost": order_params["cost"],
                "amount": order_params["cost"] / last_price
                if signal == Signal.BUY
                else (cost * last_price),
            }
        else:
            # Create the order
            # cost is the amount of quote currency to use. For example,
            # BTCUSDT (BUY): cost is the amount of USDT to use
            # BTCUSDT (SELL): cost is the amount of BTC to sell
            # On creating an order, the asset is always converted to quote currency
            # to check the minimum notional value. If the minimum notional value is
            # not met, the order will be rejected.
            order = self.exchange.create_order(order_params)

        if order is None:
            logging.warning(
                f"Failed to create order for symbol {config.currency_pair}; user_id: {config.user_id}"
            )
            return

        cost, amount = (
            self.exchange.get_order_cost_and_amount(order)
            if not config.is_simulated
            else (order["cost"], order["amount"])
        )

        # Update the config
        if signal == Signal.BUY:
            config.currency_free -= cost
            config.currency_locked += cost  # The currency is now locked
        else:
            config.asset_free -= cost
            config.asset_locked += cost  # The currency is now locked

        order_id = (
            self.exchange.get_order_id(order) if not config.is_simulated else None
        )
        status = (
            self.exchange.get_order_status(order)
            if not config.is_simulated
            else OrderStatus.FILLED
        )

        # Create an order from the exchange response
        order_record = OrderModel(
            user_id=config.user_id,
            bot_id=config.id,
            currency_pair=config.currency_pair,
            exchange=ExchangeType(config.exchange),
            order_id=order_id,
            cost=cost,
            last_price=last_price,
            amount=amount,
            side=OrderSide[signal.name],
            status=status,
            type=OrderType.MARKET,
            limit_price=None,
            is_autotraded=True,
            is_simulated=config.is_simulated,
            # meta=str(order) if not config.is_simulated else {}, # TODO: Add new field to database
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        session.add(order_record)
        session.flush()

        logging.info(
            f"Order created {config.currency_pair} with side {signal.name} - order_id: {order_record.order_id}"
        )

        return order_record

    def update_order(
        self, session, order: OrderModel, config: CurrencyPairConfigModel
    ) -> OrderModel:
        """Update an order

        :param session: The database session
        :param order: The order

        :return: The order

        :rtype: dict
        """

        logging.info(
            f"Updating order for symbol {order.currency_pair} with order_id {order.order_id}."
        )

        order_res = None
        if not config.is_simulated:
            # Fetch the order from the exchange
            order_res = self.exchange.get_order(
                symbol=order.currency_pair, order_id=order.order_id
            )

        # Only a non-simulated bot will ever enter this if statement
        if order.status != OrderStatus.FILLED:
            order.cost = order_res["cost"]
            order.amount = order_res["amount"]
            # Update the order in the database
            order.status = OrderStatus[order_res["status"]]

        if order.status == OrderStatus.FILLED:
            if not config.is_simulated:
                fees = order_res["fees"]
                # TODO: logic for including fees in the cost

            # Update the bot balances
            if order.side == OrderSide.BUY:
                # Updates the currency balance in both the portfolio and the bot
                config.currency_locked -= order.cost
                config.asset_free += order.amount
                config.earnings -= order.cost
            else:
                # Updates the currency balance in both the portfolio and the bot
                config.asset_locked -= order.cost
                config.currency_free += order.amount
                config.earnings += order.amount

        order.updated_at = datetime.now()
        session.flush()

        logging.info(
            f"Finished updating order for symbol {order.currency_pair} with order_id {order.order_id}."
        )

        return order
