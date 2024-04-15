import os
from Command.Command import Command
from Command.Issue import Issue
from Command.Option import Option
from Entry.Album import Album
from Entry.Artist import Artist
from utils.util import loopAlbums
from utils.constants import rootDir
from tidal import tidal


class AlbumArtistFolderConflictsIssue(Issue):
    artist: Artist
    album: Album


class AlbumArtistFolderConflicts(Command):
    cta = 'Conflict between album artist tags and artist folder for album'
    allowEdit = True

    def findIssues(self) -> list[Issue]:
        def cb(artist, album) -> list[Issue]:
            found: list[Issue] = []
            for track in album.tracks:
                albumArtistTag = track.tags.albumArtist
                folderName = album.path.albumArtist
                issue = AlbumArtistFolderConflictsIssue(
                    artist=artist,
                    album=album,
                    original=folderName,
                    delta=albumArtistTag
                )
                if albumArtistTag != folderName and issue not in found:
                    found.append(issue)

            return found

        return loopAlbums(rootDir, cb)

    def suggest(self, issue: Issue):
        results = tidal.searchArtist(
            issue.original,
        )
        suggestions = []
        for result in results:
            suggestions.append(Option(
                key=result.name,
                value=result.name,
                display=result.name
            ))
        return suggestions

    def auto(self, issue):
        original = issue.original
        delta = issue.delta
        return (original and not delta) or (delta and not original)

    def check(self, issue: Issue) -> bool:
        if not os.path.exists(issue.entry.path.realPath):
            return False
        return True

    def callback(self, good, issue: AlbumArtistFolderConflictsIssue) -> None:
        if good == issue.original:
            # We're updating tags
            album = issue.album
            album.setAlbumArtist(good)
        else:
            # We're updating filepath; do it at the artist folder level
            artist = issue.artist
            artist.setAlbumArtist(good)
