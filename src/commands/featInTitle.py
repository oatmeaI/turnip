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


class FeatInTitleIssue(TrackIssue):
    data: str


class FeatInTitle(Command):
    def findIssues(self) -> list[FeatInTitleIssue]:
        def cb(artist: Artist, album: Album, track: Track) -> Optional[FeatInTitleIssue]:

            matches = re.match(featPattern, track.title)
            if not matches:
                return None

            return FeatInTitleIssue(
                    artist=artist,
                    album=album,
                    track=track,
                    original=track.title,
                    delta=re.sub(featPattern, r'\1\3', track.title),
                    data=str(matches.group(2)),
                )

        return loopTracks(rootDir, cb)

    def heuristic(self, options: list[Option]) -> Option:
        for option in options:
            if option.value and not re.match(featPattern, option.value):
                return option
        return options[0]

    def callback(self, good, issue: FeatInTitleIssue) -> None:
        track = issue.track
        artistTag = track.artist

        track.setTitle(good)

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
