import re
import os
from internal_types import Issue, Option
from utils.userio import bold, promptHeader, confirm
from utils.constants import featPattern
from utils.util import newFix, loopTracks, getInput
from utils.path import (
    splitFileName,
    stripRootPath,
    setTitleInPath,
    renameFile,
)
from utils.tagging import getTitleTag, setTitleTag, getArtistTag, setArtistTag


def findFeatInTitle(rootDir: str) -> list[Issue]:
    def cb(artist: os.DirEntry, album: os.DirEntry, track: os.DirEntry) -> list[Issue]:
        found: list[Issue] = []
        parts = splitFileName(track.path)

        if not parts:
            return found

        fileName = parts["name"]
        tagName = getTitleTag(track.path)
        matches = re.match(featPattern, fileName)
        foundInFile = True
        if not matches and tagName:
            matches = re.match(featPattern, tagName)
            foundInFile = False
        if not matches:
            return []

        original = fileName if foundInFile else tagName

        if not original:
            return []

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
    issues = findFeatInTitle(rootDir)

    def cb(good, issue: Issue) -> None:
        track = issue["entry"]
        setTitleTag(track.path, good)

        artistTag = getArtistTag(track.path) or ""
        default = not issue["data"] or issue["data"] not in artistTag
        shouldUpdateArtist = confirm(
            "Add featured artists to artist tag: " + bold(artistTag) + "?",
            default=default,
        )
        if shouldUpdateArtist:
            if issue["data"] and issue["data"] in artistTag:
                artistTag = artistTag.replace(
                    " (ft. " + issue["data"] + ")", "")
            newArtistTag = (
                (artistTag or "")
                + " · "
                + (issue["data"] or "")
                .replace(" & ", " · ")
                .replace(" and ", " · ")
                .replace(", ", " · ")
            )
            resp = confirm("Does this look right? " +
                           bold(newArtistTag), default=True)
            if not resp:
                newArtistTag = getInput("Enter your correction")
            else:
                setArtistTag(track.path, newArtistTag)

        destination = setTitleInPath(track=track, title=good)
        renameFile(file=track, destination=destination)

    def prompt(issue: Issue, index: int, count: int) -> str:
        return (
            promptHeader("featInTitle", index, count)
            + "\n"
            + "Featured artist found in title tag at: "
            + bold(stripRootPath(issue["entry"].path, rootDir))
        )

    def heuristic(options: list[Option]) -> Option:
        for option in options:
            if not re.match(featPattern, option["value"]):
                return option
        return options[0]

    return newFix(
        rootDir=rootDir,
        issues=issues,
        callback=cb,
        prompt=prompt,
        allowEdit=True,
        heuristic=heuristic,
    )
