from internal_types import Issue
from utils.fs import loadTracks, loadFolders
from utils.userio import promptHeader, bold
from utils.util import newFix, loopArtists
from utils.tagging import setAlbumArtistTag, getAlbumArtistTag
from utils.path import parseTrackPath, stripRootPath
from tidal import tidal
import os


def findConflictedArtistTags(rootDir: str) -> list[Issue]:
    def cb(artist: os.DirEntry) -> list[Issue]:
        found: list[Issue] = []
        albums = loadFolders(artist.path)
        for album in albums:
            tracks = loadTracks(album.path)
            foundTag = None
            for track in tracks:
                artistTag = getAlbumArtistTag(track.path)
                issue: Issue = {
                    "data": None,
                    "entry": artist,
                    "original": foundTag,
                    "delta": artistTag,
                }
                if (
                    artistTag
                    and foundTag
                    and foundTag != artistTag
                    and issue not in found
                ):
                    found.append(issue)
                    break
                foundTag = artistTag
        return found

    return loopArtists(rootDir, cb)


def process(rootDir) -> int:
    conflicts = findConflictedArtistTags(rootDir)

    def suggest(issue: Issue):
        entry = issue["entry"]
        split = parseTrackPath(entry.path, rootDir)

        results = tidal.searchArtist(split["artist"])
        suggestions = []
        for result in results:
            suggestions.append(
                {
                    "key": "NONE",
                    "value": result.name,
                }
            )
        return suggestions

    def callback(good: str, issue: Issue):
        artist = issue["entry"]
        albums = loadFolders(artist.path)
        for album in albums:
            tracks = loadTracks(issue["entry"].path)
            for track in tracks:
                if getAlbumArtistTag(track.path) != good:
                    setAlbumArtistTag(track.path, good)

    def prompt(issue: Issue, index: int, count: int) -> str:
        return (
            promptHeader("artistTagConflicts", index, count)
            + "\n"
            + "Conflicted artist tags for artist "
            + bold(stripRootPath(issue["entry"].path, rootDir))
        )

    return newFix(
        rootDir=rootDir,
        issues=conflicts,
        prompt=prompt,
        callback=callback,
        allowEdit=True,
        suggest=suggest,
    )
