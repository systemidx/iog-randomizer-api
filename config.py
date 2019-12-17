import os

class Config(object):
    def __init__(self):

        self.DB_CONNECTIONSTRING = os.environ.get("DB_CONNECTIONSTRING")
        if not self.DB_CONNECTIONSTRING:
            raise ValueError("No DB_CONNECTIONSTRING set in CLI arguments or OS Environment")

        self.DB_DATABASE_ID = os.environ.get("DB_DATABASE_ID")
        if not self.DB_DATABASE_ID:
            raise ValueError("No DB_DATABASE_ID set in CLI arguments or OS Environment")

        self.DB_COLLECTION_ID = os.environ.get("DB_COLLECTION_ID")
        if not self.DB_COLLECTION_ID:
            raise ValueError("No DB_COLLECTION_ID set in CLI arguments or OS Environment")            
