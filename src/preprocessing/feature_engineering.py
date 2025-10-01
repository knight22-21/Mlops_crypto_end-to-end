import pandas as pd
import ta

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add lag features, moving averages, and technical indicators.
    Expects df with 'timestamp' and 'close'.
    """
    df = df.copy().sort_values("timestamp")

    # Lag features
    for lag in [1, 2, 3, 6, 12, 24]:
        df[f"lag_{lag}h"] = df["close"].shift(lag)

    # Moving averages
    df["ma_6h"] = df["close"].rolling(window=6).mean()
    df["ma_12h"] = df["close"].rolling(window=12).mean()

    # RSI
    df["rsi"] = ta.momentum.RSIIndicator(close=df["close"], window=14).rsi()

    # MACD
    macd = ta.trend.MACD(close=df["close"])
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()

    # Bollinger Bands
    boll = ta.volatility.BollingerBands(close=df["close"], window=20, window_dev=2)
    df["bollinger_hband"] = boll.bollinger_hband()
    df["bollinger_lband"] = boll.bollinger_lband()

    return df.dropna().reset_index(drop=True)
