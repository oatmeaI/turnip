from utils.constants import rootDir
from utils.util import compareDupes, loopArtists, findBad
from internal_types import Issue, Key
from utils.fs import moveDirFiles
from Command import Command


class ArtistDuplicates(Command):
    cta = "Possible artist duplicates found. Select which to keep:"

    def findIssues(self) -> list[Issue]:
        keys: list[Key] = []

        def cb(artist):
            return compareDupes(artist, keys, artist.name)

        return loopArtists(rootDir, cb)

    def callback(self, good: str, issue: Issue) -> None:
        bad = findBad(issue, good)
        if bad and good:
            moveDirFiles(bad, good)
