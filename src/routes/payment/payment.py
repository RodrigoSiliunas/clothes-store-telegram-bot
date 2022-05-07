from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update
from telegram.ext import CallbackContext
from src.utils.constants import PAYMENT, STORE_COLLECTION


def main_page(update: Update, callback: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    user_data = STORE_COLLECTION.find_one(
        {'identifier': update.effective_user.id}
    )
    user_data = user_data['cart_information'][0]

    total_value_of_order = user_data['total_value']
    orders_in_bag = user_data['total_in_cart']

    keyboard = [
        [
            InlineKeyboardButton('🔙 Voltar à página inicial',
                                 callback_data='back_to_home'),
            InlineKeyboardButton('🗑️ Descartar Pedido',
                                 callback_data='back_to_home'),
        ],
        [
            InlineKeyboardButton('❖ Efetuar Pix',
                                 callback_data='create_pix_request'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message_to_send = f'❖ *VOCÊ ESTÁ NA ÁREA DE PAGAMENTOS PIX!*\n\n' \
                      f'Você tem um total de *{orders_in_bag}* itens em seu carrinho de compras.\n' \
                      f'O valor total a ser pago é de *R$*_{total_value_of_order:.2f}_\n\n' \
                      f'✓ SELECIONE A SUA OPÇÃO ABAIXO: '

    query.edit_message_text(
        text=message_to_send, reply_markup=reply_markup, parse_mode='Markdown')

    return PAYMENT
