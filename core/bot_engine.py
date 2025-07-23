import importlib
import json
import os
from core.data_provider import fetch_data


def load_config(config_path="config/bots.json"):
    with open(config_path, "r") as f:
        return json.load(f)


def run_bots():
    config = load_config()

    exchange = config["exchange"]
    symbol = config["symbol"]
    intervals = config["intervals"]
    start = config["start"]
    end = config["end"]
    mode = config["mode"]
    investment = config["investment"]
    fee = config["fee"]
    bots = config["bots"]

    performance_dir = "performance"
    os.makedirs(performance_dir, exist_ok=True)

    for bot_name in bots:
        print(f"\n🤖 Running bot: {bot_name}...")
        bot_module = importlib.import_module(f"bots.{bot_name}")

        for interval in intervals:
            print(f"⏱️  Interval: {interval}")
            df = fetch_data(exchange, symbol, interval, start, end, mode=mode)

            # Create a unique config for this run
            run_config = {
                "bot_name": bot_name,
                "exchange": exchange,
                "symbol": symbol,
                "interval": interval,
                "mode": mode,
                "investment": investment,
                "fee": fee
            }

            trade_logs = bot_module.run_strategy(df.copy(), run_config)

            filename = f"{bot_name}_{interval}.json"
            filepath = os.path.join(performance_dir, filename)

            with open(filepath, "w") as f:
                json.dump(trade_logs, f, indent=2)

            print(f"✅ Logs saved to {filepath}")


if __name__ == "__main__":
    run_bots()