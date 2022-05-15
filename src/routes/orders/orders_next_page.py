from .utils import get_reply_markup, get_default_message

from telegram import Update
from telegram.ext import CallbackContext

from src.utils.constants import ORDERS, SOLDED_COLLECTION


def next_page(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    user = SOLDED_COLLECTION.find_one(
        {
            'identifier': update.effective_user.id
        }
    )

    page = user['page']
    orders = user['types']

    # Number of page is higher or equal than number of orders.
    if (page) >= (len(orders) - 1):
        return

    # We increment the current page number by one in the database.
    page += 1
    SOLDED_COLLECTION.update_one(
        {
            'identifier': update.effective_user.id
        },
        {
            '$set': {
                'page': page
            }
        }
    )

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
