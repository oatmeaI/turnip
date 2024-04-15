from typing import Any
from Command.Command import Command
from Command.Issue import Issue
from utils.constants import rootDir
from utils.util import compareDupes, loopAlbums, newFix, findBad
from utils.userio import promptHeader
from utils.fs import moveDirFiles


class AlbumDuplicates(Command):
    cta = "Possible album duplicates found. Select which to keep:"

    def findIssues(self) -> list[Issue]:
        keys: list[Any] = []
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

    def callback(self, good: str, issue: Issue) -> None:
        bad = findBad(issue, good)
        if bad and good:
            moveDirFiles(bad, good)


def findAlbumDupes(rootDir: str) -> list[Issue]:
    keys: list[Any] = []
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

    return newFix(issues=albumDupes, callback=callback, prompt=prompt)
