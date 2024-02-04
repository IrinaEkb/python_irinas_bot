from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import requests

TOKEN = "6749742797:AAEvGwdGHRXt3KuJur65oUBASQVaFHauOs4"


CRYPTO_NAME_TO_TICKER = {
    "Bitcoin": "BTC-USD",
    "Ethereum": "ETH-USD",
    "Doge": "DOGE-USD",
    "Solana": "SOL-USD",
    "Chainlink": "LINK-USD",
    "Pi": "PI-USD"
}


bot = TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=False)
    for crypto_name in CRYPTO_NAME_TO_TICKER.keys():
        item_button = KeyboardButton(crypto_name)
        markup.add(item_button)
    bot.send_message(message.chat.id, "Choose a crypto", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in CRYPTO_NAME_TO_TICKER.keys())
def send_price(message):
    crypto_name = message.text
    ticker = CRYPTO_NAME_TO_TICKER[crypto_name]
    price = get_price_by_ticker(ticker=ticker)
    bot.send_message(message.chat.id, f"Price of {crypto_name} to USDT is {price}")


def get_price_by_ticker(*, ticker: str) -> float:
    # Adjust the ticker format for Coinbase Pro
    # Example: Convert "BTCUSDT" to "BTC-USD"
    ticker = ticker.replace("USDT", "-USD")

    # Coinbase Pro API endpoint for the current price of a cryptocurrency
    endpoint = f"https://api.pro.coinbase.com/products/{ticker}/ticker"

    response = requests.get(endpoint)
    data = response.json()

    # Check if 'price' key exists in the response
    if 'price' in data:
        # If 'price' key exists, proceed to round and return the price
        price = round(float(data["price"]), 2)
        return price
    else:
        # If 'price' key does not exist, print a helpful message for debugging
        print(f"No price found for {ticker}. Response: {data}")
        return 0.0  # Or handle this case as appropriate for your application

bot.infinity_polling()