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
        self.checksum =  self.__generateChecksum__(patch, version)

    def __generateChecksum__(self, patch: str, version: str):
        encodedPatch = patch.encode('utf-8')
        encodedVersion = version.encode('utf-8')
        return hashlib.md5(encodedPatch + encodedVersion).hexdigest()