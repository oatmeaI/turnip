import os
from Command.Command import Command
from Command.Issue import TrackIssue
from Entry.Album import Album
from Entry.Artist import Artist
from Entry.Track import Track
from utils.compare import compare
from utils.constants import rootDir
from utils.util import loopTracks
from utils.path import stripRootPath
from utils.fs import rmFile


class TrackDuplicates(Command):
    cta = 'Possible duplicate tracks found. Select which to keep:'
    seen: list[Track]

    def findIssues(self) -> list[TrackIssue]:
        self.seen = []

        def cb(artist: Artist, album: Album, track: Track) -> list[TrackIssue]:
            found = []

            for otherTrack in self.seen:
                albumMatch = track.path.album == otherTrack.path.album
                artistMatch = track.path.albumArtist == otherTrack.path.albumArtist

                if albumMatch and artistMatch:
                    trackMatch = compare(track.path.title, otherTrack.path.title)
                    if trackMatch:
                        found.append(TrackIssue(
                            artist=artist,
                            album=album,
                            track=track,
                            original=otherTrack.path.realPath,
                            delta=track.path.realPath
                            ))

            self.seen.append(track)
            return found

        return loopTracks(rootDir, cb)

    def getFileSize(self, path):
        try:
            return round(os.path.getsize(path) / 1000000, 2)
        except Exception:
            return 0

    def heuristic(self, options):
        # TODO check bit rate here too
        largest = 0
        default = None
        for option in options:
            if not option['value'].startswith(rootDir):
                continue
            size = self.getFileSize(option['value'])
            if size > largest:
                largest = size
                default = option
        return default

    def optionString(self, optionValue):
        fileSize = self.getFileSize(optionValue)
        return stripRootPath(optionValue) + ' (' + str(fileSize) + 'mb)'

    def callback(self, good: str, issue: TrackIssue) -> None:
        if not os.path.exists(issue.original) or not os.path.exists(issue.delta):
            return
        if good == issue.original:
            rmFile(issue.delta)
        else:
            rmFile(issue.original)
