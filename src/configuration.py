import os


class Configuration:
    pass


class DevelopmentConfiguration(Configuration):
    BOT_SECRET_KEY = "5354755740:AAEB24P4RnwkZXB8eyk2uPB0lsFKcHwAdpM"


class ProductionConfiguration(Configuration):
    BOT_SECRET_KEY = os.environ.get("BOT_SECRET_KEY")
