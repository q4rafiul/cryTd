import pandas_ta as ta

def run_strategy(data, config):
    logs = []
    capital = config["investment"]
    fee = config["fee"] / 100
    symbol = config["symbol"]
    interval = config["interval"]

    # Apply indicators needed for this bot
    data["sma_fast"] = ta.sma(data["close"], length=10)
    data["sma_slow"] = ta.sma(data["close"], length=25)
    macd = ta.macd(data["close"])
    data["macd"] = macd["MACD_12_26_9"]
    data["macd_signal"] = macd["MACDs_12_26_9"]

    in_position = False
    buy_price = 0
    quantity = 0

    for i in range(25, len(data)):
        row = data.iloc[i]

        # Entry condition
        if not in_position and row["sma_fast"] > row["sma_slow"] and row["macd"] > row["macd_signal"]:
            buy_price = row["close"] * (1 + fee)
            quantity = capital / buy_price
            in_position = True

            logs.append({
                "action": "BUY",
                "price": round(buy_price, 2),
                "quantity": round(quantity, 6),
                "time": str(row["time"])
            })

        # Exit condition
        elif in_position and row["macd"] < row["macd_signal"]:
            sell_price = row["close"] * (1 - fee)
            profit = (sell_price - buy_price) * quantity
            capital += profit
            in_position = False

            logs.append({
                "action": "SELL",
                "price": round(sell_price, 2),
                "quantity": round(quantity, 6),
                "profit": round(profit, 2),
                "capital": round(capital, 2),
                "time": str(row["time"])
            })

    return logs
