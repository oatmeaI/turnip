import os
from internal_types import Issue, Option
from utils.util import newFix, loadTracks, loopAlbums
from utils.path import splitFileName, buildFileName, parseTrackPath, stripRootPath
from utils.tagging import (
    getTrackNumberTag,
    setTrackNumberTag,
)
from utils.userio import promptHeader, bold, blue
from tidal import tidal


def findConflictedTrackNumber(rootDir: str) -> list[Issue]:
    def cb(artist: os.DirEntry, album: os.DirEntry) -> list[Issue]:
        found: list[Issue] = []
        tracks = loadTracks(album.path)
        numbers = []
        for track in tracks:
            tagNumber = getTrackNumberTag(track.path)
            if tagNumber in numbers:
                found.append(
                    {
                        "data": None,
                        "entry": track,
                        "original": str(tagNumber),
                        "delta": None,
                    }
                )
            else:
                numbers.append(tagNumber)

        return found

    return loopAlbums(rootDir, cb)


def process(rootDir: str) -> int:
    conflicts = findConflictedTrackNumber(rootDir)

    def suggest(issue: Issue) -> list[Option]:
        entry = issue["entry"]
        split = parseTrackPath(entry.path, rootDir)

        results = tidal.searchTrack(
            split["track"]["name"], split["album"]["name"], split["artist"]
        )
        suggestions: list[Option] = []
        for result in results:
            suggestions.append(
                {
                    "key": "NONE",
                    "display": blue(
                        result.name
                        + " by "
                        + result.artist.name
                        + " on "
                        + result.album.name
                        + ": "
                        + int(result.track_num)
                    ),
                    "value": result.track_num,
                }
            )
        return suggestions

    def cb(good: str, issue: Issue) -> None:
        track = issue["entry"]
        tag = getTrackNumberTag(track.path)
        if tag != good:
            setTrackNumberTag(track.path, int(good))
            parts = splitFileName(track.path)
            if not parts:
                print("Problem tagging", issue["entry"])
                return
            newName = buildFileName(
                parts["dir"], int(good), parts["name"], parts["extension"]
            )
            os.rename(track, newName)

    def prompt(issue: Issue, index: int, count: int) -> str:
        return (
            promptHeader("conflictedTrackNumbers", index, count)
            + "\n"
            + "Two tracks with the same number at "
            + bold(stripRootPath(issue["entry"].path, rootDir))
        )

    return newFix(
        rootDir=rootDir,
        issues=conflicts,
        callback=cb,
        prompt=prompt,
        allowEdit=True,
        suggest=suggest,
    )
