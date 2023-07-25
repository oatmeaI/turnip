from utils.util import loopAlbums, newFix
from utils.userio import bold, purple
from internal_types import Issue, Option
from utils.fs import loadTracks
from commands.countTagConflicts import detectConflictedTracks, detectMissingTrackCount
from utils.tagging import getTrackCountTag
from tidal.rip import rip
from utils.path import stripRootPath, splitFileName
from utils.fs import rmDir
from tidal.tidal import searchAlbum
import os


def findMissingTracks(rootDir: str) -> list[Issue]:
    i = 0

    def cb(artist: os.DirEntry, album: os.DirEntry) -> list[Issue]:
        nonlocal i
        found: list[Issue] = []
        i += 1
        tracks = loadTracks(album.path)
        conflict = detectConflictedTracks(album, tracks)
        missing = detectMissingTrackCount(album, tracks)

        if conflict or missing:
            return []

        for track in tracks:
            count = getTrackCountTag(track.path)
            if count:
                break

        if not count:
            return []

        actualCount = len(tracks)
        if actualCount < count:
            issue: Issue = {
                "data": None,
                "entry": album,
                "delta": str(count),
                "original": str(actualCount),
            }
            found.append(issue)

        return found

    return loopAlbums(rootDir, cb)


def process(rootDir):
    albumsMissingTracks = findMissingTracks(rootDir)

    def prompt(issue: Issue, index: int, count: int) -> str:
        line1 = (
            "\n"
            + "\n"
            + purple("[fixMissingTracks]:\n")
            + "Progress: "
            + str(index)
            + "/"
            + str(count)
            + "\n"
            + "Found "
            + str(issue["original"])
            + " tracks for album "
            + issue["entry"].name
            + ". Expected "
            + bold(str(issue["delta"]))
            + " at "
            + bold(stripRootPath(issue["entry"].path))
        )

        return line1

    def cb(good, issue):
        rmDir(issue["entry"])
        rip(good)

    def makeKey(result):
        return (
            result.artist.name
            + " - "
            + result.name
            + (" (Explicit)" if result.explicit else "")
            + " ("
            + str(result.year)
            + ")"
            + ": "
            + str(result.num_tracks)
            + " (Available: "
            + str(result.tidal_release_date.year)
            + ")"
        )

    def suggest(issue: Issue) -> list[Option]:
        album = issue["entry"]
        parts = splitFileName(album.path)
        if not parts:
            return []
        results = searchAlbum(parts["album"], parts["artist"])
        choices: list[Option] = []
        for result in results:
            url = "https://listen.tidal.com/album/" + str(result.id)
            choices.append({"key": "NONE", "value": url,
                           "display": makeKey(result)})
        return choices

    return newFix(
        issues=albumsMissingTracks,
        prompt=prompt,
        callback=cb,
        suggest=suggest,
        skipIssueValues=True,
        suggestionLimit=-1,
    )
