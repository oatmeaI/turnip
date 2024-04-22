from typing import Optional
from Command.Command import TrackCommand
from Command.Issue import TrackIssue
from Entry.Album import Album
from Entry.Artist import Artist
from Entry.Track import Track
from utils.constants import args


class SetCommand(TrackCommand):
    def detectIssue(self, artist: Artist, album: Album, track: Track) -> Optional[TrackIssue]:
        tagValue = track[args.tag]
        if tagValue != args.value:
            return TrackIssue(artist=artist, album=album, track=track, original=tagValue, delta=args.value)

    def heuristic(self, options):
        return options[1]

    def callback(self, good, issue: TrackIssue):
        print(good, args.value)
        if good == args.value:
            issue.track[args.tag] = good
