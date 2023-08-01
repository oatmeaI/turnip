import os
from utils.constants import rootDir
from internal_types import Issue, Key
from utils.util import compareDupes, loopTracks, findBad
from utils.path import splitFileName
from utils.fs import rmFile
from commands.artistDuplicates import Command


class TrackDuplicates(Command):
    cta = "Possible duplicate tracks found. Select which to keep:"

    def findIssues(self) -> list[Issue]:
        keys: list[Key] = []
        currentArtist = ""

        def cb(artist, album, track) -> list[Issue]:
            nonlocal keys
            nonlocal currentArtist
            if currentArtist != artist:
                keys = []
                currentArtist = artist

            return compareDupes(track, keys, track.name)

        return loopTracks(rootDir, cb)

    def similar(self, issue: Issue) -> str:
        originalAlbum = splitFileName(issue["original"])["album"]
        deltaAlbum = splitFileName(issue["delta"])["album"]
        return f"{originalAlbum} > {deltaAlbum}"

    def callback(self, good: str, issue: Issue) -> None:
        bad = findBad(issue, good)
        if not bad or not os.path.exists(good) or not os.path.exists(bad):
            return
        rmFile(bad)
