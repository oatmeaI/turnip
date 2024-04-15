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
    entry: Album
    data: Track

    @property
    def key(self):
        return 'albumTagConflict' + self.original + self.delta + self.data.path.title


class AlbumTagConflicts(Command):
    def findIssues(self) -> list[AlbumTagConflictsIssue]:
        def cb(artist: Artist, album: Album) -> list[Issue]:
            found: list[Issue] = []
            foundTag = None
            for track in album.tracks:
                albumTag = track.tags.album
                if albumTag and foundTag and foundTag != albumTag:
                    found.append(AlbumTagConflictsIssue(
                        entry=album,
                        original=foundTag,
                        delta=albumTag,
                        data=track
                    ))
                    break
                foundTag = albumTag
            return found

        return loopAlbums(rootDir, cb)

    def suggest(self, issue: AlbumTagConflictsIssue) -> list[Option]:
        album = issue.entry
        results = tidal.searchAlbum(album.path.album, album.path.albumArtist)
        suggestions: list[Option] = []
        for result in results:
            suggestions.append(Option(key="NONE", value=result.name, display=None))
        return suggestions

    def callback(self, good: str, issue: AlbumTagConflictsIssue) -> None:
        album = issue.entry
        for track in album.tracks:
            track.setAlbum(good)
