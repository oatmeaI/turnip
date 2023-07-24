import os
from utils.util import loopArtists
from utils.fs import loadTracks, loadFolders, rmDir


def process(rootDir: str) -> int:
    count = 0

    def isEmpty(dir):
        if not os.path.exists(dir):
            return False
        return len(loadTracks(dir)) < 1 and len(loadFolders(dir)) < 1

    def cb(artist: os.DirEntry) -> list:
        nonlocal count
        if isEmpty(artist):
            print("\nRemoving " + artist.path + "\n")
            count += 1
            rmDir(artist)
            print("\nRemoving " + artist.path + "\n")
        else:
            albums = loadFolders(artist.path)
            found = False
            for album in albums:
                if not os.path.exists(album):
                    continue
                if isEmpty(album):
                    print("\nRemoving " + artist.path + "\n")
                    rmDir(album)
                else:
                    found = True
            if not found:
                count += 1
                rmDir(artist)
                print("\nRemoving " + artist.path + "\n")
        return []

    loopArtists(rootDir, cb)
    return count
