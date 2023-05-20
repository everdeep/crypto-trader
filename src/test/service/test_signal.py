from unittest.mock import MagicMock
from service import SignalService
from cryptolib.enums import Signal, StrategyType
from cryptolib.model import StrategyConfigModel
from cryptolib.schema import CurrencyPairConfigSchema
from test.mock_data import currency_pair_config

import pytest


@pytest.fixture
def exchange():
    """Exchange fixture"""
    exchange = MagicMock()
    exchange.get_klines.return_value = [
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    ]
    yield exchange


@pytest.fixture
def config():
    """config fixture"""
    return CurrencyPairConfigSchema().dump(currency_pair_config)


def test_generate_signal_bollinger_bands(exchange, config):
    """Tests the generate_signal method"""
    signal_service = SignalService(exchange, config)
    signal = signal_service.generate_signal()
    assert signal == Signal.HOLD


def test_generate_signal_invalid_strategy(exchange, config):
    """Tests the generate_signal method with an invalid strategy"""
    config["strategy"] = "invalid"
    signal_service = SignalService(exchange, config)
    with pytest.raises(ValueError):
        signal_service.generate_signal()


def test_generate_signal_macd(exchange, config):
    """Tests the generate_signal method with the MACD strategy"""
    config["strategy"] = StrategyType.MACD.value
    config["strategy_config"] = [
        {
            "strategy": StrategyType.MACD.value,
            "key": "short_window",
            "value": 2,
        },
        {
            "strategy": StrategyType.MACD.value,
            "key": "long_window",
            "value": 15,
        },
        {
            "strategy": StrategyType.MACD.value,
            "key": "signal_window",
            "value": 5,
        },
    ]
    signal_service = SignalService(exchange, config)
    signal = signal_service.generate_signal()
    assert signal == Signal.HOLD


def test_generate_signal_rsi(exchange, config):
    """Tests the generate_signal method with the RSI strategy"""
    config["strategy"] = StrategyType.RSI.value
    config["strategy_config"] = [
        {
            "strategy": StrategyType.RSI.value,
            "key": "window",
            "value": 10,
        }
    ]
    signal_service = SignalService(exchange, config)
    signal = signal_service.generate_signal()
    assert signal == Signal.HOLD


def test_generate_signal_stochastic_oscillator(exchange, config):
    """Tests the generate_signal method with the Stochastic Oscillator strategy"""
    config["strategy"] = StrategyType.STOCHASTIC_OSCILLATOR.value
    config["strategy_config"] = [
        {
            "strategy": StrategyType.STOCHASTIC_OSCILLATOR.value,
            "key": "window",
            "value": 10,
        }
    ]
    signal_service = SignalService(exchange, config)
    signal = signal_service.generate_signal()
    assert signal == Signal.HOLD


def test_generate_signal_williams_r(exchange, config):
    """Tests the generate_signal method with the Williams R strategy"""
    config["strategy"] = StrategyType.WILLIAMS_R.value
    config["strategy_config"] = [
        {
            "strategy": StrategyType.WILLIAMS_R.value,
            "key": "window",
            "value": 10,
        }
    ]
    signal_service = SignalService(exchange, config)
    signal = signal_service.generate_signal()
    assert signal == Signal.HOLD


def test_generate_signal_moving_average_crossover(exchange, config):
    """Tests the generate_signal method with the Moving Average Crossover strategy"""
    config["strategy"] = StrategyType.MOVING_AVERAGE_CROSSOVER.value
    config["strategy_config"] = [
        {
            "strategy": StrategyType.MOVING_AVERAGE_CROSSOVER.value,
            "key": "short_window",
            "value": 10,
        },
        {
            "strategy": StrategyType.MOVING_AVERAGE_CROSSOVER.value,
            "key": "long_window",
            "value": 20,
        },
    ]
    signal_service = SignalService(exchange, config)
    signal = signal_service.generate_signal()
    assert signal == Signal.HOLD


def test_generate_signal_macd_rsi(exchange, config):
    """Tests the generate_signal method with the MACD RSI strategy"""
    config["strategy"] = StrategyType.MACD_RSI.value
    config["strategy_config"] = [
        {
            "strategy": StrategyType.MACD_RSI.value,
            "key": "short_window",
            "value": 2,
        },
        {
            "strategy": StrategyType.MACD_RSI.value,
            "key": "long_window",
            "value": 15,
        },
        {
            "strategy": StrategyType.MACD_RSI.value,
            "key": "signal_window",
            "value": 5,
        },
        {
            "strategy": StrategyType.MACD_RSI.value,
            "key": "rsi_window",
            "value": 14,
        },
    ]
    signal_service = SignalService(exchange, config)
    signal = signal_service.generate_signal()
    assert signal == Signal.HOLD
