from .utils import get_reply_markup, get_default_message
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update
from telegram.ext import CallbackContext
from src.utils.constants import CART, COSTUMERS_COLLECTION, STORE_COLLECTION


def main_page(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    cart = COSTUMERS_COLLECTION.find_one(
        {
            'identifier': update.effective_user.id
        },
        {
            '_id': 0, 'cart': 1
        }
    )

    # If can't find any product inside bag.
    if not cart["cart"]:
        context.bot.send_message(
            text='Você não possui nenhum item em seu carrinho de compras.',
            chat_id=update.effective_chat.id
        )
        return

    # Here we do a aggregate and then save/update it on store collections to after finds and updates.
    COSTUMERS_COLLECTION.aggregate([
        {
            '$match': {
                'identifier': update.effective_user.id
            }
        }, {
            '$project': {
                'identifier': 1,
                'nickname': 1,
                'cart_information': [
                    {
                        'total_value': {
                            '$sum': '$cart.value'
                        },
                        'total_in_cart': {
                            '$size': '$cart'
                        },
                        'acctualy_page': 0
                    }
                ]
            }
        }, {
            '$out': 'store'
        }
    ])

    informartion_user = STORE_COLLECTION.find_one(
        {'identifier': update.effective_user.id}
    )
    page = informartion_user['cart_information'][0]['acctualy_page']
    total_value_of_order = informartion_user['cart_information'][0]['total_value']
    orders_in_bag = informartion_user['cart_information'][0]['total_in_cart']

    reply_markup = get_reply_markup()

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
