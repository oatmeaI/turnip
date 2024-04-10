from Album import Album
from Entry import Entry
from Song import Song
from internal_types import TrackNameParts
from utils.util import loadFolders
from utils.tagging import setAlbumArtistTag


class Artist(Entry):
    parts: TrackNameParts
    albums: list[Album]
    tracks: list[Song]
    path: str

    def __init__(self, path: str):
        super(Artist, self).__init__(path)
        self.path = path

        self.albums = []
        for folder in loadFolders(path):
            self.albums.append(Album(folder.path))

        self.tracks = []
        for album in self.albums:
            self.tracks += album.tracks

    def __str__(self):
        return self.path

    def setName(self, name: str) -> None:
        self.parts["artist"] = name
        self.updatePath()
        for track in self.tracks:
            setAlbumArtistTag(track.path, name)
