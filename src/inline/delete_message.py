from telegram import Update
from telegram.ext import CallbackContext

from src.utils.constants import COSTUMERS_COLLECTION, STORE


def delete_message(update: Update, context: CallbackContext) -> int:
    user = update.effective_user

    message = COSTUMERS_COLLECTION.find_one(
        { 'identifier': user.id },
        {'_id': False, 'inlineMessage': True }
    )
    message = message['inlineMessage']

    COSTUMERS_COLLECTION.update_one(
        { 'identifier': user.id },
        {
            '$unset': {
                'inlineMessage': True
            }
        }
    )

    context.bot.delete_message(chat_id=message['chatId'], message_id=message['id'])

    return STORE