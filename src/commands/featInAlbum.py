import re
from typing import Optional
from Command.Command import Command
from Command.Issue import TrackIssue
from Command.Option import Option
from Entry.Album import Album
from Entry.Artist import Artist
from Entry.Track import Track
from utils.constants import rootDir
from utils.userio import bold,confirm
from utils.constants import featPattern
from utils.util import loopTracks, getInput


class FeatInAlbumIssue(TrackIssue):
    data: str


class FeatInAlbum(Command):
    def findIssues(self):
        def cb(artist: Artist, album: Album, track: Track) -> Optional[FeatInAlbumIssue]:
            tagName = track.album
            matches = re.match(featPattern, tagName)

            if not matches:
                return None

            return FeatInAlbumIssue(
                    artist=artist,
                    album=album,
                    track=track,
                    original=tagName,
                    delta=re.sub(featPattern, r"\1\3", tagName),
                    data=str(matches.group(2))
                    )

        return loopTracks(rootDir, cb)

    def callback(self, good, issue: FeatInAlbumIssue) -> None:
        track = issue.track
        track.setAlbum(good)

        artistTag = track.artist
        default = not issue.data or issue.data not in artistTag
        shouldUpdateArtist = confirm(
            "Add featured artists to artist tag: " + bold(artistTag) + "?",
            default=default,
        )
        if shouldUpdateArtist:
            if issue.data and issue.data in artistTag:
                artistTag = artistTag.replace(
                    " (ft. " + issue.data + ")", "")
            newArtistTag = (
                (artistTag or "")
                + " · "
                + (issue.data or "")
                .replace(" & ", " · ")
                .replace(" and ", " · ")
                .replace(", ", " · ")
            )
            resp = confirm("Does this look right? " +
                           bold(newArtistTag), default=True)
            if not resp:
                newArtistTag = getInput("Enter your correction")
            else:
                track.setArtist(newArtistTag)

    def heuristic(self, options: list[Option]) -> Option:
        for option in options:
            if not re.match(featPattern, option.value):
                return option
        return options[0]
