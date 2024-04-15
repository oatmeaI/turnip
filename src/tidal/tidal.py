import tidalapi
import pickle
import os
import urllib.parse
from utils.userio import blue

config = tidalapi.Config()
session = tidalapi.Session(config)
session.country_code = "US"


def getSession():
    if not os.path.exists("tidalSession.pickle"):
        return None
    with open("tidalSession.pickle", "rb") as f:
        return pickle.load(f)


def saveSession():
    with open("tidalSession.pickle", "wb") as f:
        pickle.dump(
            {"token_type": session.token_type, "access_token": session.access_token},
            f,
            protocol=pickle.HIGHEST_PROTOCOL,
        )


def login():
    oldSession = getSession()
    if not oldSession:
        session.login_oauth_simple()
        saveSession()
        return

    try:
        session.load_oauth_session(
            oldSession["token_type"], oldSession["access_token"])
    except:
        session.login_oauth_simple()
        saveSession()

    if not session.check_login():
        session.login_oauth_simple()
        saveSession()


def checkLogin():
    if not session.check_login():
        login()


def searchAlbum(album: str, artist: str):
    checkLogin()
    query = " ".join([album, artist])
    print("Searching Tidal with query: '" + blue(query) + "'")
    results = session.search(query, [tidalapi.album.Album])
    return results["albums"]


def searchArtist(artist):
    checkLogin()
    query = artist
    print("Searching Tidal with query: " + query)
    results = session.search(query, [tidalapi.artist.Artist])
    return results["artists"]


def searchTrack(track, album, artist):
    checkLogin()
    query = " ".join([track, artist])
    print("Searching Tidal with query: " + query)
    results = session.search(query, [tidalapi.media.Track])
    return filter(lambda r: r.album.name == album, results["tracks"])
