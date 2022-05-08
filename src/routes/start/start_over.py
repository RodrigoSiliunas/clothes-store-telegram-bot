from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update
from telegram.ext import CallbackContext
from src.utils.constants import HOME


def over(update: Update, context: CallbackContext) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    query = update.callback_query
    query.answer()

    keyboard = [
        [
            InlineKeyboardButton(
                "🧛 Comprar CPF", callback_data="open_store_information"),
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
    message_to_send = f'*Bem-vindo, {query.from_user.first_name}!*\n\n' \
        'Você acaba de acessar a _loja do Fuinha_. Necessitando de informação para ' \
        'algum serviço? Sinta-se livre para se registrar e explorar nossos produtos.\n\n' \
        '[🤖 Suporte](https://t.me/empiresuporte3)'

    query.edit_message_text(text=message_to_send,
                            parse_mode='Markdown', reply_markup=reply_markup)

    return HOME
