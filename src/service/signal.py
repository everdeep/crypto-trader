import logging
import pandas as pd
import numpy as np
from cryptolib.enums import StrategyType, Signal


class SignalService:
    def __init__(self, exchange, config):
        self._exchange = exchange
        self._config = config

    def _remove_repeated_signals(self, signals):
        """Removes repeated signals."""
        # replace consecutive ones and negative ones with zero
        signals = signals.mask(signals.eq(signals.shift()) & signals.eq(1), 0)
        signals = signals.mask(signals.eq(signals.shift()) & signals.eq(-1), 0)

        # fill in the NaN values with zeros
        signals = signals.fillna(0)

        return signals

    def _get_params(self, strategy_config):
        """Gets the strategy parameters from the config."""
        params = {}
        for param in strategy_config:
            params[param["key"]] = param["value"]
        return params

    def generate_signal(self) -> Signal:
        id: int = self._config.get("id")
        interval: str = self._config.get("interval")
        currency_pair: str = self._config.get("currency_pair")
        strategy: StrategyType = self._config.get("strategy")
        strategy_config: list[dict] = self._config.get("strategy_config")
        params = self._get_params(strategy_config)

        logging.info(
            f"Generating signal for symbol {currency_pair} with params {{ config_id: {id}, interval: {interval}, strategy: {strategy} }}."
        )

        # Fetch the historical data
        data = []
        try:
            data = self._exchange.get_symbol_data(currency_pair, interval, limit=1000)
        except Exception as e:
            logging.error(
                f"Failed to fetch data for user {self._config.get('user_id')} and symbol {currency_pair} with error: {e}"
            )
            return

        self._data = pd.DataFrame(
            data,
            columns=[
                "time",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "close_time",
                "quote_asset_volume",
                "number_of_trades",
                "taker_buy_base_asset_volume",
                "taker_buy_quote_asset_volume",
                "ignore",
            ],
            dtype=np.float64,
        )
        self._data.set_index("time", inplace=True)
        self._data.index = pd.to_datetime(self._data.index, unit="ms")

        if strategy == StrategyType.MACD.value:
            return self.macd(**params)
        elif strategy == StrategyType.RSI.value:
            return self.rsi(**params)
        elif strategy == StrategyType.STOCHASTIC_OSCILLATOR.value:
            return self.stochastic_oscillator(**params)
        elif strategy == StrategyType.WILLIAMS_R.value:
            return self.williams_r(**params)
        elif strategy == StrategyType.MOVING_AVERAGE_CROSSOVER.value:
            return self.moving_average_crossover(**params)
        elif strategy == StrategyType.BOLLINGER_BANDS.value:
            return self.bollinger_bands(**params)
        elif strategy == StrategyType.MACD_RSI.value:
            return self.macd_rsi(**params)
        elif strategy == StrategyType.AVERAGE_DIRECTIONAL_INDEX.value:
            return self.average_directional_index(**params)
        elif strategy == StrategyType.COMMODITY_CHANNEL_INDEX.value:
            return self.commodity_channel_index(**params)
        elif strategy == StrategyType.CHAIKIN_OSCILLATOR.value:
            return self.chaikin_oscillator(**params)
        elif strategy == StrategyType.KNOW_SURE_THING.value:
            return self.know_sure_thing(**params)
        else:
            raise ValueError(f"Invalid strategy {strategy}")

    def moving_average_crossover(self, short_window=50, long_window=100) -> Signal:
        """Plots the moving average crossover for a cryptocurrency symbol"""
        close = self._data.get("close")
        short_rolling = close.rolling(window=short_window).mean()
        long_rolling = close.rolling(window=long_window).mean()
        signal = pd.Series(0, index=self._data.index)
        signal[short_rolling > long_rolling] = Signal.BUY.value
        signal[short_rolling < long_rolling] = Signal.SELL.value
        return Signal(signal.iloc[-1])

    def bollinger_bands(self, window=20, std=2, cooldown=5) -> Signal:
        """Plots the bollinger bands for a cryptocurrency symbol"""
        last_trade_time = self._config.get("signal").get("last_trade_time")
        if last_trade_time:
            last_trade_time = pd.to_datetime(last_trade_time)
            if (pd.Timestamp.now() - last_trade_time).total_seconds() < cooldown:
                return Signal.HOLD

        close = self._data.get("close")
        rolling_mean = close.rolling(window=window).mean()
        rolling_std = close.rolling(window=window).std()
        upper_band = rolling_mean + (rolling_std * std)
        lower_band = rolling_mean - (rolling_std * std)
        signal = pd.Series(0, index=self._data.index)
        signal[close > upper_band] = Signal.BUY.value
        signal[close < lower_band] = Signal.SELL.value
        return Signal(signal.iloc[-1])

    def macd(self, short_window=12, long_window=26, signal_window=9) -> Signal:
        """Plots the macd for a cryptocurrency symbol"""
        close = self._data.get("close")
        short_ema = close.ewm(span=short_window, adjust=False).mean()
        long_ema = close.ewm(span=long_window, adjust=False).mean()
        macd = short_ema - long_ema
        signal = macd.ewm(span=signal_window, adjust=False).mean()
        signal = pd.Series(0, index=self._data.index)
        signal[macd > signal] = Signal.BUY.value
        signal[macd < signal] = Signal.SELL.value
        return Signal(signal.iloc[-1])

    def rsi(self, window=14) -> Signal:
        """Plots the rsi for a cryptocurrency symbol"""
        close = self._data.get("close")
        delta = close.diff()
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0
        roll_up1 = up.ewm(com=window - 1, adjust=False).mean()
        roll_down1 = down.abs().ewm(com=window - 1, adjust=False).mean()
        rs = roll_up1 / roll_down1
        rsi = 100.0 - (100.0 / (1.0 + rs))
        signal = pd.Series(0, index=self._data.index)
        signal[rsi < 30] = Signal.BUY.value
        signal[rsi > 70] = Signal.SELL.value
        return Signal(signal.iloc[-1])

    def stochastic_oscillator(self, window=14):
        """Plots the stochastic oscillator for a cryptocurrency symbol"""
        close = self._data.get("close")
        high = self._data.get("high")
        low = self._data.get("low")
        k = 100 * (
            (close - low.rolling(window).min())
            / (high.rolling(window).max() - low.rolling(window).min())
        )
        d = k.rolling(3).mean()
        signals = pd.Series(0, index=self._data.index)
        signals[k > d] = Signal.BUY.value
        signals[k < d] = Signal.SELL.value
        return Signal(signals.iloc[-1])

    def williams_r(self, window=14) -> Signal:
        """Plots the williams r for a cryptocurrency symbol"""
        close = self._data.get("close")
        high = self._data.get("high")
        low = self._data.get("low")
        r = 100 * (
            (high.rolling(window).max() - close)
            / (high.rolling(window).max() - low.rolling(window).min())
        )
        signal = pd.Series(0, index=self._data.index)
        signal[r < -80] = Signal.BUY.value
        signal[r > -20] = Signal.SELL.value
        return Signal(signal.iloc[-1])

    def average_directional_index(self, window=14, plot=False) -> Signal:
        """Plots the average directional index for a cryptocurrency symbol"""
        close = self._data.get("close")
        high = self._data.get("high")
        low = self._data.get("low")
        tr = high - low
        tr1 = high - close.shift(1)
        tr2 = close.shift(1) - low
        tr = tr.combine(tr1, max).combine(tr2, max)
        tr = tr.rolling(window).sum()
        dm = high - high.shift(1)
        dm1 = low.shift(1) - low
        dm = dm.combine(dm1, max)
        dm = dm.clip(lower=0)
        dm = dm.rolling(window).sum()
        pdi = dm / tr
        mdi = -dm / tr
        dx = (pdi - mdi).abs() / (pdi + mdi)
        adx = dx.rolling(window).mean()
        signal = pd.Series(0, index=self._data.index)
        signal[adx < 20] = Signal.BUY.value
        signal[adx > 50] = Signal.SELL.value
        return Signal(signal.iloc[-1])

    def commodity_channel_index(self, window=20) -> Signal:
        """Plots the commodity channel index for a cryptocurrency symbol"""
        close = self._data.get("close")
        high = self._data.get("high")
        low = self._data.get("low")
        tp = (high + low + close) / 3
        cci = (tp - tp.rolling(window).mean()) / (0.015 * tp.rolling(window).std())
        signal = pd.Series(0, index=self._data.index)
        signal[cci < -100] = Signal.BUY.value
        signal[cci > 100] = Signal.SELL.value
        return Signal(signal.iloc[-1])

    def macd_rsi(
        self, short_window=12, long_window=26, signal_window=9, rsi_window=14
    ) -> Signal:
        close = self._data.get("close")
        short_ema = close.ewm(span=short_window, adjust=False).mean()
        long_ema = close.ewm(span=long_window, adjust=False).mean()
        macd = short_ema - long_ema
        signal = macd.ewm(span=signal_window, adjust=False).mean()
        signal = pd.Series(0, index=self._data.index)
        signal[macd > signal] = Signal.BUY.value
        signal[macd < signal] = Signal.SELL.value
        rsi = self.rsi(rsi_window)
        if signal.iloc[-1] == Signal.BUY.value and rsi == Signal.BUY.value:
            return Signal.BUY
        elif signal.iloc[-1] == Signal.SELL.value and rsi == Signal.SELL.value:
            return Signal.SELL
        else:
            return Signal.HOLD

    def chaikin_oscillator(self, short_window=3, long_window=10):
        """Plots the chaikin oscillator for a cryptocurrency symbol"""
        close = self._data.get("close")
        high = self._data.get("high")
        low = self._data.get("low")
        volume = self._data.get("volume")
        adl = ((close - low) - (high - close)) / (high - low)
        adl = adl * volume
        adl = adl.rolling(short_window).sum() - adl.rolling(long_window).sum()
        signals = pd.Series(0, index=self._data.index)
        signals[adl > 0] = Signal.BUY.value
        signals[adl < 0] = Signal.SELL.value
        return Signal(signals.iloc[-1])

    def know_sure_thing(self, window1=10, window2=15, window3=20, window4=30):
        """Plots the know sure thing for a cryptocurrency symbol"""
        close = self._data.get("close")
        roc1 = close.diff(window1)
        roc2 = close.diff(window2)
        roc3 = close.diff(window3)
        roc4 = close.diff(window4)
        kst = (roc1 * 1) + (roc2 * 2) + (roc3 * 3) + (roc4 * 4)
        kst = kst.rolling(9).mean()
        signals = pd.Series(0, index=self._data.index)
        signals[kst > 0] = Signal.BUY.value
        signals[kst < 0] = Signal.SELL.value
        return Signal(signals.iloc[-1])
