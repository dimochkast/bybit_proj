import json
import sqlite3
from datetime import datetime
from urllib.request import urlopen

DB_NAME = 'crypto_prices.db'
TABLE_NAME = 'btc_prices'

API_URL = "https://api.bybit.com/v5/market/tickers"
SYMBOL = "BTCUSDT"


def create_table(conn):
    cursor = conn.cursor()
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            date TEXT NOT NULL,
            price REAL NOT NULL,
            status TEXT NOT NULL
        )
        """
    )
    conn.commit()


def fetch_price():
    params = f"?category=spot&symbol={SYMBOL}"
    with urlopen(API_URL + params) as response:
        data = json.load(response)
    return float(data["result"]["list"][0]["lastPrice"])


def get_last_price(conn):
    cursor = conn.cursor()
    cursor.execute(f"SELECT price FROM {TABLE_NAME} ORDER BY rowid DESC LIMIT 1")
    row = cursor.fetchone()
    return row[0] if row else None


def determine_status(last_price, current_price):
    if last_price is None:
        return "initial"
    return "рост" if current_price > last_price else "падение"


def save_price(conn, price, status):
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO {TABLE_NAME} (date, price, status) VALUES (?, ?, ?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), price, status),
    )
    conn.commit()


def main():
    with sqlite3.connect(DB_NAME) as conn:
        create_table(conn)
        current_price = fetch_price()
        last_price = get_last_price(conn)
        status = determine_status(last_price, current_price)
        save_price(conn, current_price, status)
        print(f"Price: {current_price}, status: {status}")


if __name__ == "__main__":
    main()
