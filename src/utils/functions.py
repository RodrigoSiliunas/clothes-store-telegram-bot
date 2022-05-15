from time import sleep

from datetime import datetime, timedelta
from bson import ObjectId

from telegram import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardMarkup,
    ParseMode,
    Update
)
from telegram.ext import CallbackContext

from src.utils.constants import (
    PRODUCTS_COLLECTION,
    COSTUMERS_COLLECTION,
    SOLDED_COLLECTION,
    STORE_COLLECTION
)


def get_database_info(reply_markup: InlineKeyboardMarkup) -> list:
    products_arr = []

    collection = PRODUCTS_COLLECTION.find()

    for product in collection:
        description = f'{product["quantity"]}x {product["name"]} | Por apenas: R${product["value"]:.2f}'
        input_message_content = f'*Informação Detalhada:*\n\n' \
                                f'🔒 *Identify*: _{product["_id"]}_,\n' \
                                f'👖 *Nome*: _{product["name"]}_,\n' \
                                f'🔢 *Quantidade*: _{product["quantity"]}_,\n' \
                                f'💰 *Peso*: _{product["weight"]}_,\n\n' \
                                f'💸 *Preço*: R$_{product["value"]:.2f}_'

        products_arr.append(
            InlineQueryResultArticle(
                id=str(product['_id']),
                title=product['name'],
                description=description,
                input_message_content=InputTextMessageContent(
                    input_message_content,
                    parse_mode=ParseMode.MARKDOWN
                ),
                reply_markup=reply_markup
            )
        )

    return products_arr


def delete_message(update: Update, context: CallbackContext) -> None:
    update.effective_message.delete()


def remove_unfinished_order() -> None:
    while True:
        print(f'🔍 Estamos verificando se não há nenhum produto esquecido nos carrinhos de compras.')
        costumers = COSTUMERS_COLLECTION.find()

        for costumer in costumers:
            if costumer['cart']:

                for item in costumer['cart']:
                    acctualy_date = item['inserted_at'] + timedelta(seconds=40)

                    if datetime.now() >= acctualy_date:
                        # Here we remove the page information from the user's cart.
                        # We also removed the null that is left when removing an array item in MongoDB.
                        COSTUMERS_COLLECTION.update_one(
                            {'identifier': costumer['identifier']},
                            {
                                '$pull': {
                                    'cart': {
                                        '_id': ObjectId(item['_id'])
                                    }
                                }
                            }
                        )
        sleep(10 * 60)  # Every ten minutes this code will execute.


def transfer_paid_items(transaction_id: str) -> None:
    user_identifier = STORE_COLLECTION.find_one(
        {
            'transaction_id': transaction_id
        }
    )
    user_identifier = user_identifier['identifier']

    user = COSTUMERS_COLLECTION.find_one(
        {
            'identifier': user_identifier
        }
    )

    SOLDED_COLLECTION.update_one(
        {
            'identifier': user_identifier,
        },
        {
            '$set': {
                'page': 0
            },
            '$addToSet': {
                'types': {
                    '$each': user['cart']
                }
            }
        },
        upsert=True
    )

    COSTUMERS_COLLECTION.update_one(
        {
            'identifier': user_identifier
        },
        {
            '$set': {
                'cart': []
            }
        }
    )
