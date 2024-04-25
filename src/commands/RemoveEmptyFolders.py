from typing import Union
from Command.Command import Command
from Command.Issue import Issue
from Entry.Artist import Artist
from utils.util import loopArtists
from utils.fs import loadTracks, loadFolders, rmDir
from utils.path import stripRootPath
from utils.constants import rootDir


class RemoveEmptyFolders(Command):
    def findIssues(self) -> list[Issue]:
        def cb(artist: Artist) -> Union[Issue, list[Issue]]:
            if len(artist.albums) < 1:
                return Issue(artist=artist, original=artist.path.realPath)

            found: list[Issue] = []
            for album in artist.albums:
                if len(album.tracks) < 1:
                    found.append(Issue(artist=artist, album=album, original=album.path.realPath))

                subfolders = loadFolders(album.path.realPath)
                for subfolder in subfolders:
                    tracks = loadTracks(subfolder.path)
                    if len(tracks) < 1:
                        found.append(Issue(artist=artist, album=album, original=subfolder.path))

            return found

        return loopArtists(rootDir, cb)

    def callback(self, good, issue):
        print("Trashing empty folder -> " + stripRootPath(issue.original))
        rmDir(issue.original)
