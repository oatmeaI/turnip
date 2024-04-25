from Entry.Album import Album
from Entry.Artist import Artist
from Entry.Track import Track
from Search.SearchResult import AlbumSearchResult, ArtistSearchResult, TrackSearchResult


class SearchGateway:
    def close(self):
        pass

    def searchArtist(self, artist: Artist) -> list[ArtistSearchResult]:
        raise Exception('Not implemented')

    def searchAlbum(self, album: Album) -> list[AlbumSearchResult]:
        raise Exception('Not implemented')

    def searchTrack(self, track: Track) -> list[TrackSearchResult]:
        raise Exception('Not implemented')
