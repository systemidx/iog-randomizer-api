import hashlib

class Patch(object):
    patch: str = ''
    patchName: str = ''
    checksum: str = ''
    version: str = ''

    def __init__(self, patch: str, patchName: str, version: str):
        self.patch = patch
        self.patchName = patchName
        self.version = version
        self.checksum =  hashlib.md5(patch.encode('utf-8')).hexdigest()