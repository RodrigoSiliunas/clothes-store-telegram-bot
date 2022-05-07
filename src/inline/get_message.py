from pymongo.collection import Collection

from telegram import Update
from telegram.ext import CallbackContext

from src.utils.constants import COSTUMERS_COLLECTION


def get_message(update: Update, context: CallbackContext) -> Collection:
    user = update.effective_user

    query = COSTUMERS_COLLECTION.find_one(
        {'identifier': user.id},
        {'_id': False, 'inlineMessage': True}
    )

    return query
