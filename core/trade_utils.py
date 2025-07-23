import os
import json
from core.live_trade import place_order

def get_log_filename(bot_name, symbol, interval, mode):
    return f"performance/{bot_name}_{symbol}_{interval}_{mode}.json"

def buy(exchange, symbol, quantity, price, capital, mode, logs, row_time, interval, bot_name):
    if mode == "live":
        place_order(exchange, symbol, side="BUY", quantity=quantity)

    log_entry = {
        "action": "BUY",
        "price": round(price, 2),
        "quantity": round(quantity, 6),
        "capital": round(capital, 2),
        "time": str(row_time)
    }
    logs.append(log_entry)

    if mode in ["live", "paper"]:
        save_logs(bot_name, symbol, interval, mode, logs)

def sell(exchange, symbol, quantity, price, profit, capital, mode, logs, row_time, interval, bot_name):
    if mode == "live":
        place_order(exchange, symbol, side="SELL", quantity=quantity)

    log_entry = {
        "action": "SELL",
        "price": round(price, 2),
        "quantity": round(quantity, 6),
        "profit": round(profit, 2),
        "capital": round(capital, 2),
        "time": str(row_time)
    }
    logs.append(log_entry)

    if mode in ["live", "paper"]:
        save_logs(bot_name, symbol, interval, mode, logs)

def save_logs(bot_name, symbol, interval, mode, logs):
    filename = get_log_filename(bot_name, symbol, interval, mode)
    os.makedirs("performance", exist_ok=True)
    with open(filename, "w") as f:
        json.dump(logs, f, indent=2)
