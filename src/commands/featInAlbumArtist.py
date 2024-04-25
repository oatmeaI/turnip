import re
from Command.Command import TrackCommand
from Command.Issue import TrackIssue
from Entry.Album import Album
from Entry.Artist import Artist
from Entry.Track import Track
from utils.userio import bold, confirm
from utils.constants import featPattern
from utils.util import getInput


class FeatInAlbumArtist(TrackCommand):
    def detectIssue(self, artist: Artist, album: Album, track: Track):
        fileName = track.path.albumArtist
        tagName = track.tags.albumArtist
        matches = re.match(featPattern, fileName)

        foundInFile = True
        if not matches and tagName:
            matches = re.match(featPattern, tagName)
            foundInFile = False

        if not matches:
            return None

        original = fileName if foundInFile else tagName

        return TrackIssue(
                artist=artist,
                album=album,
                track=track,
                original=original,
                delta=re.sub(featPattern, r"\1\3", original or ""),
                data=str(matches.group(2)),
            )

    def cb(self, good: str, issue: TrackIssue) -> None:
        # Update Album Artist tag
        track = issue.track

        # Add featured artists to artist tag
        artistTag = track.tags.artist
        default = not issue.data or (issue.data not in artistTag)

        shouldUpdateArtist = confirm(
            "Add featured artists to artist tag: " +
            bold(artistTag or "") + "?",
            default=default,
        )

        if shouldUpdateArtist:
            newArtistTag = (artistTag or "") + " · " + (issue.data or "")
            resp = confirm("Does this look right? " +
                           bold(newArtistTag), default=True)
            if not resp:
                newArtistTag = getInput("Enter your correction")
            else:
                track.setArtist(newArtistTag)

        track.setAlbumArtist(good)
