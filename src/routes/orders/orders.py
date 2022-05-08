from .utils import get_reply_markup, get_default_message

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from src.utils.constants import ORDERS, SOLDED_COLLECTION


def main_page(update: Update, callback: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    keyboard = [
        [
            InlineKeyboardButton("🔙 Voltar à página inicial",
                                 callback_data='back_to_home')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message_to_send = f'Mano, não tô entendendo mais nada!!!'
    query.edit_message_text(
        text=message_to_send, reply_markup=reply_markup, parse_mode='Markdown')

    # query = update.callback_query
    # query.answer()

    # print('isso está sendo clicado')

    # user = SOLDED_COLLECTION.find_one(
    #     {'identifier': update.effective_user.id}
    # )
    # orders = user['types']
    # page = user['page']

    # # # If user don't have any registred orders in database, return a message and do nothing.
    # # if (len(orders) < 1):
    # #     print("travou nessa buceta")
    # #     callback.bot.send_message(
    # #         'Você não possui nenhum item em seus últimos pedidos.')
    # #     return

    # message_to_send = get_default_message(
    #     identifier=orders[page]['identifier'],
    #     number=orders[page]['number'],
    #     age=orders[page]['age'],
    #     state=orders[page]['state'],
    #     price=orders[page]['value']

    # )
    # reply_markup = get_reply_markup()

    # query.edit_message_text(
    #     text=message_to_send, reply_markup=reply_markup, parse_mode='Markdown')

    return ORDERS
