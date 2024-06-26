from typing import Optional
from Entry.Album import Album
from Entry.Artist import Artist
from Entry.Entry import Entry
from Entry.Track import Track


class Issue:
    track: Optional[Track]
    album: Optional[Album]
    artist: Optional[Artist]

    original: str
    delta: Optional[str]

    def __init__(self, original, delta=None, track=None, album=None, artist=None, data=None):
        self.original = original
        self.delta = delta
        self.data = data
        self.track = track
        self.album = album
        self.artist = artist

    @property
    def entry(self) -> Optional[Entry]:
        return self.track or self.album or self.artist

    @property
    def key(self):
        track = self.track.tags.title if self.track else ''
        album = self.album.path.album if self.album else ''
        artist = self.artist.path.albumArtist if self.artist else ''
        delta = self.delta or ''
        return self.original + delta + track + album + artist

    def __eq__(self, other):
        try:
            return self.key == other.key
        except AttributeError:
            return False

    # TODO - this is just for backward compat
    def __getitem__(self, key: str):
        match key:
            case 'data':
                return self.data
            case 'entry':
                return self.entry
            case 'original':
                return self.original
            case 'delta':
                return self.delta

    # TODO - this is just for backward compat
    def __setitem__(self, key: str, value):
        match key:
            case 'data':
                self.data = value
            case 'entry':
                self.entry = value
            case 'original':
                self.original = value
            case 'delta':
                self.delta = value


class ArtistIssue(Issue):
    artist: Artist

    @property
    def key(self):
        artist = self.artist.path.albumArtist if self.artist else ''
        delta = self.delta or ''
        return self.original + delta + artist


class AlbumIssue(ArtistIssue):
    album: Album

    @property
    def key(self):
        album = self.album.path.album if self.album else ''
        delta = self.delta or ''
        return self.original + delta + album


class TrackIssue(AlbumIssue):
    track: Track

    @property
    def key(self):
        track = self.track.tags.title if self.track else ''
        delta = self.delta or ''
        return self.original + delta
