import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import threading
import time
import random
import datetime

# Your bot token and chat ID
BOT_TOKEN = "7659946164:AAF0wWg_4Xs66y7x2oIBmNoSx4ZEU43dElE"
CHAT_ID = "@U7774_bot"

bot = telebot.TeleBot(BOT_TOKEN)

# Bot state (ON/OFF)
bot_active = True  
scalping_trades_sent = 0
swing_trades_sent = 0

# Forex and Swing Trading Pairs
FOREX_PAIRS = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD"]
SWING_PAIRS = ["XAU/USD", "BTC/USD", "ETH/USD"]

# Function to check if the forex market is open
def is_forex_market_open():
    now = datetime.datetime.utcnow()
    weekday = now.weekday()
    return weekday not in [5, 6]  # No forex trades on Saturday & Sunday

# Function to check trading session priority
def is_high_probability_session():
    now = datetime.datetime.utcnow()
    hour = now.hour
    return (7 <= hour < 10) or (12 <= hour < 15)  # London & New York session priority

# Function to generate trade signals
def generate_trade(pair, rr):
    entry = round(random.uniform(1.10000, 1.20000), 5)  # Example entry price
    sl = round(entry - (0.0020 * rr), 5)  # Stop-loss placement
    tp = round(entry + (0.0040 * rr), 5)  # Take-profit placement
    return f"📢 Trade Alert:\nPair: {pair}\nEntry: {entry}\n🛑 SL: {sl}\n🎯 TP: {tp}"

# Function to send trades
def send_trades():
    global scalping_trades_sent, swing_trades_sent, bot_active

    while True:
        if bot_active:
            if scalping_trades_sent < 3 and is_forex_market_open():
                pair = random.choice(FOREX_PAIRS)
                trade_msg = generate_trade(pair, rr=2)
                bot.send_message(CHAT_ID, trade_msg)
                scalping_trades_sent += 1

            if swing_trades_sent < 2:
                pair = random.choice(SWING_PAIRS)
                trade_msg = generate_trade(pair, rr=4)
                bot.send_message(CHAT_ID, trade_msg)
                swing_trades_sent += 1

        time.sleep(3600)  # Check every hour

# Function to create the toggle button
def get_toggle_keyboard():
    status = "✅ ON" if bot_active else "❌ OFF"
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(f"Trading Bot: {status}", callback_data="toggle"))
    return markup

# Handle /start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🚀 Trading Bot Started!", reply_markup=get_toggle_keyboard())

# Handle button click (toggle ON/OFF)
@bot.callback_query_handler(func=lambda call: call.data == "toggle")
def toggle_callback(call):
    global bot_active
    bot_active = not bot_active  # Toggle state
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=get_toggle_keyboard())

# Run the bot in a thread
threading.Thread(target=send_trades, daemon=True).start()

print("🚀 Bot is running...")
bot.polling(none_stop=True)
