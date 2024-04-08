import os
from utils.fs import loadTracks, loadFolders, moveDirFiles
from utils.util import loopArtists
from utils.constants import rootDir
from Command import Command
from internal_types import Issue


class FolderStructure(Command):
    cta = "Found an issue with the folder structure"

    def similar(self, issue):
        return False

    def checkStructure(self, artist: os.DirEntry) -> list[Issue]:
        found: list[Issue] = []
        tracks = loadTracks(artist.path)
        if len(tracks) > 0:
            artistIssue: Issue = {
                    "entry": artist,
                    "delta": "Create unnamed album",
                    "original": "Ignore",
                    "data": "artist"
                    }
            found.append(artistIssue)

        albums = loadFolders(artist.path)
        for album in albums:
            subDirs = loadFolders(album.path)
            if len(subDirs) > 0:
                issue: Issue = {
                    "entry": album,
                    "data": "album",
                    "original": "Ignore",
                    "delta": "Move to album root"
                }
                found.append(issue)

        return found

    def findIssues(self) -> list[Issue]:
        return loopArtists(rootDir, self.checkStructure)

    def callback(self, good, issue: Issue) -> None:
        if (good == "Ignore"):
            return # TODO - cache this
        if (good == "Move to album root"):
            subDirs = loadFolders(issue["entry"].path)
            for dir in subDirs:
                moveDirFiles(dir.path, issue["entry"].path)



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
