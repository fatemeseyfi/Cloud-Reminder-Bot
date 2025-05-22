from telegram.ext import Updater, CommandHandler
import json, os

TOKEN = os.getenv("TELEGRAM_TOKEN")
DATA_FILE = "data/tasks.json"

# Create tasks file if it doesn't exist
if not os.path.exists(DATA_FILE):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

def add(update, context):
    text = " ".join(context.args)
    if not text:
        update.message.reply_text("Please provide a task description.")
        return
    with open(DATA_FILE, "r+") as f:
        tasks = json.load(f)
        tasks.append({"task": text})
        f.seek(0)
        json.dump(tasks, f, indent=2)
    update.message.reply_text("Task added:".format(text))

def list_tasks(update, context):
    with open(DATA_FILE, "r") as f:
        tasks = json.load(f)
    if not tasks:
        update.message.reply_text("No tasks found.")
        return
    message = "\n".join([f"{i+1}. {t['task']}" for i, t in enumerate(tasks)])
    update.message.reply_text("Task list:\n" + message)

def delete(update, context):
    try:
        index = int(context.args[0]) - 1
    except:
        update.message.reply_text("❗️ Please provide a valid task number.")
        return
    with open(DATA_FILE, "r+") as f:
        tasks = json.load(f)
        if 0 <= index < len(tasks):
            removed = tasks.pop(index)
            f.seek(0)
            f.truncate()
            json.dump(tasks, f, indent=2)
            update.message.reply_text(f"🗑 Deleted: {removed['task']}")
        else:
            update.message.reply_text("❗️ Invalid task number.")

def start(update, context):
    update.message.reply_text(
        "👋 Welcome! This bot helps you manage tasks.\n\n"
        "Available commands:\n"
        "/add [task description] - Add a new task\n"
        "/list - Show all tasks\n"
        "/delete [number] - Delete a task"
    )

updater = Updater(TOKEN)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("add", add))
dp.add_handler(CommandHandler("list", list_tasks))
dp.add_handler(CommandHandler("delete", delete))

print("Bot is running...")
updater.start_polling()
updater.idle()
