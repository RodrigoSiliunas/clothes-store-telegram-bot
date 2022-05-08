from .utils import get_reply_markup, get_default_message

from telegram import Update
from telegram.ext import CallbackContext

from src.utils.constants import ORDERS, SOLDED_COLLECTION


def main_page(update: Update, callback: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    print('isso está sendo clicado')

    user = SOLDED_COLLECTION.find_one(
        {'identifier': update.effective_user.id}
    )
    orders = user['types']

    # If user don't have any registred orders in database, return a message and do nothing.
    if (len(orders) < 1):
        print("travou nessa buceta")
        callback.bot.send_message(
            'Você não possui nenhum item em seus últimos pedidos.')
        return

    page = user['page']

    reply_markup = get_reply_markup()
    message = get_default_message(
        identifier=orders[page]['identifier'],
        number=orders[page]['number'],
        age=orders[page]['age'],
        state=orders[page]['state'],
        price=orders[page]['value']

    )
    

    query.edit_message_text(
        text=message, reply_markup=reply_markup, parse_mode='Markdown')

    return ORDERS