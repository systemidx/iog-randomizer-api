import json


class VersionResponse(object):
    version: str = ''

    def __init__(self, version: str):
        self.version = version

    def to_json(self):
        return json.dumps(self.__dict__)
