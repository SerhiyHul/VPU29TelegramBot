from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes


async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.contact.user_id
    first_name = update.message.contact.first_name
    last_name = update.message.contact.last_name
    await update.message.reply_text(
        f"""
        user_id = {user_id}
        first_name = {first_name}        
        last_name = {last_name}
        """, reply_markup=ReplyKeyboardRemove())