from .configuration import ProductionConfiguration
from pymongo import MongoClient

"""
==========================================================================
 ➠ Database Configuration File
 ➠ Section By: Neo
 ➠ Related system: Database (PyMongo)
 ➠ Tips: To avoid circular imports this file is required. Please don't delete this file.
==========================================================================
"""

client = MongoClient(ProductionConfiguration.MONGO_URI)
