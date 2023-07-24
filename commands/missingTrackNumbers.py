import os
from internal_types import Issue, Option
from utils.util import newFix, loopTracks
from utils.path import splitFileName, buildFileName, parseTrackPath, stripRootPath
from utils.tagging import (
    getTrackNumberTag,
    setTrackNumberTag,
)
from utils.userio import promptHeader, bold, blue
from tidal import tidal


def findMissingTrackNumber(rootDir: str) -> list[Issue]:
    def cb(artist: os.DirEntry, album: os.DirEntry, track: os.DirEntry) -> list[Issue]:
        found: list[Issue] = []
        tagNumber = getTrackNumberTag(track.path)
        fileNumber = parseTrackPath(track.path, rootDir)["track"]["number"]
        if not tagNumber and not fileNumber:
            found.append(
                {
                    "data": None,
                    "entry": track,
                    "original": None,
                    "delta": None,
                }
            )

        return found

    return loopTracks(rootDir, cb)


def process(rootDir: str) -> int:
    conflicts = findMissingTrackNumber(rootDir)

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
                    "display": bold(
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
                return
            newName = buildFileName(
                parts["dir"], int(good), parts["name"], parts["extension"]
            )
            os.rename(track, newName)

    def prompt(issue: Issue, index: int, count: int) -> str:
        return (
            promptHeader("missingTrackNumbers", index, count)
            + "\n"
            + "No track number for "
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
