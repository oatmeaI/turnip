from Command.Command import TrackCommand
from Command.Issue import TrackIssue
from Entry.Album import Album
from Entry.Artist import Artist
from Entry.Track import Track


class CheckFileNames(TrackCommand):
    def detectIssue(self, artist: Artist, album: Album, track: Track):
        builtPath = track.path.buildPath()
        print(builtPath, "\n", track.path.realPath)
        if builtPath != track.path.realPath:
            return TrackIssue(artist=artist, album=album, track=track, original=track.path.realPath, delta=builtPath)

    def heuristic(self, options):
        return options[1]

    def callback(self, good, issue: TrackIssue):
        if good != issue.track.path.realPath:
            issue.track.path.move()
