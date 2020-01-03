import jsonpickle, hashlib, uuid
from enum import Enum
from randomizer.models.randomizer_data import RandomizerData as Settings

@jsonpickle.handlers.register(Enum, base=True)
class EnumHandler(jsonpickle.handlers.BaseHandler):
    def flatten(self, obj, data):
        return obj.value

class Document(object):
    def __init__(self, checksum: str, version: str, patch: str, patchName: str, spoiler: str, spoilerName: str, settings: Settings):
        self._id = hashlib.sha1(uuid.uuid4().bytes).hexdigest()[:8]
        self.checksum = checksum
        self.version = version
        self.patch = patch
        self.patchName = patchName
        self.spoiler = spoiler
        self.spoilerName = spoilerName         
        self.settings = settings.__dict__

    def to_document(self):
        parameters = self.__dict__
        encoded = jsonpickle.encode(parameters, unpicklable=True)
        decoded = jsonpickle.decode(encoded)

        return decoded

    def to_json(self):
        parameters = self.__dict__
        encoded = jsonpickle.encode(parameters, unpicklable=True)
        return encoded