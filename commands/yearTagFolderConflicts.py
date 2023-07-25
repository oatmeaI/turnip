import os
from internal_types import Issue, Option
from utils.util import loopAlbums, newFix
from utils.path import stripRootPath, splitFileName, setYearInPath, renameFile
from utils.fs import loadTracks
from utils.tagging import (
    getYearTag,
    setYearTag,
)
from utils.userio import promptHeader, bold, blue
from tidal import tidal


def findConflictedAlbumYears(rootDir: str) -> list[Issue]:
    def cb(artist: os.DirEntry, album: os.DirEntry) -> list[Issue]:
        found: list[Issue] = []
        tracks = loadTracks(album.path)
        parts = splitFileName(album.path)

        if not parts:
            return []

        foundYear = parts["year"]

        for track in tracks:
            yearTag = getYearTag(track.path)
            issue: Issue = {
                "data": None,
                "entry": album,
                "original": str(foundYear),
                "delta": str(yearTag) if yearTag else "",
            }
            if (yearTag or foundYear) and yearTag != foundYear and issue not in found:
                found.append(issue)
        return found

    return loopAlbums(rootDir, cb)


def process(rootDir: str) -> int:
    conflicts = findConflictedAlbumYears(rootDir)

    def suggest(issue: Issue) -> list[Option]:
        entry = issue["entry"]
        split = splitFileName(entry.path)

        if not split:
            return []

        results = tidal.searchAlbum(split["album"], split["artist"])
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
                print(track.name + " year: " + str(yearTag) + " -> ", str(good))
        parts = splitFileName(album.path)

        if not parts:
            return

        albumYear = parts["year"]
        if albumYear != str(good):
            newName = setYearInPath(album, good)
            if not newName:
                return
            print(album.name + " -> " + newName)
            renameFile(album, newName)

    def prompt(issue: Issue, index: int, count: int) -> str:
        return (
            promptHeader("yearTagFolderConflicts", index, count)
            + "\n"
            + "Conflict between album year tag and album year in path for album at "
            + bold(stripRootPath(issue["entry"].path))
        )

    def heuristic(options: list[Option]) -> Option:
        for option in options:
            if option["value"].isdigit() and int(option["value"]) > 0:
                return option
        return options[0]

    return newFix(
        issues=conflicts,
        callback=cb,
        heuristic=heuristic,
        prompt=prompt,
        allowEdit=True,
        suggest=suggest,
    )
