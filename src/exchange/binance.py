import ccxt
import pandas as pd
from binance.spot import Spot
from config import app_config


class Binance:
    def __init__(self, api_key=None, api_secret=None, sandbox=False):
        # Use global dev api keys if no api keys are provided
        if not api_key:
            api_key = app_config.BINANCE_API_KEY
            api_secret = app_config.BINANCE_API_SECRET

        # Using both ccxt and python-binance for now
        self.client = Spot(api_key=api_key, api_secret=api_secret)
        self.exchange = ccxt.binance(
            {
                "apiKey": api_key,
                "secret": api_secret,
                "enableRateLimit": True,
            }
        )

        self.exchange.set_sandbox_mode(sandbox)

    def load_markets(self):
        self.tickers_info = self.exchange.load_markets()

    def get_all_symbols(self):
        data = self.exchange.fetch_tickers()
        return data

    def get_symbol_data(self, symbol, interval, limit):
        return self.client.klines(symbol=symbol, interval=interval, limit=limit)

    def get_symbol_ticker(self, symbol):
        return self.client.ticker_price(symbol)

    def get_account(self):
        return self.client.account()

    def get_balance(self, symbol=None):
        account = self.get_account()
        balances = account["balances"]
        df = pd.DataFrame(balances).astype({"free": "float", "locked": "float"})
        # Only return the balance if it is greater than 0
        df = df[df["free"] > 0]

        if symbol:
            return df[df["asset"] == symbol].iloc[0].to_dict()

        return df.to_dict("records")

    def get_open_orders(self, symbol=None):
        return self.client.get_open_orders(symbol)

    def get_order(self, symbol, order_id):
        return self.exchange.fetch_order(id=order_id, symbol=symbol)

    def get_all_orders(self, symbol, limit=None, start_time=None, end_time=None, order_id=None):
        return self.client.get_orders(
            symbol=symbol, limit=limit, start_time=start_time, end_time=end_time, order_id=order_id
        )

    def create_order(self, order, test=False):
        if test:
            return self.client.new_order_test(**order)

        return self.client.new_order(**order)

    def cancel_order(self, symbol, order_id):
        return self.client.cancel_order(symbol, order_id)
