from utils.util import loadTracks
from utils.tagging import setAlbumTag, setAlbumArtistTag
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
        self.parts["artist"] = albumArtist
        map(lambda f: setAlbumArtistTag(f, albumArtist), self.tracks)
        self.updatePath()

    def setTitle(self, title: str) -> None:
        self.parts["album"] = title
        # TODO - this is a pattern that I'm repeating a lot; maybe I can
        # abstract it somewhere? Also, don't set if it's the same?
        map(lambda f: setAlbumTag(f, title))
        self.updatePath()
