import os
from Entry import Entry
from utils.util import loadFolders, loadTracks
from utils.tagging import setAlbumArtistTag


class Artist(Entry):
    def __init__(self, path: str):
        super(Artist, self).__init__(path)
        self.albums = loadFolders(path)
        self.tracks = []
        map(lambda album: self.tracks.append(loadTracks(album.path)), self.albums)

    def setName(self, name: str) -> None:
        self.parts["artist"] = name
        self.updatePath()
        map(lambda f: setAlbumArtistTag(f, name), self.tracks)
