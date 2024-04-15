import pickle
import sqlite3
import os
from typing import Union


class TagNames:
    ALBUM_ARTIST = 'albumArtist'
    ARTIST = 'artist'
    YEAR = 'year'
    TITLE = 'title'
    TRACK_NUMBER = 'trackNumber'
    TRACK_COUNT = 'trackCount'
    ALBUM = 'album'


# TODO - separate Driver code out into separate classes
# TODO - it turns out sqlite is actually slower than pickle; makes sense - this isn't very relational data, a key-value store makes more sense. look into other solutions (redis?) that might be even faster
class _TagCache:
    def __init__(self, driver='pickle'):
        self.driver = driver
        self.cache = {}
        self.loadCache()

    def escape(self, string):
        result = string.replace('"', '').replace('\'', '') # TODO
        return result

    def getValue(self, track: str, key: str):
        if self.driver == 'sqlite':
            query = f"SELECT {key} from tracks where path='{self.escape(track)}'"
            # print(query, self.reads, self.writes)
            return self.cur.execute(query).fetchone()
        if track not in self.cache or key not in self.cache[track]:
            return False
        trackCache = self.cache[track]

        return trackCache[key] if key in trackCache else ''

    def setValue(self, track: str, key: str, value: Union[str, int]):
        if self.driver == 'sqlite':
            query = f"""
    INSERT INTO tracks(path, {key}) VALUES
        ('{self.escape(track)}', '{self.escape(value)}') ON CONFLICT(path) DO UPDATE SET {key}='{self.escape(value)}';
"""
            # print(query, self.reads, self.writes)
            self.cur.execute(query)
            self.con.commit()

        if track not in self.cache:
            self.cache[track] = {}
        self.cache[track][key] = value

    def loadCache(self):
        if self.driver == 'pickle':
            if not os.path.exists('tagCache.pickle'):
                return {}
            with open('tagCache.pickle', 'rb') as f:
                self.cache = pickle.load(f)
        if self.driver == 'sqlite':
            source = sqlite3.connect('existing_db.db')
            dest = sqlite3.connect(':memory:')
            source.backup(dest)
            self.con = sqlite3.connect(":memory:",isolation_level=None)
            self.cur = self.con.cursor()
            self.cur.execute("CREATE TABLE IF NOT EXISTS tracks(path PRIMARY KEY, title, artist, albumArtist, album, trackNumber, trackCount, year)")
            self.cur.execute('''PRAGMA synchronous = OFF''')
            self.cur.execute('''PRAGMA journal_mode = OFF''')

    def writeCache(self):
        with open('tagCache.pickle', 'wb') as f:
            pickle.dump(self.cache, f, protocol=pickle.HIGHEST_PROTOCOL)


TagCache = _TagCache()
