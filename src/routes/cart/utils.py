from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_reply_markup() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("⬅️ Anterior",
                                 callback_data="cart_previous_page"),
            InlineKeyboardButton("🗑️ Descartar",
                                 callback_data="remove_from_cart"),
            InlineKeyboardButton("Próximo ➡️",
                                 callback_data="cart_next_page")
        ],
        [
            InlineKeyboardButton("🔙 Voltar à página inicial",
                                 callback_data='back_to_home'),
            InlineKeyboardButton("🧚🏻‍♀️ Efetuar Pagamento 💸",
                                 callback_data="open_payment_page")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_default_message(
        identifier: str, name: str, quantity: int, weight: int | float, value: int | float,
        page: int, orders_in_bag: int, total_value_of_order: int | float) -> str:

    message = f'🛒 *VOCÊ ESTÁ NO SEU CARRINHO DE COMPRAS!*\n\n' \
        f'Aqui você pode visualizar os items dentro do seu carrinho. ' \
        f'Você também pode excluir um item do seu carrinho se preferir. ' \
        f'Se sua intenção é finalizar o pedido não espere para clicar em _"_*Efetuar* ' \
        f'*Pagamento*_"_.\n\n\n' \
        f'*Informações sobre o item atual:*\n\n' \
        f'*Identifier*: _{identifier}_,\n' \
        f'*Nome*: _{name}_,\n' \
        f'*Quantidade*: _{quantity}_,\n' \
        f'*Peso*: _{weight}_,\n' \
        f'*Preço*: _{value}_\n\n\n' \
        f'✨ Você está na página *{page + 1}* de *{orders_in_bag}*.\n' \
        f'💰 O valor total do seu pedido está em: R$ {total_value_of_order:.2f}'

    return message
