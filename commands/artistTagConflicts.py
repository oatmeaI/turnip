from Artist import Artist
from Command import Command
from Issue import Issue
from utils.util import loopArtists
from utils.constants import rootDir
import os


class ArtistTagConflictsIssue(Issue):
    data: Artist


class ArtistTagConflicts(Command):
    cta = "Conflicted album artist tags for artist at "

    def findIssues(self) -> list[Issue]:
        def cb(artistDir: os.DirEntry) -> list[Issue]:
            artist = Artist(artistDir.path)
            found: list[Issue] = []
            for album in artist.albums:
                foundTag = album.tracks[0].tags._getAlbumArtist()
                for track in album.tracks:
                    artistTag = track.tags._getAlbumArtist()
                    issue = ArtistTagConflictsIssue(
                        data=artist,
                        entry=artistDir,
                        original=foundTag,
                        delta=artistTag
                    )
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

    def callback(self, good: str, issue: ArtistTagConflictsIssue):
        artist = issue.data
        for album in artist.albums:
            album.setAlbumArtist(good)
