from Path.Path import Path
from utils.constants import rootDir
from utils.path import joinPath, sanitizePathSegment


class ArtistPath(Path):
    albumArtist: str

    def __init__(self, fullPath: str):
        super(ArtistPath, self).__init__(fullPath)
        self.albumArtist = self.normalizeString(self.parentPathParts[0])

    def setAlbumArtist(self, artist: str):
        self.albumArtist = artist
        self.move()

    def buildPath(self):
        pathParts = [rootDir, sanitizePathSegment(self.albumArtist)]
        return joinPath(pathParts)
