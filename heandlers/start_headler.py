from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, CommandHandler

from heandlers.base_handler import BaseHandler


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton('/hello')],
        [KeyboardButton('Share my location', request_location=True)],
        [KeyboardButton('Share my contact', request_contact=True)]
    ]
    reply_text = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text(f"How can i help you {update.effective_user.first_name}?", reply_markup=reply_text)


class StartHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        app.add_handler(CommandHandler("start", start))
        print('register')

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        keyboard = [
            [KeyboardButton('/hello')],
            [KeyboardButton('Share my location', request_location=True)],
            [KeyboardButton('Share my contact', request_contact=True)]
        ]
        reply_text = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        await update.message.reply_text(f"How can i help you {update.effective_user.first_name}?",
                                        reply_markup=reply_text)