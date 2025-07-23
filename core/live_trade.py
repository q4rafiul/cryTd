import os
from dotenv import load_dotenv

# Load keys
load_dotenv("../env/.env")

# Binance
from binance.client import Client as BinanceClient
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")

# Bybit
from pybit.unified_trading import HTTP as BybitClient
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")

# Initialize clients
binance_client = BinanceClient(BINANCE_API_KEY, BINANCE_API_SECRET)
bybit_client = BybitClient(api_key=BYBIT_API_KEY, api_secret=BYBIT_API_SECRET)

def place_order(exchange, symbol, side, quantity, order_type="MARKET"):
    """
    Place a live order on the specified exchange.

    Parameters:
        - exchange: 'binance' or 'bybit'
        - symbol: e.g. 'BTCUSDT'
        - side: 'BUY' or 'SELL'
        - quantity: trade size (float or str)
        - order_type: default is 'MARKET'
    """
    side = side.upper()

    if exchange.lower() == "binance":
        return binance_client.create_order(
            symbol=symbol,
            side=side,
            type=order_type,
            quantity=quantity
        )

    elif exchange.lower() == "bybit":
        return bybit_client.place_order(
            category="linear",
            symbol=symbol,
            side=side,
            orderType=order_type,
            qty=quantity,
            timeInForce="GoodTillCancel"
        )

    else:
        raise ValueError("Unsupported exchange")
