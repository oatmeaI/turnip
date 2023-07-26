from internal_types import Issue, Option
from Command import Command
from Album import Album
from utils.fs import loadTracks, loadFolders
from utils.userio import promptHeader, bold
from utils.util import newFix, loopArtists
from utils.tagging import setAlbumArtistTag, getAlbumArtistTag
from utils.path import stripRootPath, splitFileName
from tidal import tidal
from utils.constants import rootDir
import os


class ArtistTagConflicts(Command):
    cta = "Conflicted album artist tags for artist at "

    def findIssues(self) -> list[Issue]:
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

    def callback(good: str, issue: Issue):
        artist = issue["entry"]
        albums = loadFolders(artist.path)
        for path in albums:
            album = Album(path.path)
            album.setAlbumArtist(good)


# def process(rootDir) -> int:
#     conflicts = findConflictedArtistTags(rootDir)
#
#     def suggest(issue: Issue) -> list[Option]:
#         entry = issue["entry"]
#         split = splitFileName(entry.path)
#
#         if not split:
#             return []
#
#         results = tidal.searchArtist(split["artist"])
#         suggestions: list[Option] = []
#         for result in results:
#             suggestions.append(
#                 {"key": "NONE", "value": result.name, "display": None})
#         return suggestions
#
#     def callback(good: str, issue: Issue):
#         artist = issue["entry"]
#         albums = loadFolders(artist.path)
#         for album in albums:
#             tracks = loadTracks(album.path)
#             for track in tracks:
#                 existingTag = getAlbumArtistTag(track.path) != good
#                 if existingTag != good:
#                     setAlbumArtistTag(track.path, good)
#
#     def prompt(issue: Issue, index: int, count: int) -> str:
#         return (
#             promptHeader("artistTagConflicts", index, count)
#             + "\n"
#             + "Conflicted album artist tags for artist at "
#             + bold(stripRootPath(issue["entry"].path))
#         )
#
#     return newFix(
#         issues=conflicts,
#         prompt=prompt,
#         callback=callback,
#         allowEdit=True,
#         suggest=suggest,
#     )
