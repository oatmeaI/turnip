import os
from Command import Command
from Album import Album
from Artist import Artist
from Issue import Issue
from utils.path import unsanitize
from utils.util import loopAlbums
from Song import Song
from utils.constants import rootDir
from tidal import tidal


class ArtistFolderConflictsIssue(Issue):
    data: str


class ArtistFolderConflicts(Command):
    cta = 'Conflict between artist tags and artist folder for album'
    allowEdit = True

    def findIssues(self) -> list[Issue]:
        def cb(artistDir, albumDir) -> list[Issue]:
            found: list[Issue] = []
            album = Album(albumDir.path)
            for track in album.tracks:
                song = Song(track.path)
                artistTag = song.tags._getAlbumArtist()
                folderName = unsanitize(album.getAlbumArtist(), artistTag)
                issue = ArtistFolderConflictsIssue(
                    data=artistDir.path,
                    entry=albumDir,
                    original=folderName,
                    delta=artistTag
                )
                if artistTag != folderName and issue not in found:
                    found.append(issue)

            return found

        return loopAlbums(rootDir, cb)

    def suggest(self, issue: Issue):
        results = tidal.searchArtist(
            issue.original,
        )
        suggestions = []
        for result in results:
            suggestions.append(
                {
                    'name': result.name,
                    'value': result.name,
                }
            )
        return suggestions

    def auto(self, issue):
        original = issue.original
        delta = issue.delta
        return (original and not delta) or (delta and not original)

    def check(self, issue: Issue) -> bool:
        if not os.path.exists(issue.entry):
            return False
        return True

    def callback(self, good, issue: ArtistFolderConflictsIssue) -> None:
        if good == issue.original:
            # We're updating tags
            albumPath = issue.entry
            album = Album(albumPath.path)
            album.setAlbumArtist(good)
        else:
            # We're updating filepath; do it at the artist folder level
            artist = issue.data
            artist = Artist(artist)
            artist.setName(good)
