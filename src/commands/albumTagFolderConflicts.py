from Command.Command import Command
from Command.Issue import Issue
from Command.Option import Option
from Entry.Album import Album
from Entry.Artist import Artist
from utils.util import loopAlbums
from utils.userio import blue
from utils.constants import rootDir
from tidal import tidal

# TODO - heuristics for picking best choice


class AlbumTagFolderConflictsIssue(Issue):
    album: Album


class AlbumTagFolderConflicts(Command):
    allowEdit = True

    def findIssues(self):
        def cb(artist: Artist, album: Album) -> list[Issue]:
            found: list[Issue] = []
            for track in album.tracks:
                albumTag = track.tags.album

                if not albumTag:
                    continue

                issue = Issue(
                    album=album,
                    original=album.path.album,
                    delta=albumTag,
                    artist=artist
                )
                if albumTag != album.path.album and issue not in found:
                    found.append(issue)
            return found

        return loopAlbums(rootDir, cb)

    def suggest(self, issue: AlbumTagFolderConflictsIssue) -> list[Option]:
        album = issue.album.path.album
        results = tidal.searchAlbum(album, issue.album.path.albumArtist)
        suggestions: list[Option] = []
        for result in results:
            option = Option(
                    key="NONE",
                    display=blue(result.name + " by " + result.artist.name),
                    value=result.name
            )
            suggestions.append(option)
        return suggestions

    def callback(self, good, issue: AlbumTagFolderConflictsIssue) -> None:
        issue.album.setAlbum(good)
