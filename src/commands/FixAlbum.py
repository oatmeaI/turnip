from Command.Command import Command
from Command.Issue import Issue, TrackIssue
from Command.Option import Option
from Entry.Album import Album
from Entry.Artist import Artist
from Search.SearchService import SearchService
from utils.util import loopAlbums
from utils.constants import rootDir


class FixAlbum(Command):
    def findIssues(self) -> list[TrackIssue]:
        def cb(artist: Artist, album: Album) -> list[Issue]:
            found: list[Issue] = []
            foundTag = None
            folderTitle = album.path.album

            for track in album.tracks:
                albumTag = track.tags.album
                if albumTag and foundTag and foundTag != albumTag:
                    found.append(TrackIssue(
                        album=album,
                        original=foundTag,
                        delta=albumTag,
                        track=track,
                        artist=artist
                    ))
                    break
                elif folderTitle != albumTag and albumTag:
                    found.append(TrackIssue(
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

    def suggest(self, issue: TrackIssue) -> list[Option]:
        album = issue.album
        results = SearchService.searchAlbum(album)
        suggestions: list[Option] = []
        for result in results:
            suggestions.append(Option(key="NONE", value=result.album, display=f"{result.album} by {result.artist} ({result.year})"))
        return suggestions

    def callback(self, good: str, issue: TrackIssue) -> None:
        album = issue.album
        for track in album.tracks:
            track.setAlbum(good)
