import unicodedata
from Entry.Entry import Entry
from Entry.Track import Track
from Path.AlbumPath import AlbumPath
from utils.TagCache import TagNames
from utils.fs import loadTracks


class Album(Entry):
    _tracks: list[Track]
    path: AlbumPath

    def __init__(self, path, forceCache=False):
        super(Album, self).__init__(path, forceCache)
        self._tracks = []

    @property
    def tracks(self):
        if len(self._tracks) < 1:
            for track in loadTracks(self.path.realPath):
                self._tracks.append(Track(track.path, forceCache=self._forceCache))
        return self._tracks

    def getAlbumTitle(self) -> str:
        return unicodedata.normalize('NFC', self.path.album)

    def setTrackCount(self, count: int) -> None:
        # TODO
        return None
        # for track in tracks set count

    def setYear(self, year: str) -> None:
        self.printPropUpdate(TagNames.YEAR, year)
        self.path.setYear(year)

        for track in self.tracks:
            track.tags.setYear(year)

    def setAlbum(self, album: str) -> None:
        self.printPropUpdate(TagNames.ALBUM, album)

        for track in self.tracks:
            if track.tags.album != album:
                track.tags.setAlbum(album)

        if (self.path.album != album):
            self.path.setAlbum(album)
        else:
            print("No need to move")

    def setAlbumArtist(self, albumArtist: str) -> None:
        self.printPropUpdate(TagNames.ALBUM_ARTIST, albumArtist)

        for track in self.tracks:
            track.tags.setAlbumArtist(albumArtist)

        if (self.path.albumArtist != albumArtist):
            self.path.setAlbumArtist(albumArtist)

    def setTitle(self, title: str) -> None:
        raise Exception('not implemented')
        # self.parts["album"] = title

        for track in self.tracks:
            track.tags.setAlbum(title)

        self.updatePath()
