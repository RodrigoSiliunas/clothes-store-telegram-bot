from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from src.utils.constants import STORE
from src.utils.functions import get_all_state_info, get_database_info


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

    if query == "display all informations":
        cpf_list = get_database_info(reply_markup)

        update.inline_query.answer(cpf_list, cache_time=0)

    if query == "display states":
        states = get_all_state_info()

        update.inline_query.answer(states, cache_time=0)

    if "display by state" in query:
        try:
            uf = query.split()[3]
        except:
            return STORE
        cpf_list = get_database_info(reply_markup, uf)

        update.inline_query.answer(cpf_list, cache_time=0)

    if ("display by age" in query):
        query = update.inline_query.query

        if (len(query) >= 17):
            age = query.split()[3]
            cpf_list = get_database_info(reply_markup, age=int(age))

            update.inline_query.answer(cpf_list, cache_time=0)

    return STORE
