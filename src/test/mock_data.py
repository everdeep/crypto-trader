from datetime import datetime
from model import (
    CurrencyPairConfigModel,
    SignalModel,
    OrderModel,
    PortfolioModel,
    BalanceModel,
    CurrencyPairModel,
    StrategyConfigModel,
)
from enums import Interval, ExchangeType, Signal, StrategyType, OrderStatus, OrderSide, OrderType

api_key = {"api_key": "test", "api_secret": "test_secret", "exchange": "Binance"}

signal = SignalModel(
    id=1,
    currency_pair_config_id="1",
    signal=Signal.HOLD,
    last_trade_time=datetime(2023, 3, 16, 0, 33, 5),
    updated_at=datetime(2023, 3, 16, 0, 33, 5),
)

# Currency Pair Config
currency_pair_config = CurrencyPairConfigModel(
    id="1",
    user_id="1",
    currency_pair="BTCUSDT",
    bot_name="test",
    exchange=ExchangeType.BINANCE,
    interval=Interval.MINUTE_1,
    strategy=StrategyType.BOLLINGER_BANDS,
    limit=1000,
    stop_loss=0.3,
    take_profit=0.3,
    earnings=0.0,
    allocated_balance=1000.0,
    currency_free=1000.0,
    currency_locked=0.0,
    asset_free=0.0,
    asset_locked=0.0,
    is_active=True,
    is_decommissioned=False,
    is_simulated=True,
    updated_at=datetime(2023, 3, 16, 0, 33, 5),
    signal=signal,
    strategy_config=[
        StrategyConfigModel(
            id="1",
            currency_pair_config_id="1",
            strategy=StrategyType.BOLLINGER_BANDS,
            key="window",
            value=20,
        ),
        StrategyConfigModel(
            id="2",
            currency_pair_config_id="1",
            strategy=StrategyType.BOLLINGER_BANDS,
            key="std",
            value=2,
        ),
    ],
)

# Portfolio
portfolio = PortfolioModel(
    id="1",
    user_id="1",
    total_earnings=0.0,
    balances=[
        BalanceModel(
            asset="BTC",
            free=0.1,
            locked=0.0,
            total=0.1,
        ),
        BalanceModel(
            asset="USDT",
            free=1000.0,
            locked=0.0,
            total=1000.0,
        ),
    ],
)

# Currency Pair
currency_pair = CurrencyPairModel(
    currency_pair="BTCUSDT",
    symbol="BTC",
    pair="USDT",
)

# Asset Balance
asset_balance = BalanceModel(
    asset="BTC",
    free=0.1,
    locked=0.0,
    total=0.1,
)

# Currency Balance
currency_balance = BalanceModel(
    asset="USDT",
    free=1000.0,
    locked=0.0,
    total=1000.0,
)

# Buy Order
order_buy = OrderModel(
    id="1",
    user_id="1",
    currency_pair="BTCUSDT",
    order_id="123456",
    exchange=ExchangeType.BINANCE,
    cost=1000.0,
    last_price=100.0,
    status=OrderStatus.NEW,
    amount=10.0,
    side=OrderSide.BUY,
    type=OrderType.LIMIT,
    limit_price=100.0,
    is_autotraded=True,
    is_simulated=True,
    created_at=datetime(2023, 3, 16, 0, 33, 5),
    updated_at=datetime(2023, 3, 16, 0, 33, 5),
)

# Sell Order
order_sell = OrderModel(
    id="1",
    user_id="1",
    currency_pair="BTCUSDT",
    order_id="123456",
    exchange=ExchangeType.BINANCE,
    cost=0.1,
    last_price=100.0,
    status=OrderStatus.NEW,
    amount=10.0,
    side=OrderSide.SELL,
    type=OrderType.LIMIT,
    limit_price=100.0,
    is_autotraded=True,
    is_simulated=True,
    created_at=datetime(2023, 3, 16, 0, 33, 5),
    updated_at=datetime(2023, 3, 16, 0, 33, 5),
)
