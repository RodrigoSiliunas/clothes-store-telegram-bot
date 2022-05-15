from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update
from telegram.ext import CallbackContext
from src.utils.constants import STORE, COSTUMERS_COLLECTION


def main_page(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    keyboard = [
        [
            InlineKeyboardButton("🧥 Roupas Disponíveis",
                                 switch_inline_query_current_chat="display products")
        ],
        [
            InlineKeyboardButton("🔙 Voltar à página inicial",
                                 callback_data='back_to_home'),
            InlineKeyboardButton("🛒 Meu Carrinho",
                                 callback_data="cart_main_page"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

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

    message_to_send = f'*{query.from_user.first_name}, você está na página:*\n👕 _Catálogo_\n\n' \
        f'Você acessou o nosso catálogo. Nessa área você ' \
        f'pode visualizar nossos produtos. Fique a vontade para explorar o ' \
        f'quanto quiser e adicionar items ao seu carrinho.\n\n'

    query.edit_message_text(
        text=message_to_send, reply_markup=reply_markup, parse_mode='Markdown')

    return STORE
