import pandas as pd
import requests
import time


def fetch_data(exchange, symbol, interval, start=None, end=None, mode="backtest"):
    if exchange == "binance":
        if mode == "backtest":
            return get_binance_historical(symbol, interval, start, end)
        else:
            return get_binance_live(symbol, interval)

    elif exchange == "bybit":
        if mode == "backtest":
            return get_bybit_historical(symbol, interval, start, end)
        else:
            return get_bybit_live(symbol, interval)

    else:
        raise ValueError(f"Exchange '{exchange}' not supported yet.")


# ---- Binance (Public API) ----
def get_binance_historical(symbol, interval, start, end):
    base_url = "https://api.binance.com/api/v3/klines"
    all_data = []
    start_time = int(pd.Timestamp(start).timestamp() * 1000)
    end_time = int(pd.Timestamp(end).timestamp() * 1000)

    while True:
        params = {
            "symbol": symbol.upper(),
            "interval": interval,
            "startTime": start_time,
            "endTime": end_time,
            "limit": 1000
        }
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if not data:
            break

        all_data.extend(data)
        last_time = data[-1][0]
        start_time = last_time + 1

        if last_time >= end_time:
            break

        time.sleep(0.3)  # To avoid hitting API rate limits

    df = pd.DataFrame(all_data, columns=[
        "time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base", "taker_buy_quote", "ignore"
    ])
    df = df[["time", "open", "high", "low", "close", "volume"]]
    df["time"] = pd.to_datetime(df["time"], unit='ms')
    df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)

    return df


def get_binance_live(symbol, interval):
    base_url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol.upper(),
        "interval": interval,
        "limit": 100
    }

    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = response.json()

    df = pd.DataFrame(data, columns=[
        "time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base", "taker_buy_quote", "ignore"
    ])

    df = df[["time", "open", "high", "low", "close", "volume"]]
    df["time"] = pd.to_datetime(df["time"], unit='ms')
    df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)

    return df


# ---- Bybit (Public API) ----
def get_bybit_historical(symbol, interval, start, end):
    base_url = "https://api.bybit.com/v5/market/kline"
    interval_map = {"1m": 1, "5m": 5, "15m": 15, "30m": 30, "1h": 60, "4h": 240, "1d": "D"}

    all_data = []
    start_ms = int(pd.Timestamp(start).timestamp() * 1000)
    end_ms = int(pd.Timestamp(end).timestamp() * 1000)

    while True:
        params = {
            "category": "linear",
            "symbol": symbol,
            "interval": str(interval_map[interval]),
            "start": start_ms,
            "end": end_ms,
            "limit": 1000
        }
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()["result"]["list"]

        if not data:
            break

        all_data.extend(data)
        last_time = int(data[-1][0])
        start_ms = last_time + 1

        if last_time >= end_ms:
            break

        time.sleep(0.3)  # Avoid rate limits

    df = pd.DataFrame(all_data, columns=[
        "time", "open", "high", "low", "close", "volume"
    ])

    df["time"] = pd.to_datetime(df["time"], unit='ms')
    df = df.astype({"open": float, "high": float, "low": float, "close": float, "volume": float})

    return df.sort_values("time")


def get_bybit_live(symbol, interval):
    base_url = "https://api.bybit.com/v5/market/kline"
    interval_map = {"1m": 1, "5m": 5, "15m": 15, "30m": 30, "1h": 60, "4h": 240, "1d": "D"}

    params = {
        "category": "linear",
        "symbol": symbol,
        "interval": str(interval_map[interval]),
        "limit": 100
    }

    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = response.json()["result"]["list"]

    df = pd.DataFrame(data, columns=[
        "time", "open", "high", "low", "close", "volume"
    ])

    df["time"] = pd.to_datetime(df["time"], unit='ms')
    df = df.astype({"open": float, "high": float, "low": float, "close": float, "volume": float})

    return df.sort_values("time")