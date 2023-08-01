from Entry import Entry
from utils.tagging import setTitleTag, setArtistTag, setAlbumArtistTag


class Song(Entry):
    propUpdateSideEffects = {"title": setTitleTag, "artist": setAlbumArtistTag}

    # TODO - better differentiating between artist and albumArtist - maybe split/build file path should say "albumAritst"
    def setAlbumArtist(self, artist: str) -> None:
        self.updateProp("artist", artist)

    def setArtist(self, artist: str) -> None:
        setArtistTag(self.path, artist)

    def setTitle(self, title: str) -> None:
        self.updateProp("title", title)

    def setTrackNumber(self, number: int) -> None:
        None
        # Set number tag
        # Build filename
        # Rename / move
