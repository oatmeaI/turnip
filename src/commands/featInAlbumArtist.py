import re
import os
from internal_types import Issue
from utils.userio import promptHeader, bold, confirm
from utils.constants import featPattern
from utils.util import newFix, loopTracks, getInput
from utils.path import (
    stripRootPath,
    splitFileName,
    setArtistInPath,
    renameFile,
)
from utils.tagging import (
    getAlbumArtistTag,
    setAlbumArtistTag,
    getArtistTag,
    setArtistTag,
)


def findFeatInAlbumArtist(rootDir: str) -> list[Issue]:
    def cb(artist: os.DirEntry, album: os.DirEntry, track: os.DirEntry) -> list[Issue]:
        found: list[Issue] = []
        parts = splitFileName(track.path)
        if not parts:
            return []
        fileName = parts["artist"]
        tagName = getAlbumArtistTag(track.path)
        matches = re.match(featPattern, fileName)
        foundInFile = True
        if not matches and tagName:
            matches = re.match(featPattern, tagName)
            foundInFile = False
        if not matches:
            return []

        original = fileName if foundInFile else tagName

        found.append(
            {
                "entry": track,
                "original": original,
                "delta": re.sub(featPattern, r"\1\3", original or ""),
                "data": str(matches.group(2)),
            }
        )
        return found

    return loopTracks(rootDir, cb)


def process(rootDir: str) -> int:
    issues = findFeatInAlbumArtist(rootDir)

    def cb(good: str, issue: Issue) -> None:
        # Update Album Artist tag
        track = issue["entry"]
        setAlbumArtistTag(track.path, good)

        # Add featured artists to artist tag
        artistTag = getArtistTag(track.path) or ""
        default = not issue["data"] or (issue["data"] not in artistTag)

        shouldUpdateArtist = confirm(
            "Add featured artists to artist tag: " +
            bold(artistTag or "") + "?",
            default=default,
        )

        if shouldUpdateArtist:
            newArtistTag = (artistTag or "") + " · " + (issue["data"] or "")
            resp = confirm("Does this look right? " +
                           bold(newArtistTag), default=True)
            if not resp:
                newArtistTag = getInput("Enter your correction")
            else:
                setArtistTag(track.path, newArtistTag)

        # Update artist path
        parts = splitFileName(track.path)

        if not parts:
            print("Error while parsing", track)
            return

        newPath = setArtistInPath(track, good)
        renameFile(track, newPath)

    def prompt(issue: Issue, index: int, count: int) -> str:
        return (
            promptHeader("featInAlbumArtist", index, count)
            + "\n"
            + "Possible featured artist found in album artist tag at "
            + bold(stripRootPath(issue["entry"].path))
        )

    return newFix(issues=issues, callback=cb, prompt=prompt, allowEdit=True)
