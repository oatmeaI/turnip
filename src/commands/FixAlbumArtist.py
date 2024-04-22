from Command.Command import Command
from Command.Issue import Issue
from Entry.Album import Album
from Entry.Artist import Artist
from Entry.Track import Track
from utils.util import loopArtists
from utils.constants import rootDir


class AlbumArtistTagConflictsIssue(Issue):
    artist: Artist
    album: Album
    track: Track

    @property
    def key(self):
        return self.album.path.albumArtist + self.track.path.realPath + str(self.original) + str(self.delta)


class FixAlbumArtist(Command):
    cta = "Conflicted album artist tags for artist at "

    def findIssues(self) -> list[Issue]:
        def cb(artist: Artist) -> list[Issue]:
            found: list[Issue] = []
            folderArtist = artist.path.albumArtist
            for album in artist.albums:
                if len(album.tracks) < 1:
                    continue
                foundTag = album.tracks[0].tags.albumArtist
                for track in album.tracks:
                    artistTag = track.tags.albumArtist

                    if foundTag != artistTag:
                        issue = AlbumArtistTagConflictsIssue(
                            artist=artist,
                            track=track,
                            album=album,
                            original=foundTag,
                            delta=artistTag
                        )
                        found.append(issue)
                        break
                    elif folderArtist != artistTag:
                        issue = AlbumArtistTagConflictsIssue(
                            artist=artist,
                            track=track,
                            album=album,
                            original=folderArtist,
                            delta=artistTag
                        )
                        found.append(issue)
                        break

                    foundTag = artistTag
            return found

        return loopArtists(rootDir, cb)

    def callback(self, good: str, issue: AlbumArtistTagConflictsIssue):
        artist = issue.artist
        for album in artist.albums:
            album.setAlbumArtist(good)
