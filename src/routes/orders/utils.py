from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_reply_markup() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("⬅️ Anterior",
                                 callback_data="orders_prev_page"),
            InlineKeyboardButton("Próximo ➡️",
                                 callback_data="orders_next_page")
        ],
        [
            InlineKeyboardButton("🔙 Voltar à página inicial",
                                 callback_data='back_to_home')
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


def get_default_message(
        identifier: str, number: str, age: int, state: str,
        price: int | float, page: int, total_pages: int) -> str:

    message = f'👁️‍🗨️ *VOCÊ ESTÁ NO SEUS ÚLTIMOS PEDIDOS!* 👁️‍🗨️\n\n' \
        f'Bem-vindo! Você está nos seus últimos pedidos. Aqui você conseguirá obter as ' \
        f'informações adquiridas sem a censura da pré-venda.\n\n' \
        f'*INFORMAÇÕES SOBRE O ITEM ATUAL*:\n\n' \
        f'*Identifier*: _{identifier}_,\n' \
        f'*Número*: _{number}_,\n' \
        f'*Idade*: _{age}_,\n' \
        f'*UF*: _{state}_,\n\n' \
        f'*VALOR*: _{price}_\n\n' \
        f'*Você está na página*: _{page}/{total_pages}_'

    return message
