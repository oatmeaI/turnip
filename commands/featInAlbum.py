import re
import os
from internal_types import Issue, Option
from utils.userio import bold, promptHeader, confirm
from utils.constants import featPattern
from utils.util import newFix, loopTracks, getInput
from utils.path import (
    stripRootPath,
    setTitleInPath,
    renameFile,
)
from utils.tagging import (
    getArtistTag,
    setArtistTag,
    getAlbumTag,
    setAlbumTag,
)


def findFeatInAlbum(rootDir: str) -> list[Issue]:
    def cb(artist: os.DirEntry, album: os.DirEntry, track: os.DirEntry) -> list[Issue]:
        found: list[Issue] = []

        tagName = getAlbumTag(track.path) or ""
        matches = re.match(featPattern, tagName)

        if not matches:
            return []

        found.append(
            {
                "entry": track,
                "original": tagName,
                "delta": re.sub(featPattern, r"\1\3", tagName),
                "data": str(matches.group(2)),
            }
        )
        return found

    return loopTracks(rootDir, cb)


def process(rootDir: str) -> int:
    issues = findFeatInAlbum(rootDir)

    def cb(good, issue: Issue) -> None:
        track = issue["entry"]
        setAlbumTag(track.path, good)

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

        destination = setTitleInPath(track=track, title=good) or ""
        renameFile(file=track, destination=destination)

    def prompt(issue: Issue, index: int, count: int) -> str:
        return (
            promptHeader("featInAlbum", index, count)
            + "\n"
            + "Featured artist found in album tag at: "
            + bold(stripRootPath(issue["entry"].path))
        )

    def heuristic(options: list[Option]) -> Option:
        for option in options:
            if not re.match(featPattern, option["value"]):
                return option
        return options[0]

    return newFix(
        issues=issues,
        callback=cb,
        prompt=prompt,
        allowEdit=True,
        heuristic=heuristic,
    )
