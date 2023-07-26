from Entry import Entry
from utils.tagging import setTitleTag
from utils.path import stripRootPath


class Song(Entry):
    propUpdateSideEffects = {"title": setTitleTag}

    def setArtist(self, artist: str) -> None:
        None
        # Set artist tag

    def setTitle(self, title: str) -> None:
        self.updateProp("title", title)

    def setTrackNumber(self, number: int) -> None:
        None
        # Set number tag
        # Build filename
        # Rename / move
