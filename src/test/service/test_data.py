from unittest.mock import MagicMock
import pytest

from enums import Signal
from service import DataService
from test.mock_data import api_key, portfolio, order_buy, currency_pair_config, signal


@pytest.fixture
def session():
    """Session fixture"""
    session = MagicMock()
    yield session


# patch
def test_get_api_keys(session):
    """Test the get_api_keys method"""

    session.query().filter_by().first.return_value = api_key
    data = DataService().get_api_key(session, "1", "Binance")
    assert data.get("api_key") == "test"
    assert data.get("api_secret") == "test_secret"


def test_get_active_bots(session):
    """Test the get_active_bots method"""

    session.query().filter_by().all.return_value = [currency_pair_config]

    data = DataService().get_active_bots(session)
    signal = data[0].signal
    assert signal.signal.name == "HOLD"


def test_get_currency_pair_config(session):
    """Test the get_currency_pair_config method"""

    session.query().filter_by().first.return_value = currency_pair_config

    data = DataService().get_currency_pair_config(session, 1)
    assert data.user_id == "1"
    assert data.currency_pair == "BTCUSDT"
    assert data.exchange.value == "Binance"
    assert data.interval.value == "1m"
    assert data.strategy.value == "Bollinger Bands"
    assert data.limit == 1000
    assert data.stop_loss == 0.3
    assert data.take_profit == 0.3
    assert data.allocated_balance == 1000.0
    assert data.currency_free == 1000.0
    assert data.currency_locked == 0.0
    assert data.is_active == True
    assert data.is_simulated == True
    assert data.signal.signal.name == "HOLD"
    assert data.strategy_config[0].strategy.value == "Bollinger Bands"
    assert data.strategy_config[0].key == "window"
    assert data.strategy_config[0].value == 20
    assert data.strategy_config[1].strategy.value == "Bollinger Bands"
    assert data.strategy_config[1].key == "std"
    assert data.strategy_config[1].value == 2


def test_get_portfolio(session):
    """Test the get_portfolio method"""

    session.query().filter_by().first.return_value = portfolio

    data = DataService().get_portfolio(session, "1")
    assert data.user_id == "1"
    assert data.total_earnings == 0.0
    assert data.balances[0].asset == "BTC"
    assert data.balances[0].free == 0.1
    assert data.balances[0].locked == 0.0
    assert data.balances[1].asset == "USDT"
    assert data.balances[1].free == 1000.0
    assert data.balances[1].locked == 0.0


def test_get_open_orders(session):
    """Test the get_open_orders method"""

    session.query().filter_by().all.return_value = [order_buy]

    data = DataService().get_open_orders(session, "1")
    assert data[0].user_id == "1"
    assert data[0].currency_pair == "BTCUSDT"
    assert data[0].order_id == "123456"
    assert data[0].exchange.value == "Binance"
    assert data[0].cost == 1000.0
    assert data[0].last_price == 100.0
    assert data[0].status.value == "New"
    assert data[0].amount == 10.0
    assert data[0].side.value == "Buy"
    assert data[0].type.value == "Limit"
    assert data[0].limit_price == 100.0
    assert data[0].is_autotraded == True
    assert data[0].is_simulated == True


def test_update_signal(session):
    """Test the update_signal method"""

    session.query().filter_by().first.return_value = signal

    data = DataService().update_signal(session, 1, Signal.HOLD.name)
    assert data.signal.value == 0
