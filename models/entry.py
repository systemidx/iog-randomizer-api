from datetime import datetime
from enum import Enum

import jsonpickle


@jsonpickle.handlers.register(Enum, base=True)
class EnumHandler(jsonpickle.handlers.BaseHandler):
    def flatten(self, obj, data):
        return obj.value


class Entry(object):
    def __init__(
        self, seed: int, version: str, patch: str, patchName: str, spoiler: str, spoilerName: str, settings: str,
        fluteless: str
        ):
        self.seed = seed
        self.version = version
        self.patch = patch
        self.patchName = patchName
        self.spoiler = spoiler
        self.spoilerName = spoilerName
        self.settings = settings
        self.fluteless = fluteless
        self.created_at = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    def to_dict(self):
        return self.__dict__

    def to_document(self):
        parameters = self.__dict__
        encoded = jsonpickle.encode(parameters, unpicklable=True)
        decoded = jsonpickle.decode(encoded)

        return decoded

    def to_json(self):
        parameters = self.__dict__
        encoded = jsonpickle.encode(parameters, unpicklable=True)
        return encoded
