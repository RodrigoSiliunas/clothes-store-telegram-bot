from .utils import get_reply_markup, get_default_message

from telegram import Update
from telegram.ext import CallbackContext

from src.utils.constants import ORDERS, SOLDED_COLLECTION


def previous_page(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    user = SOLDED_COLLECTION.find_one(
        {
            'identifier': update.effective_user.id
        }
    )

    page = user['page']
    orders = user['types']

    # Number of page is lower than zero.
    if (page) <= 0:
        return

    # We decrement the current page number by one in the database.
    page -= 1
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
        orders[page]['number'],
        orders[page]['age'],
        orders[page]['state'],
        orders[page]['value'],
        page + 1,
        len(orders)
    )
    reply_markup = get_reply_markup()

    query.edit_message_text(
        text=message, reply_markup=reply_markup, parse_mode='Markdown')

    return ORDERS
