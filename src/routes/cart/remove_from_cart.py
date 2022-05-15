
from telegram import Update
from telegram.ext import CallbackContext
from .utils import get_reply_markup, get_default_message
from src.utils.constants import CART, COSTUMERS_COLLECTION, STORE_COLLECTION


def remove(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    reply_markup = get_reply_markup()

    informartion_user = STORE_COLLECTION.find_one(
        {'identifier': update.effective_user.id}
    )

    page = informartion_user['cart_information'][0]['acctualy_page']
    total_value_of_order = informartion_user['cart_information'][0]['total_value']
    orders_in_bag = informartion_user['cart_information'][0]['total_in_cart']

    if orders_in_bag <= 0:
        return

    cart = COSTUMERS_COLLECTION.find_one(
        {
            'identifier': update.effective_user.id
        },
        {
            '_id': 0, 'cart': 1
        }
    )

    # Here we remove the page information from the user's cart.
    # We also removed the null that is left when removing an array item in MongoDB.
    COSTUMERS_COLLECTION.update_one(
        {'identifier': update.effective_user.id},
        {
            '$unset': {
                f'cart.{page}': 1
            }
        }
    )
    COSTUMERS_COLLECTION.update_one(
        {'identifier': update.effective_user.id},
        {
            '$pull': {
                'cart': None
            }
        }
    )

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

    if orders_in_bag <= 0:
        message_to_send = f'🛒 *VOCÊ ESTÁ NO SEU CARRINHO DE COMPRAS!*\n\n' \
            f'Aqui você pode verificar informações sobre seu último pedido. ' \
            f'Você também pode excluir um item do seu carrinho se preferir. ' \
            f'Se sua intenção é finalizar o pedido não espere para clicar em _"_*Efetuar* ' \
            f'*Pagamento*_"_.\n\n\n' \
            f'*Informações sobre o item atual:*\n\n' \
            f'Você não possui mais informações no carrinho de compras.\n' \

        query.edit_message_text(
            text=message_to_send, reply_markup=reply_markup, parse_mode='Markdown')

        return CART

    message_to_send = get_default_message(
        identifier=cart["cart"][page]["_id"],
        name=cart["cart"][page]["name"],
        quantity=cart["cart"][page]["quantity"],
        weight=cart["cart"][page]["weight"],
        value=cart["cart"][page]["value"],

        page=page,
        orders_in_bag=orders_in_bag,
        total_value_of_order=total_value_of_order
    )

    query.edit_message_text(
        text=message_to_send, reply_markup=reply_markup, parse_mode='Markdown')

    return CART