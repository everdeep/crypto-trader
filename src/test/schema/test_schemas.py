from model import *
from schema import *

import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import app_config

ENGINE = create_engine(app_config.SQLALCHEMY_DATABASE_URI, echo=False, pool_size=20, max_overflow=0)

# ========================
# Fixtures
# ========================


@pytest.fixture
def session():
    """Create a new session"""
    Session = sessionmaker(bind=ENGINE)
    session = Session()
    yield session
    session.close()


# ========================
# Tests
# ========================
def test_address_schema(session):
    """Test the address schema"""
    data = session.query(AddressModel).first()
    data = AddressSchema().dump(data)
    assert "id" in data
    assert "address_line_1" in data
    assert "address_line_2" in data
    assert "city" in data
    assert "state" in data
    assert "country" in data
    assert "postal_code" in data
    assert "updated_at" in data
    assert len(data.keys()) == 8


def test_api_key_schema(session):
    """Test the api_key schema"""
    data = session.query(ApiKeyModel).first()
    data = ApiKeySchema().dump(data)
    assert "api_key" in data
    assert "api_secret" in data
    assert len(data.keys()) == 2


def test_signal_schema(session):
    """Test the signal schema"""
    data = session.query(SignalModel).first()
    data = SignalSchema().dump(data)
    assert "id" in data
    assert "currency_pair_config_id" in data
    assert "signal" in data
    assert "last_trade_time" in data
    assert "updated_at" in data
    assert len(data.keys()) == 5


def test_balance_schema(session):
    """Test the balance schema"""
    data = session.query(BalanceModel).first()
    data = BalanceSchema().dump(data)
    assert "id" in data
    assert "portfolio_id" in data
    assert "asset" in data
    assert "free" in data
    assert "locked" in data
    assert "total" in data
    assert "updated_at" in data
    assert len(data.keys()) == 7


def test_currency_pair_schema(session):
    """Test the currency_pair schema"""
    data = session.query(CurrencyPairModel).first()
    data = CurrencyPairSchema().dump(data)
    assert "currency_pair" in data
    assert "symbol" in data
    assert "pair" in data
    assert len(data.keys()) == 3


def test_currency_pair_config_schema(session):
    """Test the currency_pair_config schema"""
    data = session.query(CurrencyPairConfigModel).first()
    data = CurrencyPairConfigSchema().dump(data)
    assert "id" in data
    assert "user_id" in data
    assert "currency_pair" in data
    assert "bot_name" in data
    assert "exchange" in data
    assert "interval" in data
    assert "strategy" in data
    assert "limit" in data
    assert "stop_loss" in data
    assert "take_profit" in data
    assert "earnings" in data
    assert "allocated_balance" in data
    assert "currency_free" in data
    assert "currency_locked" in data
    assert "asset_free" in data
    assert "asset_locked" in data
    assert "is_active" in data
    assert "is_decommissioned" in data
    assert "is_simulated" in data
    assert "updated_at" in data
    assert "signal" in data
    assert "orders" in data
    assert "strategy_config" in data
    assert len(data.keys()) == 23


def test_order_schema(session):
    """Test the order schema"""
    data = session.query(OrderModel).first()
    data = OrderSchema().dump(data)
    assert "id" in data
    assert "user_id" in data
    assert "currency_pair" in data
    assert "order_id" in data
    assert "bot_id" in data
    assert "exchange" in data
    assert "cost" in data
    assert "last_price" in data
    assert "amount" in data
    assert "side" in data
    assert "status" in data
    assert "type" in data
    assert "limit_price" in data
    assert "is_autotraded" in data
    assert "is_simulated" in data
    assert "created_at" in data
    assert "updated_at" in data
    assert len(data.keys()) == 17


def test_portfolio_schema(session):
    """Test the portfolio schema"""
    data = session.query(PortfolioModel).first()
    data = PortfolioSchema().dump(data)
    assert "id" in data
    assert "user_id" in data
    assert "total_earnings" in data
    assert "updated_at" in data
    assert "balances" in data
    assert len(data.keys()) == 5


def test_strategy_config_schema(session):
    """Test the strategy_config schema"""
    data = session.query(StrategyConfigModel).first()
    data = StrategyConfigSchema().dump(data)
    assert "id" in data
    assert "currency_pair_config_id" in data
    assert "strategy" in data
    assert "key" in data
    assert "value" in data
    assert len(data.keys()) == 5


def test_symbol_schema(session):
    """Test the symbols schema"""
    data = session.query(SymbolModel).first()
    data = SymbolSchema().dump(data)
    assert "symbol" in data
    assert "currency_pairs" in data
    assert len(data.keys()) == 2


def test_user_schema(session):
    """Test the user schema"""
    data = session.query(UserModel).first()
    data = UserSchema().dump(data)
    assert "id" in data
    assert "email" in data
    assert "_password" not in data
    assert "first_name" in data
    assert "last_name" in data
    assert "username" in data
    assert "dob" in data
    assert "phone" in data
    assert "address_id" not in data
    assert "portfolio_id" not in data
    assert "is_admin" not in data
    assert "is_active" not in data
    assert "is_verified" in data
    assert "created_at" not in data
    assert "updated_at" not in data
    assert "address" in data
    assert "portfolio" in data
    assert "settings" in data
    # assert "api_keys" not in data
    # assert "orders" in data
    # assert "currency_pair_configs" in data
    # assert "activity" in data
    assert len(data.keys()) == 11


def test_user_settings_schema(session):
    """Test the user_settings schema"""
    data = session.query(UserSettingsModel).first()
    data = UserSettingsSchema().dump(data)
    assert "id" in data
    assert "user_id" in data
    assert "key" in data
    assert "value" in data
    assert len(data.keys()) == 4
