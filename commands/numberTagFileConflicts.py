import os
from internal_types import Issue, Option
from utils.util import newFix, loopTracks
from utils.path import splitFileName, buildFileName, stripRootPath
from utils.tagging import (
    getTrackNumberTag,
    setTrackNumberTag,
)
from utils.userio import promptHeader, bold, blue
from tidal import tidal


def findConflictedTrackInPath(rootDir: str) -> list[Issue]:
    def cb(artist: os.DirEntry, album: os.DirEntry, track: os.DirEntry) -> list[Issue]:
        found: list[Issue] = []
        parts = splitFileName(track.path)
        if not parts:
            print("Error while parsing", track)
            return []
        fileNumber = parts["number"]
        tagNumber = getTrackNumberTag(track.path)

        if not fileNumber or not tagNumber or int(fileNumber) != int(tagNumber):
            found.append(
                {
                    "data": None,
                    "entry": track,
                    "original": str(int(fileNumber)) if fileNumber else None,
                    "delta": str(int(tagNumber)) if tagNumber else None,
                }
            )
        return found

    return loopTracks(rootDir, cb)


def process(rootDir: str) -> int:
    conflicts = findConflictedTrackInPath(rootDir)

    def suggest(issue: Issue) -> list[Option]:
        entry = issue["entry"]
        split = splitFileName(entry.path)

        if not split:
            return []

        results = tidal.searchTrack(
            split["title"], split["album"], split["artist"])
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
                        + str(result.track_num)
                    ),
                    "value": result.track_num,
                }
            )
        return suggestions

    def cb(good: str, issue: Issue) -> None:
        track = issue["entry"]
        if not os.path.exists(track):
            print("File not found")
            return
        parts = splitFileName(track.path)
        if not parts:
            print("Error while parsing", track)
            return
        fileNumber = int(parts["number"]) if parts["number"] else None
        print("filenumber", fileNumber)
        if int(good) == fileNumber:
            print("setting tag", good)
            setTrackNumberTag(track.path, int(good))
        else:
            parts["number"] = good
            newName = buildFileName(parts)
            os.rename(track, newName)

    def prompt(issue: Issue, index: int, count: int):
        return (
            promptHeader("numberTagFileConflicts", index, count)
            + "\n"
            + "Conflict between track number and file name for "
            + bold(stripRootPath(issue["entry"].path))
        )

    return newFix(
        issues=conflicts,
        callback=cb,
        prompt=prompt,
        allowEdit=True,
        suggest=suggest,
    )
