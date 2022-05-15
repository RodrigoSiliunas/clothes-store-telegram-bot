from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from src.utils.constants import STORE
from src.utils.functions import get_database_info


def querys(update: Update, context: CallbackContext) -> int:
    """Handle the inline query displaying all informations."""
    query = update.inline_query.query

    if query == "":
        return

    keyboard = [
        [
            InlineKeyboardButton("🔙 Voltar para loja",
                                 callback_data='delete_inline_message'),
            InlineKeyboardButton("🛒 Adicionar ao Carrinho",
                                 callback_data='add_to_cart')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if query == "display products":
        products = get_database_info(reply_markup)

        update.inline_query.answer(products, cache_time=0)

    return STORE
