from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from src.utils.constants import COSTUMERS_COLLECTION, HOME


def start(update: Update, context: CallbackContext) -> int:
    """Send a message when the command /start is issued."""
    user = update.effective_user

    # Upsert to collect userdata from costumers.
    COSTUMERS_COLLECTION.update_one(
        {'identifier': user.id},
        {
            '$set': {
                'last_interact_with_bot': datetime.now()
            },

            '$setOnInsert': {
                'nickname': user.full_name,
                'identifier': user.id,
                'money_total_spend': 0,
                'total_info_buyed': 0,
                'cart': []
            }
        },
        upsert=True
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

    keyboard = [
        [
            InlineKeyboardButton(
                "👕 Acessar Loja", callback_data="open_store_information"),
            InlineKeyboardButton(
                "👤 Usuário", callback_data="user_information")
        ],
        [
            InlineKeyboardButton("🛒 Meu Carrinho",
                                 callback_data="cart_main_page"),
            InlineKeyboardButton("💸 Meus Pedidos",
                                 callback_data="orders_main_page")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message_to_send = f'*Bem-vindo, {user.first_name}!*\n\n' \
        'Você acaba de acessar a *Clothes Store*. Procurando por roupas para ' \
        'revenda? Te convidamos a interagir com o nosso atendente virtual e a conhecer nossos ' \
        'produtos. Trabalhamos com as melhores marcas e com um ótimo preço.\n\n' \
        '[🤖 Suporte](https://t.me/+sMv1RgwuHqk1MTMx)'

    update.message.reply_text(text=message_to_send,
                              parse_mode='Markdown', reply_markup=reply_markup)

    return HOME
