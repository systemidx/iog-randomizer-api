import logging

from collections import OrderedDict
from pymongo import MongoClient
from pymongo.cursor import Cursor
from pymongo.collection import Collection

from config import Config
from randomizer.models.randomizer_data import RandomizerData as Settings
from models.patch import Patch
from models.spoiler import Spoiler
from models.document import Document

class Database(object):
    def __init__(self, logging: logging, config: Config):
        self.logging = logging
        self.config = config
        self.enabled = config.DB_ENABLED

        if not self.enabled:
            return

        self.client = MongoClient(config.DB_CONNECTIONSTRING, retryWrites=False)
        self.db = self.client[config.DB_DATABASE_ID]
        self.collection = self.db[config.DB_COLLECTION_ID]

    def create(self, patch: Patch, spoiler: Spoiler, settings: Settings) -> str:
        if not self.enabled:
            raise EnvironmentError("Database not enabled")

        document = Document(patch.checksum, patch.version, patch.patch, patch.patchName, spoiler.spoiler, spoiler.spoilerName, settings).to_document()
        key = document["_id"]

        tries = 0
        while self.exists(document["_id"]):
            if tries > 2:
                raise KeyError("Unable to generate a unique key")
            document = Document(patch.checksum, patch.version, patch.patch, patch.patchName, spoiler.spoiler, spoiler.spoilerName, settings).to_document()
            tries += 1

        
        self.collection.insert_one(document)
        return key

    def get(self, id: str) -> Document:
        if not self.enabled:
            raise EnvironmentError("Database not enabled")

        f = OrderedDict([{ "_id", id }])
        document = self.collection.find_one(f)
        
        return document

    def exists(self, id: str) -> bool:
        if not self.enabled:
            raise EnvironmentError("Database not enabled")
        
        f = OrderedDict([{ "_id", id }])
        count: int = self.collection.count_documents(f)
        return count > 0