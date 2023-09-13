import os
from Command import Command
from Album import Album
from internal_types import Issue
from utils.util import loopAlbums
from utils.fs import loadTracks
from utils.tagging import getAlbumArtistTag
from utils.constants import rootDir
from tidal import tidal


class ArtistFolderConflicts(Command):
    cta = 'Conflict between artist tags and artist folder for album'
    allowEdit = True

    def findIssues(self) -> list[Issue]:
        def cb(artist, album) -> list[Issue]:
            found: list[Issue] = []
            tracks = loadTracks(album)
            for track in tracks:
                artistTag = getAlbumArtistTag(track.path)
                issue: Issue = {
                    'data': None,
                    'entry': album,
                    'original': artist.name,
                    'delta': artistTag,
                }
                if artistTag != artist.name and issue not in found:
                    found.append(issue)
            return found

        return loopAlbums(rootDir, cb)

    def suggest(self, issue: Issue):
        results = tidal.searchArtist(
            issue['original'],
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
        original = issue['original']
        delta = issue['delta']
        return (original and not delta) or (delta and not original)

    def check(self, issue: Issue) -> bool:
        if not os.path.exists(issue['entry']):
            return False
        return True

    def callback(self, good, issue: Issue) -> None:
        albumPath = issue['entry']
        album = Album(albumPath.path)
        album.setAlbumArtist(good)
