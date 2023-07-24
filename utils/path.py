from internal_types import TrackNameParts
from utils.fs import ensureDirExists
from utils.tagging import getTitleTag
from typing import Optional
import re
import os


def stripRootPath(string: str, rootDir: str):
    return re.sub(rootDir + "/", "", string)


# TODO - deprecate; make splitFileName do all
def getArtistFromPath(path: str, rootDir: str):
    albumName = getAlbumNameFromFolder(path[path.rindex("/") + 1:])
    raw = stripRootPath(path, rootDir)
    artistName = raw[: raw.index("/")]
    return {"album": albumName, "artist": artistName}


# TODO - deprecate; make splitFileName do all
def parseTrackPath(path: str, rootDir: str):
    raw = stripRootPath(path, rootDir)
    parts = raw.split("/")
    artist = parts[0]
    album = splitAlbumName(parts[1]) if len(parts) > 1 else None
    track = splitTrackName(parts[2]) if len(parts) > 2 else None

    return {"artist": artist, "album": album, "track": track}


# TODO - deprecate; make splitFileName do all
def getYearFromFolder(path: str) -> Optional[str]:
    matches = re.match(r".* \((\d\d\d\d)\)", path)
    if not matches:
        return None
    return matches.group(1)


# TODO - deprecate; make splitFileName do all
def getAlbumNameFromFolder(path: str) -> str:
    return re.sub(r"\s\([12]\d\d\d\)", "", path)


# TODO - deprecate; make splitFileName do all
def splitAlbumName(path: str):
    matches = re.match(r"(.*)\s\(([12]\d\d\d\))", path)
    if not matches:
        return {"name": path, "year": None}
    return {"name": matches.group(1), "year": matches.group(2)}


# TODO - deprecate; make splitFileName do all
def splitTrackName(path: str):
    matches = re.match(r"(\d*)[ -]{0,3}(.*)\.(.*)", path)

    if not matches:
        return None

    return {
        "name": matches.group(2),
        "number": matches.group(1),
        "extension": matches.group(3),
    }


# TODO - more sanitization, also maybe a map to go back to unsanitized?
# NOTE - can only do segments (b/c it escapes slashes)
def sanitizePathSegment(segment: str) -> str:
    replacement = "_"
    if segment.startswith("."):
        segment = replacement + segment[1:]
    return segment.replace("/", replacement)[:254]


def joinPath(parts: list[str]) -> str:
    seperator = "/"
    path = seperator.join(parts)
    return path


def createArtistDir(rootDir: str, artistName: str) -> str:
    sanitizedArtistName = sanitizePathSegment(artistName)
    path = joinPath([rootDir, sanitizedArtistName])
    ensureDirExists(path)
    return path


def setTitleInPath(track: os.DirEntry, title: str) -> str:
    parts = splitFileName(track.path)
    if not parts:
        return None
    return buildFileName(
        dir=parts["dir"],
        trackNumber=int(parts["number"]),
        name=title,
        extension=parts["extension"],
    )


# TODO - make this take os.DirEntry
def splitFileName(track: str) -> Optional[TrackNameParts]:
    matches = re.match(r"(\d*)[ -]{0,3}(.*)\.(.*)",
                       track[track.rindex("/") + 1:])
    dir = track[0: track.rindex("/")]

    if not matches:
        return None

    titleTag = getTitleTag(track)
    sanitizedTag = sanitizePathSegment(titleTag)
    fileName = matches.group(2)

    # Abstract the sanitization here so that we don't have to worry about it when doing comparisons elsewhere
    # TODO - do the same for album
    name = titleTag if sanitizedTag == fileName else fileName

    return {
        "dir": dir,
        "name": name,
        "number": matches.group(1),
        "extension": matches.group(3),
    }


def buildFileNameFromParts(parts):
    return buildFileName(
        dir=parts["dir"],
        trackNumber=int(parts["number"]),
        name=parts["name"],
        extension=parts["extension"],
    )


def buildFileName(dir: str, trackNumber: int, name: str, extension: str):
    number = str(trackNumber) if trackNumber else "00"

    if trackNumber and int(trackNumber) < 10:
        number = "0" + str(int(number))

    fileName = number + " - " + name + "." + extension
    strippedFilename = sanitizePathSegment(fileName)
    return dir + "/" + strippedFilename


def renameFile(file: os.DirEntry, destination: str):
    if file.path == destination:
        return

    i = 1
    parts = splitFileName(destination)

    while os.path.exists(destination):
        parts["name"] = parts["name"] + " " + str(i)
        destination = buildFileNameFromParts(parts)
        i += 1

    os.rename(file, destination)


def updateFileName(track: str, newName: str):
    parts = splitFileName(track)
    if not parts:
        print("Error while parsing", track)
        return

    fileName = parts["name"]
    albumDir = parts["dir"]
    trackNumber = int(parts["number"]) if parts["number"] else 0
    extension = parts["extension"]

    if newName == fileName:
        print("No diff found, skipping")
        return

    destination = buildFileName(albumDir, trackNumber, newName, extension)
    i = 1
    while os.path.exists(destination):
        destination = buildFileName(
            albumDir, trackNumber, newName + " " + str(i), extension
        )
        i += 1

    os.rename(track, destination)
