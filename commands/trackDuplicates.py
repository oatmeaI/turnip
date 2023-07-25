import os
from utils.constants import rootDir
from internal_types import Issue, Key, Option
from utils.util import newFix, compareDupes, loopTracks, findBad
from utils.userio import promptHeader
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

    def callback(self, good: str, issue: Issue) -> None:
        bad = findBad(issue, good)
        if not bad or not os.path.exists(good) or not os.path.exists(bad):
            return
        rmFile(bad)


def process(rootDir: str) -> int:
    trackDupes = findTrackDupes(rootDir)

    def callback(good: str, issue: Issue) -> None:
        bad = findBad(issue, good)
        if not bad or not os.path.exists(good) or not os.path.exists(bad):
            return
        rmFile(bad)

    def heuristic(options: list[Option]) -> Option:
        return options[0]

    def prompt(issue: Issue, index: int, count: int) -> str:
        return (
            promptHeader("trackDuplicates", index, count)
            + "\n"
            + "Possible duplicate tracks found. Select which to keep:"
        )

    return newFix(
        issues=trackDupes,
        prompt=prompt,
        callback=callback,
        heuristic=heuristic,
    )
