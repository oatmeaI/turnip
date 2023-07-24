import os
import re
from internal_types import Issue, Option
from utils.util import loopAlbums, newFix
from utils.path import getYearFromFolder, stripRootPath
from utils.fs import loadTracks
from utils.tagging import (
    getYearTag,
    setYearTag,
)
from utils.userio import promptHeader, bold, blue
from utils.path import parseTrackPath
from tidal import tidal


def findConflictedAlbumYears(rootDir: str) -> list[Issue]:
    def cb(artist: os.DirEntry, album: os.DirEntry) -> list[Issue]:
        found: list[Issue] = []
        tracks = loadTracks(album.path)
        foundYear = getYearFromFolder(album.name)
        for track in tracks:
            yearTag = getYearTag(track.path)
            issue: Issue = {
                "data": None,
                "entry": album,
                "original": str(foundYear),
                "delta": str(yearTag),
            }
            if yearTag != foundYear and issue not in found:
                found.append(issue)
        return found

    return loopAlbums(rootDir, cb)


def process(rootDir: str) -> int:
    conflicts = findConflictedAlbumYears(rootDir)

    def suggest(issue: Issue) -> list[Option]:
        entry = issue["entry"]
        split = parseTrackPath(entry.path, rootDir)

        results = tidal.searchAlbum(split["album"]["name"], split["artist"])
        suggestions: list[Option] = []
        for result in results:
            suggestions.append(
                {
                    "key": "NONE",
                    "display": blue(
                        result.name
                        + " by "
                        + result.artist.name
                        + ": "
                        + str(result.year)
                    ),
                    "value": result.year,
                }
            )
        return suggestions

    def cb(good: str, issue: Issue) -> None:
        album = issue["entry"]
        if not os.path.exists(album):
            return
        tracks = loadTracks(album.path)
        for track in tracks:
            yearTag = getYearTag(track.path)
            if yearTag != good:
                setYearTag(track.path, good)
        albumYear = getYearFromFolder(album.path)
        if albumYear != str(good):
            newName = (
                re.sub(r"\s?\(\d\d\d\d\)", "", album.path) +
                " (" + str(good) + ")"
            )
            os.rename(album, newName)

    def prompt(issue: Issue, index: int, count: int) -> str:
        return (
            promptHeader("yearTagFolderConflicts", index, count)
            + "\n"
            + "Conflict between album year tag and album year in path for album at "
            + bold(stripRootPath(issue["entry"].path, rootDir))
        )

    def heuristic(options: list[Option]) -> Option:
        for option in options:
            if option["value"].isdigit() and int(option["value"]) > 0:
                return option
        return options[0]

    return newFix(
        rootDir=rootDir,
        issues=conflicts,
        callback=cb,
        heuristic=heuristic,
        prompt=prompt,
        allowEdit=True,
        suggest=suggest,
    )
