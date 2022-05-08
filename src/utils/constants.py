from src.database import client

from src.pix import PixBot
from src.pix.configuration import Configuration


# Constants to change the paging state.
HOME = 0
ACCOUNT = 1
STORE = 2
CART = 3
PAYMENT = 4
ORDERS = 5


# Constants for navigating between MongoDB collections.
DB = client['telegram']
CPF_COLLECTION = DB['cpfs']
COSTUMERS_COLLECTION = DB['costumers']
SOLDED_COLLECTION = DB['solded']
STORE_COLLECTION = DB['store']


# Location for Pix
PIX = PixBot(Configuration.APP_ID)
