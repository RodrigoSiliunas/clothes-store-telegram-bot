import re
import logging

from multiprocessing import Process
from src.configuration import DevelopmentConfiguration

from src.utils.constants import HOME, ACCOUNT, STORE, CART, PAYMENT, ORDERS
from src.utils.functions import delete_message, remove_unfinished_order, transfer_paid_items


from src.routes import store
from src.routes import cart
from src.routes import start
from src.routes import account
from src.routes import payment
from src.routes import orders

from src import inline

from flask import Flask, request, jsonify
from flask_cors import CORS

from telegram.ext import (
    Updater,
    Filters,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
    InlineQueryHandler,
    MessageHandler
)

# Enable basic logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/api/v1/payments', methods=['GET', 'POST'])
def webhook_payment_check():
    if request.method == 'POST':
        data = request.get_json()
        uuid = data['charge']['correlationID']

        transfer_paid_items(uuid)

        return jsonify({
            "success": {
                "message": "Pix's status has changed and the payment appears as paid.",
                "data": data,
                "code": 200,
            }
        }), 200

    return jsonify({
        "error": {
            "message": "This route requires calling via a Post method.",
            "type": "RequestMethodError",
            "code": 404
        }
    }), 404


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(DevelopmentConfiguration.BOT_SECRET_KEY)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start.start)],
        states={
            HOME: [
                CallbackQueryHandler(
                    store.main_page, pattern='^' + 'open_store_information' + '$'),
                CallbackQueryHandler(
                    account.main_page, pattern='^' + 'user_information' + '$'),
                CallbackQueryHandler(
                    cart.main_page, pattern='^' + 'cart_main_page' + '$'),
                CallbackQueryHandler(
                    orders.main_page, pattern='^' + 'orders_main_page' + '$')
            ],
            ACCOUNT: [
                CallbackQueryHandler(
                    start.over, pattern='^' + 'back_to_home' + '$')
            ],
            STORE: [
                MessageHandler(Filters.regex(
                    re.compile(r'^Informação Detalhada:', re.IGNORECASE)), inline.set_message),
                MessageHandler(Filters.regex(
                    re.compile(r'^Ø', re.IGNORECASE)), inline.display_by_state),
                CallbackQueryHandler(
                    cart.main_page, pattern='^' + 'cart_main_page' + '$'),
                CallbackQueryHandler(
                    start.over, pattern='^' + 'back_to_home' + '$'),
                CallbackQueryHandler(
                    payment.main_page, pattern='^' + 'open_payment_page' + '$')
            ],
            CART: [
                CallbackQueryHandler(
                    cart.previous_page, pattern='^' + 'cart_previous_page' + '$'),
                CallbackQueryHandler(
                    cart.remove, pattern='^' + 'remove_from_cart' + '$'),
                CallbackQueryHandler(
                    cart.next_page, pattern='^' + 'cart_next_page' + '$'),
                CallbackQueryHandler(
                    start.over, pattern='^' + 'back_to_home' + '$'),
                CallbackQueryHandler(
                    payment.main_page, pattern='^' + 'open_payment_page' + '$')
            ],
            PAYMENT: [
                CallbackQueryHandler(
                    start.over, pattern='^' + 'back_to_home' + '$'),
                CallbackQueryHandler(
                    payment.create_pix_request, pattern='^' + 'create_pix_request' + '$'),
            ],
            ORDERS: [
                CallbackQueryHandler(
                    start.over, pattern='^' + 'back_to_home' + '$'),
                CallbackQueryHandler(
                    orders.next_page, pattern='^' + 'orders_next_page' + '$'),
                CallbackQueryHandler(
                    orders.previous_page, pattern='^' + 'orders_prev_page' + '$')
            ]
        },
        fallbacks=[CommandHandler('start', start.start)],
    )

    # on different commands - answer in Telegram
    dispatcher.add_handler(conv_handler)

    dispatcher.add_handler(CallbackQueryHandler(
        cart.add, pattern='^' + 'add_to_cart' + '$'))

    dispatcher.add_handler(CallbackQueryHandler(
        inline.delete_message, pattern='^' + 'delete_inline_message' + '$'))

    dispatcher.add_handler(CallbackQueryHandler(
        delete_message, pattern='^' + 'delete_message' + '$'))

    dispatcher.add_handler(InlineQueryHandler(
        inline.querys, run_async=True))

    # Process to remove unfinished orders.
    # unfinished_orders = Process(target=remove_unfinished_order)
    # unfinished_orders.start()

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
