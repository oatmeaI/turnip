from typing import Optional
import re
from utils.constants import trackPattern
from Path.AlbumPath import AlbumPath
from utils.path import joinPath, sanitizePathSegment


class TrackPath(AlbumPath):
    title: str
    trackNumber: Optional[str]
    disc: Optional[str]
    extension: str

    def __init__(self, fullPath: str):
        super(TrackPath, self).__init__(fullPath)
        fileName = self.pathObject.name
        matches = re.match(trackPattern, fileName)
        if matches:
            self.title = self.normalizeString(matches.group(3))
            self.trackNumber = matches.group(2)
            self.disc = matches.group(1)
            self.extension = matches.group(4)

    def setTitle(self, title: str):
        self.title = title
        self.move()

    def setTrackNumber(self, number: int):
        self.trackNumber = str(number)
        self.move()

    def buildPath(self):
        albumPath = super(TrackPath, self).buildPath()

        trackNumber = ''
        if self.trackNumber and int(self.trackNumber) > 0:
            trackNumber = str(self.trackNumber) + ' - '
            if len(trackNumber) > 0 and int(self.trackNumber) < 10 and not trackNumber.startswith('0'):
                trackNumber = '0' + trackNumber
            if self.disc:
                trackNumber = str(self.disc) + trackNumber

        discNumber = ''
        if self.disc and int(self.disc) > 0:
            discNumber = str(self.disc) + ' - '
            if len(discNumber) > 0 and int(self.disc) < 10:
                discNumber = '0' + discNumber

        numberSegment = discNumber + trackNumber
        fileName = (numberSegment + self.title + "." + self.extension) if self.title else ''
        strippedFilename = sanitizePathSegment(fileName)

        return joinPath([albumPath, strippedFilename])
