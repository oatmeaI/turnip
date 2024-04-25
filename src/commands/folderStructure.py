from Command.Command import Command
from Command.Issue import Issue
from Entry.Artist import Artist
from utils.fs import loadTracks, loadFolders, moveDirFiles, rmDir
from utils.util import loopArtists
from utils.constants import rootDir


class FolderStructure(Command):
    cta = "Found an issue with the folder structure"

    def checkStructure(self, artist: Artist) -> list[Issue]:
        found: list[Issue] = []
        tracks = loadTracks(artist.path.realPath)
        if len(tracks) > 0:
            artistIssue = Issue(
                    artist=artist,
                    delta="Create unnamed album",
                    original="Ignore",
                    data="artist"
                    )
            found.append(artistIssue)

        for album in artist.albums:
            subDirs = loadFolders(album.path.realPath)
            if len(subDirs) > 0:
                issue = Issue(
                    album=album,
                    data="album",
                    original="Ignore",
                    delta="Move to album root"
                )
                found.append(issue)

        return found

    def findIssues(self) -> list[Issue]:
        return loopArtists(rootDir, self.checkStructure)

    def callback(self, good, issue: Issue) -> None:
        if (good == "Ignore"):
            return # TODO - cache this
        if (good == "Move to album root"):
            subDirs = loadFolders(issue.entry.path.realPath)
            for dir in subDirs:
                moveDirFiles(dir.path, issue.entry.path.realPath)
                rmDir(dir.path)


# def verify(rootDir: str) -> None:
#     def cb(artist: os.DirEntry):
#         found = []
#         tracks = loadTracks(artist.path)
#         if len(tracks) > 0:
#             found.append(
#                 {"entry": artist.path, "type": "artist", "tracks": len(tracks)}
#             )
#         albums = loadFolders(artist.path)
#         for album in albums:
#             subDirs = loadFolders(album.path)
#             if len(subDirs) > 0:
#                 found.append(
#                     {"entry": album.path, "type": "album",
#                         "dirs": len(subDirs)}
#                 )
#         return found
#
#     found = loopArtists(rootDir, cb)
#
#     if len(found):
#         print(found)
#         raise "Folder structure problems detected; we can't fix these for you yet."
