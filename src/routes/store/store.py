from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update
from telegram.ext import CallbackContext
from src.utils.constants import STORE, COSTUMERS_COLLECTION


def main_page(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    keyboard = [
        [
            InlineKeyboardButton("🔙 Voltar à página inicial",
                                 callback_data='back_to_home'),
            InlineKeyboardButton("🛒 Meu Carrinho",
                                 callback_data="cart_main_page"),
        ],
        [
            InlineKeyboardButton("👥 Verificar CPF's disponíveis",
                                 switch_inline_query_current_chat="display all informations")
        ],
        [
            InlineKeyboardButton("🔍 Buscar por Estado 🇧🇷",
                                 switch_inline_query_current_chat="display states"),
            InlineKeyboardButton("🔍 Buscar por Idade 👴",
                                 switch_inline_query_current_chat="display by age")
        ],
        [
            InlineKeyboardButton("🧚🏻‍♀️ Efetuar Pagamento 💸",
                                 callback_data="open_payment_page"),
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

    message_to_send = f'*{query.from_user.first_name}, você acessou a página:*\n🧛 _Comprar CPF_\n\n' \
        f'Você acessou nossa loja de CPF. Nessa área você ' \
        f'pode selecionar produtos por idade ou estado. Fique a vontade para explorar o ' \
        f'quanto quiser e adicionar produtos ao seu carrinho.\n\n'

    query.edit_message_text(
        text=message_to_send, reply_markup=reply_markup, parse_mode='Markdown')

    return STORE
