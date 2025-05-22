from telegram.ext import Updater, CommandHandler
import os

# Your bot token here (or set TELEGRAM_TOKEN as an environment variable)
TOKEN = os.getenv("TELEGRAM_TOKEN", "YOUR_TOKEN_HERE")

def start(update, context):
    update.message.reply_text("Hi!")

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))

print("Bot is running...")
updater.start_polling()
updater.idle()
