from monitor.tasks import do_scheduled_autotrade, do_buy_sell
from unittest.mock import patch

from cryptolib.enums import Signal
from cryptolib.schema import CurrencyPairConfigSchema
from test.mock_data import currency_pair_config


@patch("monitor.tasks.DataService.get_active_bots", return_value=[])
@patch("monitor.tasks.do_buy_sell.delay")
def test_do_scheduled_autotrade_no_pairs(do_buy_sell, get_active_bots):
    """Tests the do_generate_signals method with no currency pairs"""
    # Call the method
    do_scheduled_autotrade()

    # Assert the generate_signal method was not called
    do_buy_sell.assert_not_called()


@patch(
    "monitor.tasks.DataService.get_active_bots",
    return_value=[currency_pair_config],
)
@patch(
    "monitor.tasks.DataService.get_currency_pair_config",
    return_value=currency_pair_config,
)
@patch("monitor.tasks.do_buy_sell.delay")
def test_do_scheduled_autotrade(do_buy_sell, b, c):
    """Tests the do_generate_signals method"""

    # Call the method
    do_scheduled_autotrade()

    # Assert the generate_signal method was called
    config = CurrencyPairConfigSchema().dump(currency_pair_config)
    do_buy_sell.assert_called_once_with(config)


@patch(
    "monitor.tasks.DataService.get_api_key",
    return_value={"api_key": "key", "api_secret": "secret"},
)
@patch("monitor.tasks.ExchangeService.get_exchange", return_value="exchange")
@patch("monitor.tasks.SignalService.generate_signal", return_value=Signal.BUY)
@patch("monitor.tasks.TraderService.create_order", return_value="order")
@patch("monitor.tasks.TraderService.update_order")
@patch("monitor.tasks.update_signal.delay")
def test_do_buy_sell(update_signal, update_order, d, e, f, g):
    """Tests the generate_signal method"""
    # Call the method
    config = CurrencyPairConfigSchema().dump(currency_pair_config)
    do_buy_sell(config)

    # Assert the generate_signal method was called
    update_signal.assert_called_once_with(1, Signal.BUY.name)
    update_order.call_count == 1
    update_order.call_args_list[0][0][1] == "order"
