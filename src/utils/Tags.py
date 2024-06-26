from typing import Any, Optional
from utils.TagCache import TagCache, TagNames
from utils.constants import args


def useCache(tagName):
    def useCacheWrapper(func):
        def wrapped(self):
            value = TagCache.getValue(self.trackPath, tagName)
            if (args.no_cache and not self._forceCache) or value is False:
                value = func(self)
                TagCache.setValue(self.trackPath, tagName, value)
            return value
        return wrapped
    return useCacheWrapper


def updateCache(tagName):
    def updateCacheWrapper(func):
        def wrapped(self, value):
            # raise Exception('rekt')
            func(self, value)
            TagCache.setValue(self.trackPath, tagName, value)
        return wrapped
    return updateCacheWrapper


class BaseTags:
    trackPath: str
    _metadata: Any = {}
    _forceCache: bool

    def __init__(self, trackPath: str, forceCache=False):
        self.trackPath = trackPath
        self.parsed = False
        self._forceCache = forceCache

    @property
    def metadata(self):
        if not self.parsed:
            self.load()
            self.parsed = True

            # Cache all tags for the track the first time we load it into memory
            # TODO - is there a better way to do this, or is verbose better?
            self.artist
            self.title
            self.year
            self.album
            self.trackCount
            self.trackNumber
            self.albumArtist
        return self._metadata

    def load(self):
        raise Exception("Not implemented")

    @property
    def bitrate(self) -> str:
        return self.metadata.info.bitrate

    @property
    def length(self) -> str:
        return self.metadata.info.length

    @property
    @useCache(TagNames.ARTIST)
    def artist(self) -> str:
        return self._getArtist() or ''

    @property
    @useCache(TagNames.TITLE)
    def title(self) -> str:
        return self._getTitle() or ''

    @property
    @useCache(TagNames.ALBUM)
    def album(self) -> str:
        return self._getAlbum() or ''

    @property
    @useCache(TagNames.ALBUM_ARTIST)
    def albumArtist(self) -> str:
        return str(self._getAlbumArtist()) or ''

    @property
    @useCache(TagNames.TRACK_NUMBER)
    def trackNumber(self) -> int:
        return self._getTrackNumber() or 0

    @property
    @useCache(TagNames.TRACK_COUNT)
    def trackCount(self) -> int:
        return self._getTrackCount() or 0

    @property
    @useCache(TagNames.YEAR)
    def year(self) -> Optional[str]:
        return self._getYear()

    @updateCache(TagNames.ALBUM_ARTIST)
    def setAlbumArtist(self, albumArtist: str) -> None:
        self._updateAlbumArtistTag(albumArtist)

    @updateCache(TagNames.ARTIST)
    def setArtist(self, artist: str) -> None:
        self._updateArtistTag(artist)

    @updateCache(TagNames.TITLE)
    def setTitle(self, title: str) -> None:
        self._updateTitleTag(title)

    @updateCache(TagNames.ALBUM)
    def setAlbum(self, album: str) -> None:
        self._updateAlbumTag(album)

    @updateCache(TagNames.TRACK_COUNT)
    def setTrackCount(self, trackCount: int) -> None:
        self._updateTrackCountTag(trackCount)

    @updateCache(TagNames.TRACK_NUMBER)
    def setTrackNumber(self, trackNumber: int) -> None:
        self._updateTrackNumberTag(trackNumber)

    @updateCache(TagNames.YEAR)
    def setYear(self, year: str) -> None:
        self._updateYearTag(year)

    def _getAlbumArtist(self) -> str:
        raise Exception('Not implemented')

    def _getArtist(self) -> str:
        raise Exception('Not implemented')

    def _getTitle(self) -> str:
        raise Exception('Not implemented')

    def _getAlbum(self) -> str:
        raise Exception('Not implemented')

    def _getYear(self) -> str:
        raise Exception('Not implemented')

    def _getTrackNumber(self) -> int:
        raise Exception('Not implemented')

    def _getTrackCount(self) -> int:
        raise Exception('Not implemented')

    def _updateAlbumArtistTag(self, albumArtist: str) -> None:
        raise Exception('Not implemented')

    def _updateArtistTag(self, artist: str) -> None:
        raise Exception('Not implemented')

    def _updateTitleTag(self, title: str) -> None:
        raise Exception('Not implemented')

    def _updateAlbumTag(self, album: str) -> None:
        raise Exception('Not implemented')

    def _updateYearTag(self, year: str) -> None:
        raise Exception('Not implemented')

    def _updateTrackNumberTag(self, trackNumber: int) -> None:
        raise Exception('Not implemented')

    def _updateTrackCountTag(self, trackCount: int) -> None:
        raise Exception('Not implemented')
