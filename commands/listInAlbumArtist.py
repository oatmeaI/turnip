import os
from internal_types import Issue, Option
from utils.tagging import (
    getAlbumArtistTag,
    setAlbumArtistTag,
    getArtistTag,
    setArtistTag,
)
from utils.userio import bold, promptHeader, confirm
from utils.util import newFix, loopTracks, getInput
from utils.path import (
    stripRootPath,
)


def findListInAlbumArtist(rootDir: str) -> list[Issue]:
    def cb(artist: os.DirEntry, album: os.DirEntry, track: os.DirEntry) -> list[Issue]:
        found: list[Issue] = []

        tag = getAlbumArtistTag(track.path)

        if not tag or "," not in tag:
            return []

        artists = tag.split(", ")

        found.append(
            {
                "entry": track,
                "original": tag,
                "delta": artists[0],
                "data": " · ".join(artists[1:]),
            }
        )
        return found

    return loopTracks(rootDir, cb)


def process(rootDir: str) -> int:
    issues = findListInAlbumArtist(rootDir)
    edits = {}

    def cb(good: str, issue: Issue) -> None:
        track = issue["entry"]

        setAlbumArtistTag(track.path, good)

        artistTag = getArtistTag(track.path) or ""
        default = not issue["data"] or issue["data"] not in artistTag
        shouldUpdateArtist = confirm(
            "Add featured artists to artist tag: " + bold(artistTag) + "?",
            default=default,
        )
        if not shouldUpdateArtist:
            return

        newArtistTag = " · ".join([artistTag, (issue["data"] or "")])

        existingEdit = newArtistTag in edits

        resp = confirm(
            "Does this look right? " + bold(newArtistTag), default=not existingEdit
        )
        if not resp:
            useExisting = (
                confirm("Use existing correction " +
                        edits[newArtistTag], default=True)
                if existingEdit
                else False
            )
            editedArtistTag = (
                edits[newArtistTag]
                if useExisting
                else getInput("Enter your correction")
            )
            edits[newArtistTag] = editedArtistTag
            setArtistTag(track.path, editedArtistTag)
        else:
            setArtistTag(track.path, newArtistTag)

    def heuristic(options: list[Option]) -> Option:
        return options[1]

    def prompt(issue: Issue, index: int, count: int) -> str:
        return (
            promptHeader("listInAlbumArtist", index, count)
            + "\n"
            + "Artist list found in album artist tag at: "
            + bold(stripRootPath(issue["entry"].path))
        )

    return newFix(
        issues=issues,
        callback=cb,
        prompt=prompt,
        heuristic=heuristic,
        allowEdit=True,
    )
