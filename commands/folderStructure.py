import os
from utils.fs import loadTracks, loadFolders
from utils.util import loopArtists


def verify(rootDir: str) -> None:
    def cb(artist: os.DirEntry):
        found = []
        tracks = loadTracks(artist.path)
        if len(tracks) > 0:
            found.append(
                {"entry": artist.path, "type": "artist", "tracks": len(tracks)}
            )
        albums = loadFolders(artist.path)
        for album in albums:
            subDirs = loadFolders(album.path)
            if len(subDirs) > 0:
                found.append(
                    {"entry": album.path, "type": "album",
                        "dirs": len(subDirs)}
                )
        return found

    found = loopArtists(rootDir, cb)

    if len(found):
        print(found)
        raise "Folder structure problems detected; we can't fix these for you yet."
