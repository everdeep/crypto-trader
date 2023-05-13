from enum import Enum


class Interval(Enum):
    """The interval enum"""

    MINUTE_1 = "1m"
    MINUTE_3 = "3m"
    MINUTE_5 = "5m"
    MINUTE_15 = "15m"
    MINUTE_30 = "30m"
    HOUR_1 = "1h"
    HOUR_2 = "2h"
    HOUR_4 = "4h"
    HOUR_6 = "6h"
    HOUR_8 = "8h"
    HOUR_12 = "12h"
    DAY_1 = "1d"
    # DAY_3 = "3d"
    # WEEK_1 = "1w"
    # MONTH_1 = "1M"


class Signal(Enum):
    """Trading signals"""

    BUY = 1
    SELL = -1
    HOLD = 0


class StrategyType(Enum):
    """Strategy enum"""

    MACD = "Moving Average Convergence Divergence"
    RSI = "Relative Strength Index"
    STOCHASTIC_OSCILLATOR = "Stochastic Oscillator"
    WILLIAMS_R = "Williams R"
    MOVING_AVERAGE_CROSSOVER = "Moving Average Crossover"
    BOLLINGER_BANDS = "Bollinger Bands"
    MACD_RSI = "MACD/RSI"
    AVERAGE_DIRECTIONAL_INDEX = "Average Directional Index"
    COMMODITY_CHANNEL_INDEX = "Commodity Channel Index"
    CHAIKIN_OSCILLATOR = "Chaikin Oscillator"
    KNOW_SURE_THING = "Know Sure Thing"

class StrategyParams(Enum):
    """Enum for strategy parameters"""

    MACD = {"short_window": (1, 20), "long_window": (20, 40), "signal_window": (1, 5)}
    BOLLINGER_BANDS = {"window": (1, 40), "std": (1, 10)}
    STOCHASTIC_OSCILLATOR = {"window": (1, 60)}
    WILLIAMS_R = {"window": (1, 60)}
    AVERAGE_DIRECTIONAL_INDEX = {"window": (1, 60)}
    COMMODITY_CHANNEL_INDEX = {"window": (1, 60)}
    RSI = {"window": (1, 60)}
    MOVING_AVERAGE_CROSSOVER = {"short_window": (1, 20), "long_window": (20, 40)}
    MACD_RSI = {"short_window": (1, 20), "long_window": (20, 40), "signal_window": (1, 5), "rsi_window": (1, 60)}
    CHAIKIN_OSCILLATOR = {"short_window": (1, 30), "long_window": (10, 40)}
    KNOW_SURE_THING = {"window1": (1,15), "window2": (10, 25), "window3": (20, 35), "window4": (25, 40)}

class ExchangeType(Enum):
    BINANCE = "Binance"


class OrderType(Enum):
    MARKET = "Market"
    LIMIT = "Limit"


class OrderStatus(Enum):
    NEW = "New"
    PARTIALLY_FILLED = "Partially Filled"
    FILLED = "Filled"
    CANCELLED = "Cancelled"
    PENDING_CANCEL = "Pending Cancel"
    REJECTED = "Rejected"
    EXPIRED = "Expired"

class OrderSide(Enum):
    BUY = "Buy"
    SELL = "Sell"