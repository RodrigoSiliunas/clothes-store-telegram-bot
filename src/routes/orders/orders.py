from .utils import get_reply_markup, get_default_message

from telegram import Update
from telegram.ext import CallbackContext

from src.utils.constants import ORDERS, SOLDED_COLLECTION


def main_page(update: Update, callback: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    user = SOLDED_COLLECTION.find_one(
        {'identifier': update.effective_user.id}
    )
    orders = user['types']
    page = user['page']

    # If user don't have any registred orders in database, return a message and do nothing.
    if (len(orders) <= 0):
        callback.bot.send_message(
            'Você não possui nenhum item em seus últimos pedidos.')
        return

    message = get_default_message(
        update.effective_user.id,
        orders[page]['name'],
        orders[page]['quantity'],
        orders[page]['value'],
        orders[page]['weight'],
        page + 1,
        len(orders)
    )
    reply_markup = get_reply_markup()

    query.edit_message_text(
        text=message, reply_markup=reply_markup, parse_mode='Markdown')

    return ORDERS
