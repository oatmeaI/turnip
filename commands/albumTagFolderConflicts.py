import os
from internal_types import Issue, Option
from utils.util import loopAlbums, newFix
from utils.fs import loadTracks, moveDirFiles
from utils.tagging import getAlbumTag, setAlbumTag
from utils.userio import promptHeader, bold, blue
from utils.path import getAlbumNameFromFolder, getYearFromFolder
from utils.path import parseTrackPath, stripRootPath
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
            albumName = getAlbumNameFromFolder(
                album.path[album.path.rindex("/") + 1:])
            issue: Issue = {
                "data": None,
                "entry": album,
                "original": albumName,
                "delta": albumTag,
            }
            if scrubbedTag != albumName and issue not in found:
                found.append(issue)
        return found

    return loopAlbums(rootDir, cb)


def process(rootDir: str) -> int:
    conflicts = findConflictedAlbumFolders(rootDir)

    def suggest(issue: Issue) -> list[Option]:
        entry = issue["entry"]
        split = parseTrackPath(entry.path, rootDir)

        results = tidal.searchAlbum(split["album"]["name"], split["artist"])
        suggestions: list[Option] = []
        i = 3
        for result in results:
            suggestions.append(
                {
                    "key": str(i),
                    "display": blue(result.name + " by " + result.artist.name),
                    "value": result.name,
                }
            )
            i += 1
        return suggestions

    def cb(good, issue: Issue) -> None:
        album = issue["entry"]
        albumName = getAlbumNameFromFolder(album.name)
        albumYear = getYearFromFolder(album.name)
        tracks = loadTracks(album.path)

        for track in tracks:
            albumTag = getAlbumTag(track.path)
            if albumTag != good:
                setAlbumTag(track.path, good)

        if albumName != good:
            path = stripRootPath(album.path, rootDir)
            artist = path[: path.index("/")]
            newDir = (
                rootDir
                + "/"
                + artist
                + "/"
                + good.replace("/", "_")
                + ((" (" + albumYear + ")") if albumYear else "")
            )
            if not os.path.exists(newDir):
                os.mkdir(newDir)
            moveDirFiles(album.path, newDir)

    def prompt(issue: Issue, index: int, count: int) -> str:
        return (
            promptHeader("albumTagFolderConflicts", index, count)
            + "\n"
            + "Album folder / tag mismatch for album at "
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
