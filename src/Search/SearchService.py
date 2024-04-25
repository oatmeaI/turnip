from thefuzz import fuzz
from Entry.Album import Album
from Entry.Artist import Artist
from Entry.Track import Track
from Search.SearchGateway import SearchGateway
from Search.SearchResult import AlbumSearchResult, ArtistSearchResult, TrackSearchResult
from Search.Spotify.SpotifyGateway import SpotifyGateway
from Search.Tidal.TidalGateway import TidalGateway


class _SearchService:
    gateways: list[SearchGateway] = [TidalGateway(), SpotifyGateway()]

    def tearDown(self):
        for gateway in self.gateways:
            gateway.close()

    def searchArtist(self, artist: Artist) -> list[ArtistSearchResult]:
        results = []
        for gateway in self.gateways:
            results += gateway.searchArtist(artist)

        def sorter(result):
            return fuzz.ratio(result.artist, artist.path.albumArtist)

        results.sort(key=sorter, reverse=True)

        return results

    def searchAlbum(self, album: Album) -> list[AlbumSearchResult]:
        results = []
        for gateway in self.gateways:
            results += gateway.searchAlbum(album)

        def sorter(result):
            return fuzz.ratio(result.album, album.path.album) + fuzz.ratio(result.artist, album.path.albumArtist)

        results.sort(key=sorter, reverse=True)

        return results

    def searchTrack(self, track: Track) -> list[TrackSearchResult]:
        results = []
        for gateway in self.gateways:
            results += gateway.searchTrack(track)

        def sorter(result):
            return fuzz.ratio(result.track, track.title) + fuzz.ratio(result.album, track.album) + fuzz.ratio(result.artist, track.artist)

        results.sort(key=sorter, reverse=True)

        return results


SearchService = _SearchService()
