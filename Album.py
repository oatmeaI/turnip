import unicodedata
from utils.util import loadTracks
from utils.tagging import setAlbumTag, setAlbumArtistTag, getAlbumArtistTag
from Entry import Entry


class Album(Entry):
    def __init__(self, path: str):
        super(Album, self).__init__(path)
        self.tracks = loadTracks(path)

    def setTrackCount(self, count: int) -> None:
        None
        # for track in tracks set count

    def setYear(self, year: int) -> None:
        self.parts["year"] = year
        # build new path
        # rename / move
        # For each track in tracks set year

    def setAlbumArtist(self, albumArtist: str) -> None:
        for track in self.tracks:
            albumArtistTag = getAlbumArtistTag(track.path)
            if (albumArtistTag == albumArtist):
                continue
            setAlbumArtistTag(track.path, albumArtist)
            self.printPropUpdate('albumArtist', albumArtist)
        if (self.parts["artist"] != albumArtist):
            self.parts["artist"] = albumArtist
            self.updatePath()

    def getAlbumArtist(self) -> str:
        return unicodedata.normalize('NFC', self.parts["artist"])

    def setTitle(self, title: str) -> None:
        self.parts["album"] = title
        # TODO - this is a pattern that I'm repeating a lot; maybe I can
        # abstract it somewhere? Also, don't set if it's the same?
        map(lambda f: setAlbumTag(f, title))
        self.updatePath()
