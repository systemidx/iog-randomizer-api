import base64
import logging

import jsonpickle
import pymongo
from bson.objectid import ObjectId
from iog_randomizer.randomizer.models.enums import FluteOpt
from iog_randomizer.randomizer.models.randomizer_data import RandomizerData as Settings

from config import Config
from models.entry import Entry
from models.patch import Patch
from models.spoiler import Spoiler


class Database(object):
    def __init__(self, logging: logging, config: Config):
        self.logging = logging
        self.config = config
        self.enabled = config.DB_ENABLED

        if not self.enabled:
            return

        uri = "mongodb://{}:{}@{}:{}/{}?authSource={}".format(self.config.DB_USERNAME, self.config.DB_PASSWORD,
                                                              self.config.DB_HOST, self.config.DB_PORT,
                                                              self.config.DB_DATABASE_ID, self.config.DB_AUTHDB)
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[self.config.DB_DATABASE_ID]
        self.collection = self.db[self.config.DB_COLLECTION_ID]

    def create(self, patch: Patch, spoiler: Spoiler, settings: Settings, hide_settings: bool = False) -> str:
        if not self.enabled:
            raise EnvironmentError("Database not enabled")

        _settings = None
        if not hide_settings:
            _settings = jsonpickle.encode(settings.__dict__)

        _fluteless = True if settings.flute == FluteOpt.FLUTELESS else False

        _spoiler = None
        _spoiler_name = None
        if spoiler is not None:
            _spoiler = spoiler.spoiler
            _spoiler_name = spoiler.spoilerName

        entry = Entry(settings.seed, patch.version, patch.patch, patch.patchName, _spoiler, _spoiler_name, _settings,
                      _fluteless)

        key = self.collection.insert_one(entry.__dict__)
        return str(key.inserted_id)

    def get(self, key: str) -> Entry:
        if not self.enabled:
            raise EnvironmentError("Database not enabled")

        entry = self.collection.find_one({"_id": ObjectId(key)})
        return entry

    def __encode__(self, obj):
        json = jsonpickle.encode(obj, unpicklable=True)
        json_bytes = json.encode('utf-8')
        return base64.b64encode(json_bytes)
