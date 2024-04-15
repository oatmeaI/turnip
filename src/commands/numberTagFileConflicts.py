import os
from Command import Command
from Issue import Issue
from Option import Option
from Song import Track
from utils.util import loopTracks
from utils.constants import rootDir
from tidal import tidal


class NumberConflictIssue(Issue):
    data: None
    entry: Track


class NumberTagFileConflicts(Command):
    cta = "Conflicted track number between filename and tags for"

    # TODO - move this out of Command and into Issue?
    def similar(self, issue: NumberConflictIssue):
        return False

    def skip(self, issue: NumberConflictIssue):
        return issue.entry.tags.album + issue.entry.tags.albumArtist

    def findIssues(self) -> list[NumberConflictIssue]:
        def cb(_, __, trackPath: os.DirEntry) -> list[NumberConflictIssue]:
            found: list[NumberConflictIssue] = []
            track = Track(trackPath.path)
            fileNumber = track.path.trackNumber
            tagNumber = track.tags.trackNumber

            if not fileNumber or not tagNumber or int(fileNumber) != int(tagNumber):
                issue = NumberConflictIssue(
                    data=None,
                    entry=track,
                    original=str(fileNumber) if fileNumber else '',
                    delta=str(tagNumber) if tagNumber else ''
                )
                found.append(issue)
            return found

        return loopTracks(rootDir, cb)

    def suggest(self, issue: NumberConflictIssue) -> list[Option]:
        track = issue.entry
        results = tidal.searchTrack(track.title, track.album, track.artist)
        suggestions: list[Option] = []
        for result in results:
            display = result.name + " by " + result.artist.name + " on " + result.album.name + ": " + str(result.track_num)
            option = Option(key="NONE", display=display, value=result.track_num)
            suggestions.append(option)
        return suggestions

    def callback(self, _good: str, issue: NumberConflictIssue) -> None:
        track = issue.entry
        good = int(_good)
        track.setTrackNumber(good)
