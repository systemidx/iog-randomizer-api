from distutils.util import strtobool

from decouple import config


class Config(object):
    def __init__(self):
        self.DEBUG = strtobool(config("DEBUG", default='False'))
        self.DB_ENABLED = strtobool(config("DB_ENABLED", default='False'))

        if not self.DB_ENABLED:
            return

        self.DB_USERNAME = config("DB_USERNAME")
        if not self.DB_USERNAME:
            raise ValueError("No DB_USERNAME set in CLI arguments or OS Environment")

        self.DB_PASSWORD = config("DB_PASSWORD")
        if not self.DB_PASSWORD:
            raise ValueError("No DB_PASSWORD set in CLI arguments or OS Environment")

        self.DB_AUTHDB = config("DB_AUTHDB")
        if not self.DB_AUTHDB:
            raise ValueError("No DB_AUTHDB set in CLI arguments or OS Environment")

        self.DB_HOST = config("DB_HOST")
        if not self.DB_HOST:
            raise ValueError("No DB_HOST set in CLI arguments or OS Environment")

        self.DB_PORT = config("DB_PORT")
        if not self.DB_PORT:
            raise ValueError("No DB_PORT set in CLI arguments or OS Environment")

        self.DB_DATABASE_ID = config("DB_DATABASE_ID")
        if not self.DB_DATABASE_ID:
            raise ValueError("No DB_DATABASE_ID set in CLI arguments or OS Environment")

        self.DB_COLLECTION_ID = config("DB_COLLECTION_ID")
        if not self.DB_COLLECTION_ID:
            raise ValueError("No DB_COLLECTION_ID set in CLI arguments or OS Environment")
