import pickle
import os
from typing import Union


def readTagCache():
    if not os.path.exists('tagCache.pickle'):
        return {}
    with open('tagCache.pickle', 'rb') as f:
        return pickle.load(f)


def writeTagCache():
    with open('tagCache.pickle', 'wb') as f:
        pickle.dump(tagCache, f, protocol=pickle.HIGHEST_PROTOCOL)


tagCache = readTagCache()


class TagNames:
    ALBUM_ARTIST = 'albumArtist'
    ARTIST = 'artist'
    YEAR = 'year'
    TITLE = 'title'
    TRACK_NUMBER = 'trackNumber'
    TRACK_COUNT = 'trackCount'
    ALBUM = 'album'


class _TagCache:

    def __init__(self):
        self.cache = {}
        self.loadCache()
        self.batches = 0

    def getValue(self, track: str, key: str):
        if track not in self.cache:
            return None
        trackCache = self.cache[track]

        return trackCache[key] if key in trackCache else ''

    def setValue(self, track: str, key: str, value: Union[str, int]):
        if track not in self.cache:
            self.cache[track] = {}
        self.cache[track][key] = value
        self.writeCache()

    def loadCache(self):
        if not os.path.exists('tagCache.pickle'):
            return {}
        with open('tagCache.pickle', 'rb') as f:
            self.cache = pickle.load(f)

    # TODO -this will fail when changing one track at a time during editing.
    # probably fixed by just using db
    def writeCache(self):
        self.batches += 1
        if self.batches > 100:
            self.batches = 0
            with open('tagCache.pickle', 'wb') as f:
                pickle.dump(self.cache, f, protocol=pickle.HIGHEST_PROTOCOL)


TagCache = _TagCache()
