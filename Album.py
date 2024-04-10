import unicodedata
from Song import Song
from utils.util import loadTracks
from utils.tagging import setYearTag
from Entry import Entry


class Album(Entry):
    tracks: list[Song]

    def __init__(self, path: str):
        super(Album, self).__init__(path)

        self.tracks = []
        for track in loadTracks(path):
            self.tracks.append(Song(track.path))

    def getAlbumArtist(self) -> str:
        return unicodedata.normalize('NFC', self.parts["artist"])

    def getAlbumTitle(self) -> str:
        return unicodedata.normalize('NFC', self.parts["album"])

    def setTrackCount(self, count: int) -> None:
        # TODO
        return None
        # for track in tracks set count

    def setYear(self, year: int) -> None:
        self.parts["year"] = str(year)

        for track in self.tracks:
            setYearTag(track.path, str(year))

        self.updatePath()

    def setAlbumArtist(self, albumArtist: str) -> None:
        self.parts["artist"] = albumArtist

        for track in self.tracks:
            track.tags.setAlbumArtist(albumArtist)

        self.updatePath()

    def setTitle(self, title: str) -> None:
        self.parts["album"] = title

        for track in self.tracks:
            track.tags.setAlbum(title)

        self.updatePath()
