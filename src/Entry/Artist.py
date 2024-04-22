from Entry.Album import Album
from Entry.Entry import Entry
from Path.ArtistPath import ArtistPath
from utils.TagCache import TagNames
from utils.fs import loadFolders


class Artist(Entry):
    _albums: list[Album]
    _forceCache: bool
    path: ArtistPath

    def __init__(self, path, forceCache=False):
        super(Artist, self).__init__(path)
        self._albums = []
        self._forceCache = forceCache

    @property
    def albums(self):
        if len(self._albums) < 1:
            self._albums = []
            for folder in loadFolders(self.path.realPath):
                self._albums.append(Album(folder.path, forceCache=self._forceCache))
        return self._albums

    def setAlbumArtist(self, albumArtist: str) -> None:
        raise Exception("Not implemented")
        self.printPropUpdate(TagNames.ALBUM_ARTIST, albumArtist)

        for track in self.tracks:
            track.tags.setAlbumArtist(albumArtist)

        if self.path.albumArtist != albumArtist:
            self.path.setAlbumArtist(albumArtist)
