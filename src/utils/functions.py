from uuid import uuid4
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
    CPF_COLLECTION,
    COSTUMERS_COLLECTION,
    SOLDED_COLLECTION,
    STORE_COLLECTION
)


def encode_cpf(cpf: str) -> str:
    cpf = list(cpf)

    for i in range(4, 11):
        if i != 7:
            cpf[i] = 'X'

    return "".join(cpf)


def get_all_state_info() -> list:
    state_list = [
        {'Acre': 'AC'}, {'Alagoas': 'AL'}, {'Amapá': 'AP'}, {'Amazonas': 'AM'},
        {'Bahia': 'BA'}, {'Ceará': 'CE'}, {
            'Distrito Federal': 'DF'}, {'Espírito Santo': 'ES'},
        {'Goiás': 'GO'}, {'Maranhão': 'MA'}, {
            'Mato Grosso': 'MT'}, {'Mato Grosso do Sul': 'MS'},
        {'Minas Gerais': 'MG'}, {'Pará': 'PA'}, {
            'Paraíba': 'PB'}, {'Paraná': 'PR'},
        {'Pernambuco': 'PE'}, {'Piauí': 'PI'}, {
            'Rio de Janeiro': 'RJ'}, {'Rio Grande do Norte': 'RN'},
        {'Rio Grande do Sul': 'RS'}, {'Rondônia': 'RO'}, {
            'Roraima': 'RR'}, {'Santa Catarina': 'RS'},
        {'São Paulo': 'SP'}, {'Sergipe': 'SE'}, {'Tocantins': 'TO'}
    ]

    answer_state = []

    for state in state_list:
        for key, value in state.items():
            answer_state.append(
                InlineQueryResultArticle(
                    id=uuid4(),
                    title=value,
                    description=key,
                    input_message_content=InputTextMessageContent(
                        f'Ø {value}',
                        parse_mode=ParseMode.MARKDOWN
                    ),
                )
            )

    return answer_state


def get_database_info(reply_markup: InlineKeyboardMarkup, state: str = None, age: int = None) -> list:
    cpf_list = []

    if state is not None:
        collection = CPF_COLLECTION.find({'state': state})
    elif age is not None:
        collection = CPF_COLLECTION.find({'age': age})
    else:
        collection = CPF_COLLECTION.find()

    for cpf in collection:
        description = f'{cpf["age"]} | {cpf["state"]} | Saldo: {cpf["balance"]} | R$ {cpf["value"]}'
        input_message_content = f'*Informação Detalhada:*\n\n' \
                                f'🔒 *Identify*: _{cpf["_id"]}_,\n' \
                                f'🔢 *Número*: _{encode_cpf(cpf["number"])}_,\n' \
                                f'👴 *Idade*: _{cpf["age"]}_,\n' \
                                f'💰 *Saldo Disponível*: _{cpf["balance"]}_,\n\n' \
                                f'💸 *Preço da Informação*: _{cpf["value"]}_'

        cpf_list.append(
            InlineQueryResultArticle(
                id=str(cpf['_id']),
                title=encode_cpf(cpf['number']),
                description=description,
                input_message_content=InputTextMessageContent(
                    input_message_content,
                    parse_mode=ParseMode.MARKDOWN
                ),
                reply_markup=reply_markup
            )
        )

    return cpf_list


def delete_message(update: Update, context: CallbackContext) -> None:
    update.effective_message.delete()


def remove_unfinished_order() -> None:
    while True:
        print(f'🔍 Estamos verificando se não há nenhum CPF esquecido nos carrinhos de compras.')
        costumers = COSTUMERS_COLLECTION.find()

        for costumer in costumers:
            if costumer['cart']:

                for item in costumer['cart']:
                    acctualy_date = item['inserted_at'] + timedelta(seconds=40)

                    if datetime.now() >= acctualy_date:
                        del item['inserted_at']

                        CPF_COLLECTION.insert_one(item)

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
            'identifier': user_identifier
        },
        {
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
