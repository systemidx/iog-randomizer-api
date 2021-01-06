from models.patch import Patch
from models.spoiler import Spoiler


class Result(object):
    patch: Patch
    spoiler: Spoiler
    permalink: str

    def __init__(self, patch: Patch, spoiler: Spoiler = None, permalink: str = None):
        self.patch = patch
        self.spoiler = spoiler
        self.permalink = permalink
