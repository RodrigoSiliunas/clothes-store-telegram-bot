from uuid import uuid4

from telegram import Update
from telegram.ext import CallbackContext

from src.utils.constants import PAYMENT, STORE_COLLECTION, PIX


def create_pix_request(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    try:
        STORE_COLLECTION.update_one(
            {'identifier': update.effective_user.id},
            {
                '$set': {
                    'transaction_id': str(uuid4())
                }
            }
        )

        user_data = STORE_COLLECTION.find_one(
            {'identifier': update.effective_user.id}
        )
        cart_info = user_data['cart_information'][0]
    except:
        return PAYMENT

    transaction_id = user_data['transaction_id']
    total_value_of_order = cart_info['total_value']

    # Create a request with Pix
    pix_request = PIX.create_payment_request(
        int(total_value_of_order), transaction_id)

    if pix_request.status_code != 200:
        return PAYMENT

    pix_request = pix_request.json()

    qr_code = pix_request['charge']['qrCodeImage']
    br_code = pix_request['brCode']

    message = f'![qrCode]({qr_code})\n\n' \
              f'⚠️ *ATENÇÃO*:\n\n' \
              f'Esse é o QRCode do seu pedido. Se certifique de *NÃO PAGAR* de nenhum modo se acabarem se passando *vinte minutos* depois da mensagem. Você perderá o dinheiro caso você ' \
              f'faça isso.\n\nAtenção também no seu carrinho de compras, não deixe itens lá por ' \
              f'muito tempo ou eles podem acabar sendo retirados do seu pedido.\n\n' \
              f'*APÓS O PAGAMENTO*:\nVocê poderá encontrar os dados do seu pedido na página ' \
              f'_Últimos Pedidos_ esse caminho está na página inicial.'

    adicional_info = f'*INFORMAÇÕES ADICIONAIS*:\n\n' \
                     f'Esse é o código copia e cola do _Pix_ ❖. Disponível para pessoas que não usam QR' \
                     f'Code Scanner.\n\n' \
                     f'{br_code}'

    context.bot.send_message(
        text=message, chat_id=update.effective_chat.id, parse_mode='Markdown')
    context.bot.send_message(
        text=adicional_info, chat_id=update.effective_chat.id, parse_mode='Markdown')

    return PAYMENT
