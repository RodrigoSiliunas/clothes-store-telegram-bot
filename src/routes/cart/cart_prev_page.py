from .utils import get_reply_markup, get_default_message
from telegram import Update
from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from src.utils.constants import COSTUMERS_COLLECTION, STORE_COLLECTION, CART


def previous_page(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    reply_markup = get_reply_markup()

    cart = COSTUMERS_COLLECTION.find_one(
        {
            'identifier': update.effective_user.id
        },
        {
            '_id': 0, 'cart': 1
        }
    )

    informartion_user = STORE_COLLECTION.find_one(
        {'identifier': update.effective_user.id}
    )
    page = informartion_user['cart_information'][0]['acctualy_page']
    total_value_of_order = informartion_user['cart_information'][0]['total_value']
    orders_in_bag = informartion_user['cart_information'][0]['total_in_cart']

    # We do not allow the page number to be decremented if it is currently at zero.
    if page <= 0:
        return CART

    # Here we increment the page number by one if the current number is greater than zero.
    if page > 0:
        STORE_COLLECTION.update_one(
            {'identifier': update.effective_user.id},
            {'$set': {'cart_information.0.acctualy_page': page-1}}
        )
        page -= 1

    message_to_send = get_default_message(
        identifier=cart["cart"][page]["_id"],
        number=cart["cart"][page]["number"],
        age=cart["cart"][page]["age"],
        state=cart["cart"][page]["state"],
        balance=cart["cart"][page]["balance"],
        price=cart["cart"][page]["value"],
        page=page,
        orders_in_bag=orders_in_bag,
        total_value_of_order=total_value_of_order
    )

    query.edit_message_text(
        text=message_to_send, reply_markup=reply_markup, parse_mode='Markdown')

    return CART
