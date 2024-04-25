
from Command.Command import TrackCommand
from Command.Issue import TrackIssue
from Entry.Album import Album
from Entry.Artist import Artist
from Entry.Track import Track
from utils.fs import rmFile


class RemoveBrokenFiles(TrackCommand):
    def detectIssue(self, artist: Artist, album: Album, track: Track):
        try:
            titleTag = track.tags.title
            albumTag = track.tags.album
            artistTag = track.tags.artist
            albumArtistTag = track.tags.albumArtist
            if not titleTag and not albumTag and not artistTag and not albumArtistTag:
                return TrackIssue(artist=artist, album=album, track=track, original=track.path.realPath)
        except Exception as e:
            print('exception', e)
            return TrackIssue(artist=artist, album=album, track=track, original=track.path.realPath)
        return None

    def callback(self, good, issue=TrackIssue):
        if good == issue.track.path.realPath:
            rmFile(issue.track.path.realPath)
