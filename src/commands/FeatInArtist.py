
import re
from typing import Optional
from Command.Command import Command
from Command.Issue import TrackIssue
from Command.Option import Option
from Entry.Album import Album
from Entry.Artist import Artist
from Entry.Track import Track
from utils.userio import bold, confirm
from utils.constants import featPattern, rootDir
from utils.util import loopTracks, getInput


class FeatInArtistIssue(TrackIssue):
    data: str


class FeatInArtist(Command):
    def findIssues(self) -> list[FeatInArtistIssue]:
        def cb(artist: Artist, album: Album, track: Track) -> Optional[FeatInArtistIssue]:

            matches = re.match(featPattern, track.artist)
            if not matches:
                return None

            return FeatInArtistIssue(
                    artist=artist,
                    album=album,
                    track=track,
                    original=track.artist,
                    delta=re.sub(featPattern, r'\1\3', track.artist),
                    data=str(matches.group(2)),
                )

        return loopTracks(rootDir, cb)

    def heuristic(self, options: list[Option]) -> Option:
        for option in options:
            if option.value and not re.match(featPattern, option.value):
                return option
        return options[0]

    def callback(self, good, issue: FeatInArtistIssue) -> None:
        track = issue.track

        track.setArtist(good)
        artistTag = track.artist

        # TODO - this logic is duplicated a bunch
        default = not issue.data or issue.data not in artistTag
        shouldUpdateArtist = confirm(
            'Add featured artists to artist tag: ' + bold(artistTag) + '?',
            default=default,
        )

        if shouldUpdateArtist:
            if issue.data and (issue.data in artistTag):
                artistTag = artistTag.replace(
                    ' (ft. ' + issue.data + ')', ''
                )
            newArtistTag = (
                (artistTag or '')
                + ' · '
                + (issue.data or '')
                .replace(' & ', ' · ')
                .replace(' and ', ' · ')
                .replace(', ', ' · ')
            )
            resp = confirm(
                'Does this look right? ' + bold(newArtistTag), default=True
            )
            if not resp:
                newArtistTag = getInput('Enter your correction')
            else:
                track.setArtist(newArtistTag)
