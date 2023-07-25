from utils.fs import loadTracks
from utils.tagging import getTrackCountTag, setTrackCountTag
from utils.util import loopAlbums
from typing import Optional
from internal_types import Issue, Option
from utils.util import newFix
from utils.path import stripRootPath, splitFileName
from utils.userio import promptHeader, bold, blue
from tidal import tidal
import os


def detectConflictedTracks(
    album: os.DirEntry, tracks: list[os.DirEntry]
) -> Optional[Issue]:
    foundCount = 0
    for track in tracks:
        trackCount = getTrackCountTag(track.path)
        if foundCount != 0 and trackCount != foundCount:
            issue: Issue = {
                "data": None,
                "entry": album,
                "original": str(foundCount),
                "delta": str(trackCount) if trackCount else None,
            }
            return issue
        if foundCount == 0 and trackCount:
            foundCount = trackCount

    return None


def detectMissingTrackCount(album: os.DirEntry, tracks: list[os.DirEntry]) -> bool:
    tracks = loadTracks(album.path)
    for track in tracks:
        tracksTag = getTrackCountTag(track.path)
        if not tracksTag:
            continue
        if tracksTag:
            return False

    return True


def findConflictedTrackCounts(rootDir: str) -> list[Issue]:
    def cb(artist: os.DirEntry, album: os.DirEntry) -> list[Issue]:
        found: list[Issue] = []
        tracks = loadTracks(album.path)
        conflict = detectConflictedTracks(album, tracks)
        if conflict:
            found.append(conflict)
        return found

    return loopAlbums(rootDir, cb)


def process(rootDir: str) -> int:
    conflicts = findConflictedTrackCounts(rootDir)

    def suggest(issue: Issue) -> list[Option]:
        entry = issue["entry"]
        parts = splitFileName(entry.path)

        if not parts:
            return []

        results = tidal.searchAlbum(parts["album"], parts["artist"])
        suggestions: list[Option] = []
        for result in results:
            suggestions.append(
                {
                    "key": "NONE",
                    "display": blue(
                        result.artist.name
                        + " - "
                        + result.name
                        + ": "
                        + str(result.num_tracks)
                    ),
                    "value": result.num_tracks,
                }
            )
        return suggestions

    def callback(good: str, issue: Issue) -> None:
        tracks = loadTracks(issue["entry"].path)
        for track in tracks:
            setTrackCountTag(track.path, int(good))

    def prompt(issue: Issue, index: int, count: int) -> str:
        return (
            promptHeader("countTagConflicts", index, count)
            + "\n"
            + "Conflicted track count tags for album at "
            + bold(stripRootPath(issue["entry"].path))
        )

    return newFix(
        issues=conflicts,
        prompt=prompt,
        callback=callback,
        suggest=suggest,
        allowEdit=True,
    )
