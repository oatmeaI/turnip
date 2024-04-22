from Command.Command import Command
from Command.Issue import Issue
from Command.Option import Option
from Entry.Album import Album
from Entry.Artist import Artist
from Entry.Track import Track
from utils.util import loopAlbums
from utils.constants import rootDir
from tidal import tidal


class AlbumTagConflictsIssue(Issue):
    artist: Artist
    album: Album
    track: Track

    @property
    def key(self):
        return 'albumTagConflict' + self.original + self.delta + self.track.path.title


class FixAlbum(Command):
    def findIssues(self) -> list[AlbumTagConflictsIssue]:
        def cb(artist: Artist, album: Album) -> list[Issue]:
            found: list[Issue] = []
            foundTag = None
            folderTitle = album.path.album

            for track in album.tracks:
                albumTag = track.tags.album
                if albumTag and foundTag and foundTag != albumTag:
                    found.append(AlbumTagConflictsIssue(
                        album=album,
                        original=foundTag,
                        delta=albumTag,
                        track=track,
                        artist=artist
                    ))
                    break
                elif folderTitle != albumTag and albumTag:
                    found.append(AlbumTagConflictsIssue(
                        album=album,
                        original=folderTitle,
                        delta=albumTag,
                        track=track,
                        artist=artist
                    ))
                    break

                foundTag = albumTag
            return found

        return loopAlbums(rootDir, cb)

    def suggest(self, issue: AlbumTagConflictsIssue) -> list[Option]:
        album = issue.album
        results = tidal.searchAlbum(album.path.album, album.path.albumArtist)
        suggestions: list[Option] = []
        for result in results:
            suggestions.append(Option(key="NONE", value=result.name, display=None))
        return suggestions

    def callback(self, good: str, issue: AlbumTagConflictsIssue) -> None:
        album = issue.album
        for track in album.tracks:
            track.setAlbum(good)
