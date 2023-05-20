from service import ExchangeService

import pytest


@pytest.fixture
def api_keys():
    api_keys = {
        "binance": {"api_key": "test_key", "api_secret": "test_secret"},
    }

    yield api_keys


def test_get_binance_exchange(api_keys):
    exchange = ExchangeService().get_exchange("Binance", **api_keys["binance"])
    assert exchange is not None


def test_get_exchange_invalid_exchange(api_keys):
    with pytest.raises(ValueError):
        ExchangeService().get_exchange("invalid_exchange", **api_keys["binance"])
