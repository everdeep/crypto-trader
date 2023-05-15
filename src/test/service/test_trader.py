from unittest.mock import MagicMock, PropertyMock, patch
import pytest

from service.trader import TraderService
from cryptolib.enums import Signal, ExchangeType, OrderType, OrderStatus, OrderSide
from test.mock_data import currency_pair_config, order_buy, order_sell


@pytest.fixture
def exchange():
    exchange = MagicMock()
    exchange.get_symbol_ticker().get.side_effect = [
        100.0,
        105.0,
        85.0,
        110.0,
    ]
    return exchange


@pytest.fixture
def config():
    return currency_pair_config


@pytest.fixture
def session():
    session = MagicMock()
    return session


def test_buy_order(exchange, session, config):
    # test
    trader = TraderService(exchange)
    order = trader.create_order(session, Signal.BUY, config)
    assert order.user_id == "1"
    assert order.currency_pair == "BTCUSDT"
    assert order.exchange == ExchangeType.BINANCE
    assert order.cost == 1000.0
    assert order.last_price == 100.0
    assert order.amount == 10.0
    assert order.side == OrderSide.BUY
    assert order.status == OrderStatus.NEW
    assert order.type == OrderType.LIMIT
    assert order.limit_price == 100.0
    assert order.is_autotraded == True
    assert order.is_simulated == True

    # Check balance is correctly adjusted
    assert currency_pair_config.currency_free == 0.0
    assert currency_pair_config.currency_locked == 1000.0


def test_sell_order(exchange, session, config):
    # setup
    config.currency_locked = 1234.0
    config.asset_free = 0.1

    # test
    trader = TraderService(exchange)
    order = trader.create_order(session, Signal.SELL, config)
    assert order.user_id == "1"
    assert order.currency_pair == "BTCUSDT"
    assert order.exchange == ExchangeType.BINANCE
    assert order.cost == 0.1
    assert order.last_price == 100.0
    assert order.amount == 10.0
    assert order.side == OrderSide.SELL
    assert order.status == OrderStatus.NEW
    assert order.type == OrderType.LIMIT
    assert order.limit_price == 100.0
    assert order.is_autotraded == True
    assert order.is_simulated == True

    # Check balance is correctly adjusted
    assert currency_pair_config.asset_free == 0.0
    assert currency_pair_config.asset_locked == 0.1


def test_buy_order_no_currency_balance(exchange, session, config):
    # setup
    currency_pair_config.currency_free = 0.0

    # test
    trader = TraderService(exchange)
    order = trader.create_order(session, Signal.BUY, config)
    assert order is None


def test_sell_order_no_asset_balance(exchange, session, config):
    # setup
    currency_pair_config.asset_free = 0.0

    # test
    trader = TraderService(exchange)
    order = trader.create_order(session, Signal.SELL, config)
    assert order is None


def test_update_order_buy(exchange, session, config):
    # setup
    config.asset_free = 0.2
    config.asset_locked = 0.0
    config.currency_free = 0.0
    config.currency_locked = 1000.0

    # test
    trader = TraderService(exchange)
    order = trader.update_order(session, order_buy, config)
    assert order.status == OrderStatus.FILLED
    assert config.currency_free == 0.0
    assert config.currency_locked == 0.0
    assert config.asset_free == 10.2
    assert config.asset_locked == 0.0


def test_update_order_sell(exchange, session, config):
    # setup
    config.asset_free = 0.0
    config.asset_locked = 0.1
    config.currency_free = 1000.0
    config.currency_locked = 0.0

    # test
    trader = TraderService(exchange)
    order = trader.update_order(session, order_sell, config)
    assert order.status == OrderStatus.FILLED
    assert config.currency_free == 1010.0
    assert config.currency_locked == 0.0
    assert config.asset_free == 0.0
    assert config.asset_locked == 0.0


def test_consecutive_trades(exchange, session, config):
    # Starting balance is 5000 USDT and 0 BTC

    # Setup
    config.asset_free = 0.0
    config.asset_locked = 0.0
    config.currency_free = 5000.0
    config.currency_locked = 0.0

    # test
    trader = TraderService(exchange)
    order = trader.create_order(session, Signal.BUY, config)
    assert config.currency_locked == 5000.0

    order = trader.update_order(session, order, config)

    # After first trade, balance is 0 USDT and 50 BTC
    assert order.status == OrderStatus.FILLED
    assert config.currency_free == 0.0
    assert config.currency_locked == 0.0
    assert config.asset_free == 50.0
    assert config.asset_locked == 0.0

    order = trader.create_order(session, Signal.SELL, config)
    assert config.asset_locked == 50.0

    order = trader.update_order(session, order, config)

    # After second trade, balance is 5250 USDT and 0 BTC
    assert order.status == OrderStatus.FILLED
    assert config.currency_free == 5250.0
    assert config.currency_locked == 0.0
    assert config.asset_free == 0.0
    assert config.asset_locked == 0.0

    order = trader.create_order(session, Signal.BUY, config)
    assert config.currency_locked == 5250.0

    order = trader.update_order(session, order, config)

    # After third trade, balance is 0 USDT and ~61.7647 BTC
    assert order.status == OrderStatus.FILLED
    assert config.currency_free == 0.0
    assert config.currency_locked == 0.0
    assert f"{config.asset_free:.4f}" == "61.7647"
    assert config.asset_locked == 0.0

    order = trader.create_order(session, Signal.SELL, config)
    assert f"{config.asset_locked:.4f}" == "61.7647"

    order = trader.update_order(session, order, config)

    # After fourth trade, balance is ~6794.117647 USDT and 0 BTC
    assert order.status == OrderStatus.FILLED
    assert f"{config.currency_free:.6f}" == "6794.117647"
    assert config.currency_locked == 0.0
    assert config.asset_free == 0.0
    assert config.asset_locked == 0.0
