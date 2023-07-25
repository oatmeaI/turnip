import os
from internal_types import Issue, Option
from utils.util import loopAlbums, newFix
from utils.fs import loadTracks, moveDirFiles
from utils.tagging import getAlbumTag, setAlbumTag
from utils.userio import promptHeader, bold, blue
from utils.path import splitFileName, stripRootPath, setAlbumInPath
from tidal import tidal


def findConflictedAlbumFolders(rootDir: str) -> list[Issue]:
    def cb(artist, album) -> list[Issue]:
        found: list[Issue] = []
        tracks = loadTracks(album)
        for track in tracks:
            albumTag = getAlbumTag(track.path)
            if not albumTag:
                continue
            scrubbedTag = albumTag.replace("/", "_")
            parts = splitFileName(album.path[album.path.rindex("/") + 1:])

            if not parts:
                return found

            issue: Issue = {
                "data": None,
                "entry": album,
                "original": parts["album"],
                "delta": albumTag,
            }
            if scrubbedTag != parts["album"] and issue not in found:
                found.append(issue)
        return found

    return loopAlbums(rootDir, cb)


def process(rootDir: str) -> int:
    conflicts = findConflictedAlbumFolders(rootDir)

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
                    "display": blue(result.name + " by " + result.artist.name),
                    "value": result.name,
                }
            )
        return suggestions

    def cb(good, issue: Issue) -> None:
        album = issue["entry"]
        parts = splitFileName(
            album.path
        )  # TODO - not sure if this will work without a filename on the end

        if not parts:
            return

        albumName = parts["album"]
        tracks = loadTracks(album.path)

        for track in tracks:
            albumTag = getAlbumTag(track.path)
            if albumTag != good:
                setAlbumTag(track.path, good)

        if albumName != good:
            newDir = setAlbumInPath(album, good)

            if not os.path.exists(newDir):
                os.mkdir(newDir)
            moveDirFiles(album.path, newDir)

    def prompt(issue: Issue, index: int, count: int) -> str:
        return (
            promptHeader("albumTagFolderConflicts", index, count)
            + "\n"
            + "Album folder / tag mismatch for album at "
            + bold(stripRootPath(issue["entry"].path))
        )

    return newFix(
        issues=conflicts,
        callback=cb,
        prompt=prompt,
        allowEdit=True,
        suggest=suggest,
    )
