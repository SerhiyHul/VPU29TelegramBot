import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

from config.config import TELEGRAM_TOKEN
from heandlers.hello_heandler import hello
from heandlers.start_headler import start
from heandlers.location_heandler import location

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text.lower()
    last_name = update.effective_user.last_name

    if "hello" in message:
        if last_name:
            await update.message.reply_text(f"Здоров {update.effective_user.first_name} {update.effective_user.last_name}")
        else:
            await update.message.reply_text(f"Здоров {update.effective_user.first_name}")

    elif "bye" in message:
        if last_name:
            await update.message.reply_text(f"Goodbye {update.effective_user.first_name} {update.effective_user.last_name}")
        else:
            await update.message.reply_text(f"Goodbye {update.effective_user.first_name}")

    else:
        await update.message.reply_text(f"I don't know how to read this")

from heandlers.contact_heandler import contact


app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("hello", hello))
location_handler = MessageHandler(filters.LOCATION, location)
app.add_handler(location_handler)
contact_handler = MessageHandler(filters.CONTACT, contact)
app.add_handler(contact_handler)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
app.run_polling()