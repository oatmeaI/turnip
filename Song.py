from Entry import Entry
from utils.tagging import setTitleTag, setArtistTag, setAlbumArtistTag, setAlbumTag


class Song(Entry):
    propUpdateSideEffects = {"title": setTitleTag, "artist": setAlbumArtistTag, "album": setAlbumTag}

    # TODO - better differentiating between artist and albumArtist - maybe split/build file path should say "albumAritst"
    def setAlbumArtist(self, artist: str) -> None:
        self.updateProp("artist", artist)

    def setAlbum(self, album: str) -> None:
        self.updateProp("album", album)

    def setArtist(self, artist: str) -> None:
        setArtistTag(self.path, artist)

    def setTitle(self, title: str) -> None:
        self.updateProp("title", title)

    def setTrackNumber(self, number: int) -> None:
        None
        # Set number tag
        # Build filename
        # Rename / move
