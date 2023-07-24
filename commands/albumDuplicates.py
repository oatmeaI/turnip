from utils.util import compareDupes, loopAlbums, check, newFix, findBad
from utils.path import stripRootPath
from utils.userio import promptHeader
from internal_types import Issue, Key
from utils.fs import moveDirFiles
from typing import Optional


def findAlbumDupes(rootDir: str) -> list[Issue]:
    keys: list[Key] = []
    currentArtist = ""

    def cb(artist, album):
        nonlocal keys
        nonlocal currentArtist
        if currentArtist != artist:
            keys = []
            currentArtist = artist

        return compareDupes(
            album,
            keys,
            album.name,
        )

    return loopAlbums(rootDir, cb)


def process(rootDir: str) -> int:
    albumDupes = findAlbumDupes(rootDir)

    def callback(good: str, issue: Issue):
        bad = findBad(issue, good)
        if bad and good:
            moveDirFiles(bad, good)

    def prompt(issue: Issue, index: int, count: int):
        return (
            promptHeader("albumDuplicates", index, count)
            + "\n"
            + "Possible album duplicates found. Select which to keep:"
        )

    return newFix(rootDir=rootDir, issues=albumDupes, callback=callback, prompt=prompt)
