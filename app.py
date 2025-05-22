import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

DATA_FILE = "data/tasks.json"

# اگر فایل json وجود نداره، بساز
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

# اضافه کردن تسک
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)
    if not text:
        await update.message.reply_text("❗️ لطفاً متن تسک رو وارد کن.")
        return
    with open(DATA_FILE, "r+") as f:
        tasks = json.load(f)
        tasks.append({"task": text})
        f.seek(0)
        json.dump(tasks, f, indent=2)
    await update.message.reply_text(f"✅ تسک اضافه شد: {text}")

# نمایش لیست تسک‌ها
async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open(DATA_FILE, "r") as f:
        tasks = json.load(f)
    if not tasks:
        await update.message.reply_text("📭 لیست تسک‌ها خالیه.")
        return
    message = "\n".join([f"{i+1}. {t['task']}" for i, t in enumerate(tasks)])
    await update.message.reply_text("📝 لیست تسک‌ها:\n" + message)

# حذف تسک
async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        index = int(context.args[0]) - 1
    except:
        await update.message.reply_text("❗️ لطفاً شماره تسک رو وارد کن.")
        return
    with open(DATA_FILE, "r+") as f:
        tasks = json.load(f)
        if 0 <= index < len(tasks):
            removed = tasks.pop(index)
            f.seek(0)
            f.truncate()
            json.dump(tasks, f, indent=2)
            await update.message.reply_text(f"🗑 حذف شد: {removed['task']}")
        else:
            await update.message.reply_text("❗️ شماره معتبر نیست.")

# استارت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! 👋 این بات برای مدیریت تسک‌هاست.\nدستورها:\n/add [تسک]\n/list\n/delete [شماره]")

# راه‌اندازی برنامه
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("list", list_tasks))
app.add_handler(CommandHandler("delete", delete))

print("Bot is running...")
app.run_polling()
