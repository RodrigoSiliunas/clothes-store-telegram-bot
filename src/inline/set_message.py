from telegram import Update
from telegram.ext import CallbackContext

from src.utils.constants import COSTUMERS_COLLECTION, STORE

def set_message(update: Update, context: CallbackContext) -> int:
    user = update.effective_user

    COSTUMERS_COLLECTION.update_one(
        { 'identifier': user.id },
        {
            '$set': {
                'inlineMessage': {
                    'id': update.message.message_id,
                    'chatId': update.effective_chat.id,
                    'content': update.message.text
                }
            }
        }, upsert=True
    )

    return STORE