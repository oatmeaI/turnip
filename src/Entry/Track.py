from typing import Dict, Optional
from Entry.Entry import Entry
from Path.TrackPath import TrackPath
from utils.TagCache import TagNames
from utils.loadTags import BaseTags, loadTags

tagsObjCache: Dict[str, BaseTags] = {}


class Track(Entry):
    _tags: Optional[BaseTags]
    path: TrackPath

    def __init__(self, path):
        super(Track, self).__init__(path)
        self._tags = None

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
        self._tags = loadTags(self.path.realPath) # TODO - take a Path

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
    def artist(self):
        return self.tags.artist or ''

    def setAlbumArtist(self, albumArtist: str) -> None:
        self.printPropUpdate(TagNames.ALBUM_ARTIST, albumArtist)
        self.tags.setAlbumArtist(albumArtist)
        self.path.setAlbumArtist(albumArtist) # TODO rename this to albumArtist

    def setAlbum(self, album: str) -> None:
        self.printPropUpdate(TagNames.ALBUM, album)
        self.tags.setAlbum(album)
        self.path.setAlbum(album)

    def setArtist(self, artist: str) -> None:
        self.printPropUpdate(TagNames.ARTIST, artist)
        self.tags.setArtist(artist)

    def setTitle(self, title: str) -> None:
        self.printPropUpdate(TagNames.TITLE, title)
        self.tags.setTitle(title)
        self.path.setTitle(title)

    def setTrackNumber(self, number: int) -> None:
        self.printPropUpdate(TagNames.TRACK_NUMBER, str(number))
        self.tags.setTrackNumber(number)
        self.path.setTrackNumber(number)
