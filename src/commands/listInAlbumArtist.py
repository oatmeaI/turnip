from Command.Command import TrackCommand
from Command.Issue import TrackIssue
from Command.Option import Option
from Entry.Album import Album
from Entry.Artist import Artist
from Entry.Track import Track
from utils.userio import bold, confirm
from utils.util import getInput


class ListInAlbumArtist(TrackCommand):
    edits = {}

    def detectIssue(self, artist: Artist, album: Album, track: Track):
        tag = track.albumArtist

        if not tag or "," not in tag:
            return None

        artists = tag.split(", ")

        return TrackIssue(
                artist=artist,
                album=album,
                track=track,
                original=tag,
                delta=artists[0],
                data=" · ".join(artists[1:]),
        )

    def callback(self, good: str, issue: TrackIssue) -> None:
        track = issue.track

        artistTag = track.artist
        default = not issue.data or issue.data not in artistTag
        shouldUpdateArtist = confirm(
            "Add featured artists to artist tag: " + bold(artistTag) + "?",
            default=default,
        )
        if not shouldUpdateArtist:
            return

        newArtistTag = " · ".join([artistTag, (issue.data or "")])

        existingEdit = newArtistTag in self.edits

        resp = confirm(
            "Does this look right? " + bold(newArtistTag), default=not existingEdit
        )
        if not resp:
            useExisting = (
                confirm("Use existing correction " +
                        self.edits[newArtistTag], default=True)
                if existingEdit
                else False
            )
            editedArtistTag = (
                self.edits[newArtistTag]
                if useExisting
                else getInput("Enter your correction")
            )
            self.edits[newArtistTag] = editedArtistTag
            track.setArtist(editedArtistTag)
        else:
            track.setArtist(newArtistTag)

        track.setAlbumArtist(good)

    def heuristic(self, options: list[Option]) -> Option:
        return options[1]
