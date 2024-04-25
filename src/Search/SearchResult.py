class ArtistSearchResult:
    artist: str

    def __init__(self, artist: str):
        self.artist = artist


class AlbumSearchResult(ArtistSearchResult):
    album: str
    year: str

    def __init__(self, artist: str, album: str, year: str):
        super().__init__(artist)
        self.album = album
        self.year = year


class TrackSearchResult(AlbumSearchResult):
    track: str
    trackNumber: str

    def __init__(self, artist: str, album: str, track: str, year: str, trackNumber: str):
        super().__init__(artist, album, year)
        self.track = track
        self.trackNumber = trackNumber
