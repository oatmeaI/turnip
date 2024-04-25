from Command.Command import Command
from Command.Issue import TrackIssue
from Command.Option import Option
from Entry.Album import Album
from Entry.Artist import Artist
from Entry.Track import Track
from Search.SearchService import SearchService
from utils.util import loopTracks
from utils.constants import rootDir

# TODO heuristic


class NumberTagFileConflicts(Command):
    cta = "Conflicted track number between filename and tags for"

    # TODO - move this out of Command and into Issue?
    def similar(self, issue: TrackIssue):
        return False

    def skip(self, issue: TrackIssue):
        return issue.track.tags.album + issue.track.tags.albumArtist

    def findIssues(self) -> list[TrackIssue]:
        def cb(artist: Artist, album: Album, track: Track) -> list[TrackIssue]:
            found: list[TrackIssue] = []
            fileNumber = track.path.trackNumber
            tagNumber = track.tags.trackNumber

            if not fileNumber or not tagNumber or int(fileNumber) != int(tagNumber):
                issue = TrackIssue(
                    data=None,
                    artist=artist,
                    album=album,
                    track=track,
                    original=str(fileNumber) if fileNumber else '',
                    delta=str(tagNumber) if tagNumber else ''
                )
                found.append(issue)
            return found

        return loopTracks(rootDir, cb)

    def suggest(self, issue: TrackIssue) -> list[Option]:
        track = issue.track
        results = SearchService.searchTrack(track)
        suggestions: list[Option] = []
        for result in results:
            display = result.track + " by " + result.artist + " on " + result.album + ": " + str(result.trackNumber)
            option = Option(key="NONE", display=display, value=result.trackNumber)
            suggestions.append(option)
        return suggestions

    def callback(self, _good: str, issue: TrackIssue) -> None:
        track = issue.track
        good = int(_good)
        track.setTrackNumber(good)
