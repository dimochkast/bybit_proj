import requests
import datetime

# Список криптовалютных пар, которые хотим отслеживать
symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]

# URL для публичного API Bybit (спот-рынок)
url = "https://api.bybit.com/v5/market/tickers"

def get_prices(symbols):
    prices = {}
    for symbol in symbols:
        params = {"category": "spot", "symbol": symbol}
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            # Вытаскиваем последнюю цену
            last_price = data["result"]["list"][0]["lastPrice"]
            prices[symbol] = last_price
        except Exception as e:
            prices[symbol] = f"Ошибка: {e}"
    return prices

def save_to_file(prices, filename="crypto_prices.txt"):
    with open(filename, "a", encoding="utf-8") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"\n=== {timestamp} ===\n")
        for symbol, price in prices.items():
            f.write(f"{symbol}: {price}\n")

if __name__ == "__main__":
    prices = get_prices(symbols)
    save_to_file(prices)
    print("Данные сохранены в crypto_prices.txt")
