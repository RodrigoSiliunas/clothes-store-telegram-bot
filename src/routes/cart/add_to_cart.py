import re
from bson import ObjectId
from datetime import datetime

from telegram import Update
from telegram.ext import CallbackContext

from src.utils.constants import COSTUMERS_COLLECTION, CPF_COLLECTION
from src.inline import get_message, delete_message


def add(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    message = get_message(update, context)
    message = message['inlineMessage']

    document_id = re.findall(r'\w{24}', message['content'])[0]

    if document_id is None:
        return

    try:
        # Get CPF information from inline message.
        cpf = CPF_COLLECTION.find_one({'_id': ObjectId(document_id)})
        cpf['inserted_at'] = datetime.now()
    except Exception as e:
        return e

    # Add the document CPF to array cart in profile of costumer.
    COSTUMERS_COLLECTION.update_one(
        {'identifier': update.effective_user.id},
        {
            '$push': {
                'cart': cpf
            }
        }
    )

    # Remove the CPF from CPF collections.
    CPF_COLLECTION.delete_one({'_id': ObjectId(document_id)})

    # Return a message to your costumer.
    query.answer(
        text='Você adicionou a informação ao seu carrinho de compras. A página da loja não é atualizada dinamicamente, se houver dúvida pode verificar seu carrinho de compras.', show_alert=True)

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
