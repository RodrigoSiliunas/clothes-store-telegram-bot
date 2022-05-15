import re
from bson import ObjectId
from datetime import datetime

from telegram import Update
from telegram.ext import CallbackContext

from src.utils.constants import COSTUMERS_COLLECTION, PRODUCTS_COLLECTION
from src.inline import get_message, delete_message


def add(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    message = get_message(update, context)
    message = message['inlineMessage']

    document_id = re.findall(r'\w{24}', message['content'])[0]

    if document_id is None:
        return

    try:
        # Get PRODUCT information from inline message.
        product = PRODUCTS_COLLECTION.find_one({'_id': ObjectId(document_id)})
        product['inserted_at'] = datetime.now()
    except Exception as e:
        return e

    # Add the document of product to array cart in profile of costumer.
    COSTUMERS_COLLECTION.update_one(
        {
            'identifier': update.effective_user.id
        },
        {
            '$push': {
                'cart': product
            }
        }
    )

    # IF NECESSARY # Remove the product from products collections.
    # PRODUCTS_COLLECTION.delete_one({'_id': ObjectId(document_id)})

    # Return a message to your costumer.
    query.answer(
        text='Você adicionou o produto ao seu carrinho de compras.', show_alert=True)

    # Delete inline message and remove message from DB.
    delete_message(update, context)

    COSTUMERS_COLLECTION.update_one(
        {'identifier': update.effective_user.id},
        {
            '$unset': {
                'inlineMessage': True
            }
        }
    )

    return None
