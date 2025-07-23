from core.trade_utils import buy, sell, save_logs

def run_strategy(data, config):
    logs = []
    capital = config["investment"]
    fee = config["fee"] / 100
    symbol = config["symbol"]
    interval = config["interval"]
    mode = config["mode"]
    exchange = config["exchange"]
    bot_name = config["bot_name"]

    in_position = False
    buy_price = 0
    quantity = 0

    for i in range(20, len(data)):
        row = data.iloc[i]

        if not in_position and ...:
            buy_price = row["close"] * (1 + fee)
            quantity = capital / buy_price
            in_position = True

            buy(exchange, symbol, quantity, buy_price, capital, mode, logs, row["time"], interval, bot_name)

        elif in_position and ...:
            sell_price = row["close"] * (1 - fee)
            profit = (sell_price - buy_price) * quantity
            capital += profit
            in_position = False

            sell(exchange, symbol, quantity, sell_price, profit, capital, mode, logs, row["time"], interval, bot_name)

    if mode == "backtest":
        save_logs(bot_name, symbol, interval, mode, logs)

    return logs