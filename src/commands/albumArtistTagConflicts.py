from Command.Command import Command
from Command.Issue import Issue
from Entry.Artist import Artist
from Entry.Track import Track
from utils.util import loopArtists
from utils.constants import rootDir


class AlbumArtistTagConflictsIssue(Issue):
    data: Artist
    entry: Track

    @property
    def key(self):
        return self.data.path.albumArtist + self.entry.path.realPath + str(self.original) + str(self.delta)


class AlbumArtistTagConflicts(Command):
    cta = "Conflicted album artist tags for artist at "

    def findIssues(self) -> list[Issue]:
        def cb(artist: Artist) -> list[Issue]:
            found: list[Issue] = []
            for album in artist.albums:
                if len(album.tracks) < 1:
                    continue
                foundTag = album.tracks[0].tags.albumArtist
                for track in album.tracks:
                    artistTag = track.tags.albumArtist
                    issue = AlbumArtistTagConflictsIssue(
                        data=artist,
                        entry=track,
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

    def callback(self, good: str, issue: AlbumArtistTagConflictsIssue):
        artist = issue.data
        for album in artist.albums:
            album.setAlbumArtist(good)
