from utils.util import compareDupes, loopArtists, newFix, check, findBad
from utils.userio import promptHeader
from utils.path import stripRootPath
from internal_types import Issue, Key
from utils.fs import moveDirFiles
from typing import Optional


def findArtistDupes(rootDir: str) -> list[Issue]:
    keys: list[Key] = []

    def cb(artist):
        return compareDupes(artist, keys, artist.name)

    return loopArtists(rootDir, cb)


def process(rootDir: str) -> int:
    artistDupes = findArtistDupes(rootDir)

    def callback(good: str, issue: Issue) -> None:
        bad = findBad(issue, good)
        if bad and good:
            moveDirFiles(bad, good)

    def prompt(issue: Issue, index: int, count: int):
        return (
            promptHeader("artistDuplicates", index, count)
            + "\n"
            + "Possible artist duplicates found. Select which to keep:"
        )

    return newFix(rootDir=rootDir, issues=artistDupes, callback=callback, prompt=prompt)
