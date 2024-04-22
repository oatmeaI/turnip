import os
from typing import Dict, Optional
from Entry.Entry import Entry
from Path.TrackPath import TrackPath
from utils.TagCache import TagNames
from utils.loadTags import BaseTags, loadTags

tagsObjCache: Dict[str, BaseTags] = {}


class Track(Entry):
    _tags: Optional[BaseTags]
    path: TrackPath

    def __init__(self, path, forceCache=False):
        super(Track, self).__init__(path, forceCache)
        self._tags = None

    @property
    def getMap(self):
        return {
            'title': self.title,
            'album': self.album,
            'albumArtist': self.albumArtist,
            'artist': self.artist,
            'year': self.year
        }

    @property
    def setMap(self):
        return {
            'title': self.setTitle,
            'album': self.setAlbum,
            'albumArtist': self.setAlbumArtist,
            'artist': self.setArtist,
            'year': self.setYear
        }

    def __getitem__(self, name: str):
        return self.getMap[name]

    def __setitem__(self, name: str, value):
        self.setMap[name](value)

    @property
    def tags(self) -> BaseTags:
        if not self._tags:
            self.loadTags()
        if not self._tags:
            raise Exception("No tags")
        return self._tags

    def loadTags(self):
        if self.path.realPath in tagsObjCache:
            self._tags = tagsObjCache[self.path.realPath]
        self._tags = loadTags(self.path.realPath, self._forceCache) # TODO - take a Path

    @property
    def title(self):
        return self.tags.title or self.path.title or ''

    @property
    def albumArtist(self):
        return self.tags.albumArtist or self.path.albumArtist or ''

    @property
    def album(self):
        return self.tags.album or self.path.album or ''

    @property
    def year(self):
        return self.tags.year or self.path.year or ''

    @property
    def artist(self):
        return self.tags.artist or ''

    @property
    def trackNumber(self):
        return self.tags.trackNumber or self.path.trackNumber or ''

    @property
    def trackCount(self):
        return self.tags.trackCount or ''

    @property
    def bitrate(self):
        return self.tags.bitrate

    @property
    def length(self):
        return self.tags.length

    @property
    def size(self):
        return round(os.path.getsize(self.path.realPath) / 1000000, 2)

    def setAlbumArtist(self, albumArtist: str) -> None:
        self.printPropUpdate(TagNames.ALBUM_ARTIST, albumArtist)
        self.tags.setAlbumArtist(albumArtist)
        self.path.setAlbumArtist(albumArtist)
        self.tags.trackPath = self.path.realPath # TODO cleaner way to do this?

    def setAlbum(self, album: str) -> None:
        self.printPropUpdate(TagNames.ALBUM, album)
        self.tags.setAlbum(album)
        self.path.setAlbum(album)
        self.tags.trackPath = self.path.realPath # TODO cleaner way to do this?

    def setArtist(self, artist: str) -> None:
        self.printPropUpdate(TagNames.ARTIST, artist)
        self.tags.setArtist(artist)

    def setTitle(self, title: str) -> None:
        self.printPropUpdate(TagNames.TITLE, title)
        self.tags.setTitle(title)
        self.path.setTitle(title)
        self.tags.trackPath = self.path.realPath # TODO cleaner way to do this?

    def setYear(self, year: str) -> None:
        self.printPropUpdate(TagNames.YEAR, year)
        self.tags.setYear(year)
        self.path.setYear(year)
        self.tags.trackPath = self.path.realPath # TODO cleaner way to do this?

    def setTrackNumber(self, number: int) -> None:
        self.printPropUpdate(TagNames.TRACK_NUMBER, str(number))
        self.tags.setTrackNumber(number)
        self.path.setTrackNumber(number)
        self.tags.trackPath = self.path.realPath # TODO cleaner way to do this?
