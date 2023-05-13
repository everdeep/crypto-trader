from exchange import Binance
from enums import ExchangeType


class ExchangeService:
    def get_exchange(self, exchange, api_key, api_secret):
        if exchange == ExchangeType.BINANCE.value:
            return Binance(api_key, api_secret)
        else:
            raise ValueError("Invalid exchange type of {}".format(exchange))
