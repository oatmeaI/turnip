import os
from Command import Command
from Album import Album
from internal_types import Issue
from utils.util import loopAlbums, newFix
from utils.fs import loadTracks, loadFolders, moveDirFiles
from utils.tagging import getAlbumArtistTag, setAlbumArtistTag
from utils.userio import promptHeader, bold
from utils.path import stripRootPath, createArtistDir
from utils.constants import rootDir
from tidal import tidal


class ArtistTagFolderConflicts(Command):
    cta = "Conflict between artist tags and artist folder for album"

    def findIssues(self) -> list[Issue]:
        def cb(artist, album) -> list[Issue]:
            found: list[Issue] = []
            tracks = loadTracks(album)
            for track in tracks:
                artistTag = getAlbumArtistTag(track.path)
                issue: Issue = {
                    "data": None,
                    "entry": artist,
                    "original": artist.name,
                    "delta": artistTag,
                }
                if artistTag != artist.name and issue not in found:
                    found.append(issue)
            return found

        return loopAlbums(rootDir, cb)

    def suggest(self, issue: Issue):
        entry = issue["entry"]
        results = tidal.searchAlbum(
            entry.name,
            stripRootPath(entry.path)[
                : entry.path.rindex("/") - 1
            ],  # TODO - use filename methods here instead
        )
        suggestions = []
        for result in results:
            suggestions.append(
                {
                    "name": result.name,
                    "value": result.name,
                }
            )
        return suggestions

    def check(self, issue: Issue) -> bool:
        if not os.path.exists(issue["entry"]):
            return False
        return True

    def callback(self, good, issue: Issue) -> None:
        artist = issue["entry"]
        albums = loadFolders(artist.path)
        for path in albums:
            album = Album(path.path)
            album.setAlbumArtist(good)


# def process(rootDir: str) -> int:
#     conflicts = findConflictedArtistFolders(rootDir)
#
#     def suggest(issue: Issue):
#         entry = issue["entry"]
#         results = tidal.searchAlbum(
#             entry.name,
#             stripRootPath(entry.path)[
#                 : entry.path.rindex("/") - 1
#             ],  # TODO - use filename methods here instead
#         )
#         suggestions = []
#         for result in results:
#             suggestions.append(
#                 {
#                     "name": result.name,
#                     "value": result.name,
#                 }
#             )
#         return suggestions
#
#     def check(issue: Issue) -> bool:
#         if not os.path.exists(issue["entry"]):
#             return False
#         return True
#
#     def cb(good, issue: Issue) -> None:
#         artist = issue["entry"]
#         artistName = artist.name
#         albums = loadFolders(artist.path)
#         for album in albums:
#             tracks = loadTracks(album.path)
#             for track in tracks:
#                 artistTag = getAlbumArtistTag(track.path)
#                 if artistTag != good:
#                     setAlbumArtistTag(track.path, good)
#
#         if artistName != good:
#             newDir = createArtistDir(artistName=good)
#             moveDirFiles(artist.path, newDir)
#
#     def prompt(issue: Issue, index: int, count: int):
#         return (
#             promptHeader("artistTagFolderConflicts", index, count)
#             + "\n"
#             + "Conflict between artist tags and artist folder for album "
#             + bold(issue["entry"].name)
#         )
#
#     return newFix(issues=conflicts, callback=cb, prompt=prompt, allowEdit=True)
