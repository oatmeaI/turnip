import os
from typing import Union
from Command.Command import Command
from Command.Issue import Issue
from Entry.Artist import Artist
from utils.util import loopArtists, loopTracks
from utils.fs import loadTracks, loadFolders, rmDir, rmFile
from utils.path import stripRootPath
from utils.constants import rootDir
from utils.tagging import getAlbumArtistTag


class RemoveEmptyFolders(Command):
    def findIssues(self) -> list[Issue]:
        def cb(artist: Artist) -> Union[Issue, list[Issue]]:
            if len(artist.albums) < 1:
                return Issue(artist=artist, original=artist.path.realPath)

            found: list[Issue] = []
            for album in artist.albums:
                if len(album.tracks) < 1:
                    found.append(Issue(artist=artist, album=album, original=album.path.realPath))
            return found

        return loopArtists(rootDir, cb)

    def callback(self, good, issue):
        print("Trashing empty folder -> " + stripRootPath(issue.original))
        obj = issue.album or issue.artist
        rmDir(obj.path.realPath)



def fixBrokenFiles() -> int:
    count  = 0
    brokenFiles = []

    def cb(artist, album, track: os.DirEntry):
        try:
            getAlbumArtistTag(track.path)
        except Exception as e:
            print('exception', e)
            brokenFiles.append(track)
        return []

    loopTracks(rootDir, cb)

    for track in brokenFiles:
        rmFile(track.path)
        count += 1

    return count



def findEmptyFolders() -> list[os.DirEntry]:
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


def process() -> int:
    count = 0

    emptyFolders = findEmptyFolders()

    for folder in emptyFolders:
        print("Trashing empty folder -> " + stripRootPath(folder.path))
        rmDir(folder)
        count += 1

    return count
