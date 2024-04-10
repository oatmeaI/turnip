from typing import Optional
import pathlib
import re
import os
from utils.path import joinPath, rename, sanitizePathSegment, stripRootPath, unsanitize
from utils.constants import rootDir
from utils.loadTags import loadTags


class TrackNameParts:
    title: str
    trackNumber: Optional[str]
    disc: Optional[str]
    extension: str
    albumArtist: str
    album: str
    year: Optional[str]
    realPath: str

    def __init__(self, fullPath: str):
        self.year = None
        self.disc = None
        self.trackNumber = None
        self.realPath = fullPath

        # Setup
        strippedPath = stripRootPath(fullPath)
        path = pathlib.Path(strippedPath)
        self.extension = path.suffix
        fileName = path.name

        # This is kinda janky
        # Get info from file path
        parentPathParts = path.as_posix().split('/')
        pathType = len(parentPathParts)

        pathArtist = parentPathParts[0]
        pathAlbum = ''
        pathTitle = ''

        # Split year out of album folder name
        if pathType > 1:
            fullAlbum = parentPathParts[1]
            albumMatches = re.match(r'(.*)\s\(([12]\d\d\d)\)', fullAlbum)
            if not albumMatches:
                pathAlbum = fullAlbum
            else:
                pathAlbum = albumMatches.group(1)
                self.year = albumMatches.group(2)

        if pathType > 2:
            # Get info from filename
            matches = re.match(r'(?:(\d)-)?(\d*)[ -]{0,3}(.*)\.(.*)', fileName)
            if matches:
                pathTitle = matches.group(3)
                self.trackNumber = matches.group(2)
                self.disc = matches.group(1)
                self.extension = matches.group(4)

        # Unsanitize the stuff that comes from file paths
        titleTag = ''
        albumTag = ''
        artistTag = ''
        if os.path.exists(fullPath) and pathType > 2:
            tags = loadTags(fullPath)
            titleTag = tags.title or ''
            albumTag = tags.album or ''
            artistTag = tags.albumArtist or ''

        self.album = unsanitize(pathAlbum, albumTag)
        self.albumArtist = unsanitize(pathArtist, artistTag)
        self.title = unsanitize(pathTitle, titleTag) or ''

    def setAlbumArtist(self, artist: str):
        self.albumArtist = artist
        self.move()

    def setAlbum(self, album: str):
        self.album = album
        self.move()

    def setTitle(self, title: str):
        self.title = title
        self.move()

    def setTrackNumber(self, number: int):
        self.trackNumber = str(number)
        self.move()

    def move(self):
        newPath = self.buildPath()

        print(f"{stripRootPath(self.realPath)} -> {stripRootPath(newPath)}")

        rename(self.realPath, newPath)
        self.realPath = newPath

    def buildPath(self):
        trackNumber = ''
        if self.trackNumber and int(self.trackNumber) > 0:
            print(self.trackNumber)
            trackNumber = str(self.trackNumber) + ' - '
            if len(trackNumber) > 0 and int(self.trackNumber) < 10 and not trackNumber.startswith('0'):
                trackNumber = '0' + trackNumber

        discNumber = ''
        if self.disc and int(self.disc) > 0:
            discNumber = str(self.disc) + ' - '
            if len(discNumber) > 0 and int(self.disc) < 10:
                discNumber = '0' + discNumber

        numberSegment = discNumber + trackNumber
        fileName = numberSegment + self.title + "." + self.extension
        strippedFilename = sanitizePathSegment(fileName)

        if self.year:
            albumPath = self.album + ' (' + str(self.year) + ')'
        else:
            albumPath = self.album

        path = joinPath(
            [
                rootDir,
                sanitizePathSegment(self.albumArtist),
                sanitizePathSegment(albumPath),
                strippedFilename,
            ]
        )

        return path[:-1] if path.endswith('/') else path
