import os
from utils.util import loopArtists
from utils.fs import loadTracks, loadFolders, rmDir
from utils.path import stripRootPath


def findEmptyFolders(rootDir: str) -> list[os.DirEntry]:
    empties: list[os.DirEntry] = []

    def isEmpty(dir):
        if not os.path.exists(dir):
            return False
        return len(loadTracks(dir)) < 1 and len(loadFolders(dir)) < 1

    def cb(artist: os.DirEntry) -> list:
        if isEmpty(artist):
            empties.append(artist)
            return []

        albums = loadFolders(artist.path)
        found = False

        for album in albums:
            if not os.path.exists(album):
                continue
            if isEmpty(album):
                empties.append(album)
            else:
                found = True

        if not found:
            empties.append(artist)

        return []  # TODO - to make type annotation happy

    loopArtists(rootDir, cb)
    return empties


def process(rootDir: str) -> int:
    count = 0

    emptyFolders = findEmptyFolders(rootDir)

    for folder in emptyFolders:
        print("Trashing empty folder -> " + stripRootPath(folder.path))
        rmDir(folder)
        count += 1

    return count
