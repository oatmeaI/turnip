import tidalapi
import pickle
import os
from Entry.Album import Album
from Entry.Artist import Artist
from Entry.Track import Track
from Search.SearchGateway import SearchGateway
from Search.SearchResult import AlbumSearchResult, ArtistSearchResult, TrackSearchResult
from utils.userio import blue

config = tidalapi.Config()
session = tidalapi.Session(config)
session.country_code = "US"


class TidalGateway(SearchGateway):
    def getSession(self):
        if not os.path.exists("tidalSession.pickle"):
            return None
        with open("tidalSession.pickle", "rb") as f:
            return pickle.load(f)

    def saveSession(self):
        with open("tidalSession.pickle", "wb") as f:
            pickle.dump(
                {"token_type": session.token_type, "access_token": session.access_token},
                f,
                protocol=pickle.HIGHEST_PROTOCOL,
            )

    def login(self):
        oldSession = self.getSession()
        if not oldSession:
            session.login_oauth_simple()
            self.saveSession()
            return

        try:
            session.load_oauth_session(
                oldSession["token_type"], oldSession["access_token"])
        except:
            session.login_oauth_simple()
            self.saveSession()

        if not session.check_login():
            session.login_oauth_simple()
            self.saveSession()

    def checkLogin(self):
        if not session.check_login():
            self.login()

    def searchArtist(self, artist: Artist):
        self.checkLogin()
        query = artist.path.albumArtist
        print("Searching Tidal with query: " + query)
        results = session.search(query, [tidalapi.artist.Artist])

        artists = []
        for result in results["artists"]:
            artists.append(ArtistSearchResult(artist=result.name))

        return artists

    def searchAlbum(self, album: Album):
        self.checkLogin()
        query = " ".join([album.path.album, album.path.albumArtist])
        print("Searching Tidal with query: '" + blue(query) + "'")
        results = session.search(query, [tidalapi.album.Album])

        albums = []
        for result in results["albums"]:
            albums.append(AlbumSearchResult(artist=result.artist.name, album=result.name, year=result.release_date))

        return albums

    def searchTrack(self, track: Track):
        self.checkLogin()
        query = " ".join([track.artist, track.title]).lower()
        print("Searching Tidal with query: " + query)
        results = session.search(query, [tidalapi.media.Track])

        tracks = []
        for result in results["tracks"]:
            tracks.append(TrackSearchResult(artist=result.artist.name, album=result.album.name, track=result.name, trackNumber=result.track_num, year=result.album.release_date))

        return tracks
