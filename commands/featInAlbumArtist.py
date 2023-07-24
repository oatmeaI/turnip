import re
import os
from internal_types import Issue
from utils.userio import promptHeader, bold
from utils.constants import featPattern
from utils.util import newFix, loopTracks
from utils.path import buildFileName, parseTrackPath, stripRootPath
from utils.tagging import (
    getAlbumArtistTag,
    setAlbumArtistTag,
    getArtistTag,
    setArtistTag,
)


def findFeatInAlbumArtist(rootDir: str) -> list[Issue]:
    def cb(artist: os.DirEntry, album: os.DirEntry, track: os.DirEntry) -> list[Issue]:
        found: list[Issue] = []
        parts = parseTrackPath(track.path, rootDir)
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
                "delta": re.sub(featPattern, r"\1\3", original),
                "data": str(matches.group(2)),
            }
        )
        return found

    return loopTracks(rootDir, cb)


def process(rootDir: str) -> int:
    issues = findFeatInAlbumArtist(rootDir)

    def cb(good: str, issue: Issue) -> None:
        track = issue["entry"]
        setAlbumArtistTag(track.path, good)

        print("Add featured artists to artist tag? (y/n)")
        resp = input("> ")
        while resp not in ["y", "n"]:
            resp = input("> ")
        if resp == "n":
            return
        artistTag = getArtistTag(track.path)
        newArtistTag = (artistTag or "") + ", " + (issue["data"] or "")
        print("Does this look right?", newArtistTag)
        resp = input("(y)es/(e)dit/(s)kip")
        while resp not in ["y", "e", "s"]:
            resp = input("> ")
        if resp == "e":
            newArtistTag = input("> ")
            print("Confirm", newArtistTag)
            resp = input("(y)es/(n)o")
            while resp not in ["y", "n"]:
                resp = input("(y)es/(n)o")
        if resp == "n":
            newArtistTag = input("> ")
        if resp == "y":
            setArtistTag(track.path, newArtistTag)

        parts = parseTrackPath(track.path, rootDir)
        if not parts:
            print("Error while parsing", track)
            return
        albumDir = (
            rootDir
            + "/"
            + good
            + "/"
            + parts["album"]["name"]
            + (("(" + parts["album"]["year"] + ")")
               if parts["album"]["year"] else "")
        )
        trackNumber = int(parts["track"]["number"]
                          ) if parts["track"]["number"] else 0
        extension = parts["track"]["extension"]

        destination = buildFileName(
            albumDir, trackNumber, parts["track"]["name"], extension
        )
        i = 1
        while os.path.exists(destination):
            destination = buildFileName(
                albumDir, trackNumber, good + " " + str(i), extension
            )
            i += 1
        if not os.path.exists(albumDir):
            os.makedirs(albumDir, exist_ok=True)
        os.rename(track, destination)

    def prompt(issue: Issue, index: int, count: int) -> str:
        return (
            promptHeader("featInAlbumArtist", index, count)
            + "\n"
            + "Possible featured artist found in album artist tag at "
            + bold(stripRootPath(issue["entry"].path, rootDir))
        )

    return newFix(
        rootDir=rootDir, issues=issues, callback=cb, prompt=prompt, allowEdit=True
    )
