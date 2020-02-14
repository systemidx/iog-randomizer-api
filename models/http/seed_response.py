import hashlib, json

class SeedResponse(object):
    permalink_id: str = ''
    patch: str = ''
    patchName: str = ''
    spoiler: str = ''
    spoilerName: str = ''
    checksum: str = ''
    version: str = ''

    def __init__(self, patch: str, patchName: str, version: str, permalink_id: str):
        self.patch = patch
        self.patchName = patchName
        self.version = version
        self.permalink_id = permalink_id
        self.checksum =  hashlib.md5(patch.encode('utf-8')).hexdigest()

    def to_json(self):
        return json.dumps(self.__dict__)
