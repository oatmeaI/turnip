import json
from typing import Any
import spotify.sync as spotify
from Entry.Album import Album
from Entry.Artist import Artist
from Entry.Track import Track
from Search.SearchGateway import SearchGateway
from Search.SearchResult import AlbumSearchResult, ArtistSearchResult, TrackSearchResult


class SpotifyGateway(SearchGateway):
    client: Any # TODO

    def __init__(self):
        with open('./spotify.json') as json_data:
            data = json.load(json_data)
            self.client = spotify.Client(data['client'], data['secret'])

    def close(self):
        self.client.close()

    def searchTrack(self, track: Track):
        query = " ".join([track.title, track.artist]).lower() # TODO - had to patch the spotify library to stop urlencoding the query because it was wrecking search results. probably should fork it or something
        print("Searching Spotify with query: " + query)
        results = self.client.search(query, types=['track'])

        tracks = []

        for result in results.tracks:
            artists = [x.name for x in result.artists]
            tracks.append(TrackSearchResult(artist=" • ".join(artists), album=result.album.name, track=result.name, trackNumber=result.track_number, year=result.album.release_date))

        return tracks

    def searchAlbum(self, album: Album):
        query = " ".join([album.path.album, album.path.albumArtist]).lower()
        print("Searching Spotify with query: " + query)
        results = self.client.search(query, types=['album'])

        albums = []

        for result in results.albums:
            artists = [x.name for x in result.artists]
            albums.append(AlbumSearchResult(artist=" • ".join(artists), album=result.name, year=result.release_date))

        return albums

    def searchArtist(self, artist: Artist):
        print("Searching Spotify with query: " + artist.path.albumArtist)
        results = self.client.search(artist.path.albumArtist, types=['album'])

        artists = []

        if not results.artists:
            return []

        for result in results.artists:
            artists.append(ArtistSearchResult(artist=result.name))

        return artists
