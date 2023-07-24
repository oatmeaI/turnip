from internal_types import Issue, Option
from utils.fs import loadTracks
from utils.userio import promptHeader, blue, bold
from utils.util import loopAlbums
from utils.tagging import getTrackCountTag, setTrackCountTag
from utils.path import parseTrackPath, stripRootPath
from utils.util import newFix
from tidal import tidal
import os


def findMissingTrackCounts(rootDir: str) -> list[Issue]:
    def cb(artist: os.DirEntry, album: os.DirEntry) -> list[Issue]:
        found: list[Issue] = []
        tracks = loadTracks(album.path)
        for track in tracks:
            trackCountTag = getTrackCountTag(track.path)
            if trackCountTag:
                return []
        found.append({"data": None, "entry": album,
                     "original": None, "delta": None})
        return found

    return loopAlbums(rootDir, cb)


def process(rootDir: str) -> int:
    conflicts = findMissingTrackCounts(rootDir)

    def suggest(issue: Issue) -> list[Option]:
        entry = issue["entry"]
        tags = parseTrackPath(entry.path, rootDir)
        results = tidal.searchAlbum(tags["album"]["name"], tags["artist"])
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
            promptHeader("missingTrackCounts", index, count)
            + "\n"
            + "Missing track count for album at "
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
