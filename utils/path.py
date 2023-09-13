from internal_types import TrackNameParts
import shutil
from pathlib import Path
from utils.fs import ensureDirExists
from utils.tagging import getTitleTag, getAlbumTag, getAlbumArtistTag
from typing import Optional
from utils.constants import rootDir
import re
import os


def stripRootPath(string: str):
    stripped = re.sub(rootDir, '', string)
    return stripped[1:] if stripped.startswith('/') else stripped


def sanitizePathSegment(segment: str) -> str:
    replacement = '_'

    if segment.startswith('.'):
        segment = replacement + segment[1:]

    return segment.replace('/', replacement).replace(':', replacement)[:254]


def joinPath(parts: list[str]) -> str:
    seperator = '/'
    path = seperator.join(parts)
    return path


def createArtistDir(artistName: str) -> str:
    sanitizedArtistName = sanitizePathSegment(artistName)
    path = joinPath([rootDir, sanitizedArtistName])
    ensureDirExists(path)
    return path


def setAlbumInPath(path: os.DirEntry, album: str) -> Optional[str]:
    return setValueInPath(path, 'album', album)


def setYearInPath(path: os.DirEntry, year: str) -> Optional[str]:
    return setValueInPath(path, 'year', year)


def setArtistInPath(path: os.DirEntry, artist: str) -> Optional[str]:
    return setValueInPath(path, 'artist', artist)


def setTitleInPath(track: os.DirEntry, title: str) -> Optional[str]:
    return setValueInPath(track, 'title', title)


def setValueInPath(
    track: os.DirEntry, position: str, value: str
) -> Optional[str]:
    parts = splitFileName(track.path)

    if not parts:
        return None

    parts[position] = value  # TODO - typing

    return buildFileName(parts)


def unsanitize(pathValue: str, tagValue: str):
    sanitizedTagValue = sanitizePathSegment(tagValue)
    return tagValue if sanitizedTagValue == pathValue else pathValue


def splitFileName(fullPath: str) -> Optional[TrackNameParts]:
    # Setup
    lastSlashIndex = fullPath.rindex('/')
    fileName = fullPath[lastSlashIndex + 1:]

    # This is kinda janky
    # Get info from file path
    parentSubPath = stripRootPath(fullPath)
    parentPathParts = parentSubPath.split('/')
    pathType = len(parentPathParts)

    pathArtist = parentPathParts[0]
    pathAlbum = ''
    pathTitle = ''

    year = ''
    number = ''
    disc = ''
    extension = ''

    # Split year out of album folder name
    if pathType > 1:
        fullAlbum = parentPathParts[1]
        albumMatches = re.match(r'(.*)\s\(([12]\d\d\d)\)', fullAlbum)
        if not albumMatches:
            pathAlbum = fullAlbum
        else:
            pathAlbum = albumMatches.group(1)
            year = albumMatches.group(2)

    if pathType > 2:
        # Get info from filename
        matches = re.match(r'(?:(\d)-)?(\d*)[ -]{0,3}(.*)\.(.*)', fileName)
        if not matches:
            return None
        pathTitle = matches.group(3)
        number = matches.group(2)
        disc = matches.group(1)
        extension = matches.group(4)

    # Unsanitize the stuff that comes from file paths
    titleTag = ''
    albumTag = ''
    artistTag = ''
    if os.path.exists(fullPath) and pathType > 2:
        titleTag = getTitleTag(fullPath) or ''
        albumTag = getAlbumTag(fullPath) or ''
        artistTag = getAlbumArtistTag(fullPath) or ''
    album = unsanitize(pathAlbum, albumTag)
    artist = unsanitize(pathArtist, artistTag)
    title = unsanitize(pathTitle, titleTag) or ''

    return {
        'artist': artist,
        'album': album,
        'year': year,
        'disc': disc,
        'number': number,
        'title': title,
        'extension': extension,
    }


def buildFileName(parts: TrackNameParts) -> str:
    number = str(parts['number']) if parts['number'] else '00'

    if parts['number'] and int(parts['number']) < 10:
        number = '0' + str(int(number))
    discNumber = str(parts['disc']) + '-' if parts['disc'] is not None else ''
    fileName = discNumber + number + ' - ' + parts['title'] + '.' + parts['extension']
    strippedFilename = sanitizePathSegment(fileName) if parts['title'] else ''
    albumPath = (
        parts['album'] + ' (' + str(parts['year']) + ')'
        if parts['year']
        else parts['album']
    )

    path = joinPath(
        [
            rootDir,
            sanitizePathSegment(parts['artist']),
            sanitizePathSegment(albumPath),
            strippedFilename,
        ]
    )

    return path[:-1] if path.endswith('/') else path


def rename(fromPath: str, toPath: str) -> None:
    if fromPath == toPath or not os.path.exists(fromPath):
        return

    # TODO - probably a builtin to do this
    parent = toPath[: toPath.rindex('/')]
    if not os.path.exists(parent):
        Path(parent).mkdir(parents=True, exist_ok=True)

    shutil.move(fromPath, toPath)


def renameFile(file: str, destination: str):
    if file == destination:
        return

    i = 1
    parts = splitFileName(destination)

    if not parts:
        # TODO - throw error tbh
        return

    while os.path.exists(destination):
        parts['title'] = parts['title'] + ' ' + str(i)
        destination = buildFileName(parts)
        i += 1

    os.rename(file, destination)
