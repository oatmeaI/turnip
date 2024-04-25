from utils.constants import albumPattern
import re
from Path.ArtistPath import ArtistPath
from utils.path import joinPath, sanitizePathSegment


class AlbumPath(ArtistPath):
    album: str
    year: str

    def __init__(self, fullPath: str):
        super(AlbumPath, self).__init__(fullPath)

        self.year = ''
        fullAlbum = self.parentPathParts[1]
        albumMatches = re.match(albumPattern, fullAlbum)
        if not albumMatches:
            pathAlbum = fullAlbum
        else:
            pathAlbum = albumMatches.group(1)
            self.year = albumMatches.group(2)
        self.album = self.normalizeString(pathAlbum)

    def setAlbum(self, album: str):
        self.album = album
        self.move()

    def setYear(self, year: str):
        self.year = year
        self.move()

    def buildPath(self):
        artistPath = super(AlbumPath, self).buildPath()
        if self.year:
            albumPath = self.album + ' (' + str(self.year)[0:4] + ')'
        else:
            albumPath = self.album

        return joinPath([artistPath, sanitizePathSegment(albumPath)])
