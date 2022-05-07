from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update
from telegram.ext import CallbackContext
from src.utils.constants import ACCOUNT


def main_page(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    keyboard = [
        [
            InlineKeyboardButton("🔙 Voltar à página inicial",
                                 callback_data='back_to_home')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message_to_send = f'👤 *Informações sobre a conta:*\n\n*Nome*: {query.from_user.first_name},\n*ID*: {query.from_user.id}'
    query.edit_message_text(
        text=message_to_send, reply_markup=reply_markup, parse_mode='Markdown')

    return ACCOUNT
