from utils.fs import loadTracks
from utils.tagging import getAlbumTag, setAlbumTag
from utils.util import loopAlbums, newFix
from typing import Optional
from internal_types import Issue, Option
from utils.userio import promptHeader, bold
from utils.path import parseTrackPath, stripRootPath
from tidal import tidal
import os


def findConflictedAlbums(rootDir) -> list[Issue]:
    def cb(artist: os.DirEntry, album: os.DirEntry) -> list[Issue]:
        tracks = loadTracks(album.path)
        found: list[Issue] = []
        foundTag = None
        for track in tracks:
            albumTag = getAlbumTag(track.path)
            if albumTag and foundTag and foundTag != albumTag:
                found.append(
                    {
                        "entry": album,
                        "original": foundTag,
                        "delta": albumTag,
                        "track": track.path,
                    }
                )
                break
            foundTag = albumTag
        return found

    return loopAlbums(rootDir, cb)


def process(rootDir) -> int:
    conflicts = findConflictedAlbums(rootDir)

    def suggest(issue: Issue) -> list[Option]:
        entry = issue["entry"]
        split = parseTrackPath(entry.path, rootDir)

        results = tidal.searchAlbum(split["album"]["name"], split["artist"])
        suggestions: list[Option] = []
        i = 3
        for result in results:
            suggestions.append(
                {"key": str(i), "value": result.name, "display": None})
            i += 1
        return suggestions

    def callback(good: str, issue: Issue) -> None:
        tracks = loadTracks(issue["entry"].path)
        for track in tracks:
            setAlbumTag(track.path, good)

    def prompt(issue: Issue, index: int, count: int) -> str:
        return (
            promptHeader("albumTagConflicts", index, count)
            + "\n"
            + "Conflicted album tags for album at "
            + bold(stripRootPath(issue["entry"].path, rootDir))
        )

    return newFix(
        rootDir=rootDir,
        issues=conflicts,
        callback=callback,
        prompt=prompt,
        allowEdit=True,
        suggest=suggest,
    )
