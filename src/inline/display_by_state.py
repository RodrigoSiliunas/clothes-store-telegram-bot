from . import get_message, delete_message, set_message

from telegram.ext import CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from src.utils.constants import STORE


def display_by_state(update: Update, context: CallbackContext) -> int:
    set_message(update, context)

    message = get_message(update, context)
    message = message['inlineMessage']

    delete_message(update, context)

    state_uf = message['content'].split()[1]

    keyboard = [
        [
            InlineKeyboardButton(
                "🔙 Voltar para Loja | Alterar Estado", callback_data="delete_message"),
            InlineKeyboardButton(
                "👤 Exibir Lista de CPF",
                switch_inline_query_current_chat=f"display by state {state_uf}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message_to_user = f'*Você selecionou o estado de*: _{state_uf}_\n\n' \
                      f'Você poderá ver aqui uma lista com diversos números de CPF ' \
                      f'pertencentes a esse estado. Caso tenha alguma dúvida não hesite em contatar nosso canal de suporte.\n\n' \
                      f'*Selecione uma das opções abaixo:*'

    context.bot.send_message(
        text=message_to_user, reply_markup=reply_markup, chat_id=message['chatId'], parse_mode='Markdown')

    return STORE
