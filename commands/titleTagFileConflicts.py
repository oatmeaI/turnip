import os
from internal_types import Issue, Option
from utils.util import loopTracks, newFix
from utils.tagging import getTitleTag, setTitleTag
from utils.userio import promptHeader, bold, blue
from utils.path import buildFileName, splitFileName, stripRootPath, parseTrackPath
from tidal import tidal
from titlecase import titlecase


def findConflictedTrackNames(rootDir: str) -> list[Issue]:
    def cb(artist: os.DirEntry, album: os.DirEntry, track: os.DirEntry) -> list[Issue]:
        found: list[Issue] = []
        parts = splitFileName(track.path)
        if not parts:
            return found
        fileName = parts["name"]
        tagName = getTitleTag(track.path)

        if fileName != tagName:
            found.append(
                {
                    "data": None,
                    "entry": track,
                    "original": tagName,
                    "delta": fileName,
                }
            )
        return found

    return loopTracks(rootDir, cb)


def process(rootDir: str) -> int:
    conflicts = findConflictedTrackNames(rootDir)

    def check(issue: Issue) -> bool:
        return os.path.exists(issue["entry"])

    def suggest(issue: Issue) -> list[Option]:
        entry = issue["entry"]
        split = parseTrackPath(entry.path, rootDir)
        if not split:
            return []
        trackName = split["track"]["name"] if split["track"] else ""
        albumName = split["album"]["name"] if split["album"] else ""
        results = tidal.searchTrack(trackName, albumName, split["artist"])
        suggestions: list[Option] = []
        for result in results:
            suggestions.append(
                {
                    "key": "NONE",
                    "display": result.name
                    + " by "
                    + result.artist.name
                    + " on "
                    + result.album.name,
                    "value": result.name,
                }
            )
        titleCasedOriginal = titlecase(issue["original"])
        titleCasedDelta = titlecase(issue["delta"])
        if titleCasedOriginal != issue["original"]:
            suggestions.append(
                {
                    "key": "NONE",
                    "display": titleCasedOriginal,
                    "value": titleCasedOriginal,
                }
            )
        if titleCasedDelta != issue["delta"]:
            suggestions.append(
                {"key": "NONE", "display": titleCasedDelta, "value": titleCasedDelta}
            )
        return suggestions

    def cb(good: str, issue: Issue) -> None:
        track = issue["entry"]
        if not os.path.exists(issue["entry"]):
            return
        parts = splitFileName(track.path)
        if not parts:
            print("Error while parsing", track)
            return
        fileName = parts["name"]
        albumDir = parts["dir"]
        trackNumber = int(parts["number"]) if parts["number"] else 0
        extension = parts["extension"]

        if getTitleTag(track.path) != good:
            setTitleTag(track.path, good)
        if fileName != good:
            destination = buildFileName(albumDir, trackNumber, good, extension)
            i = 1
            while os.path.exists(destination):
                destination = buildFileName(
                    albumDir, trackNumber, good + " " + str(i), extension
                )
                i += 1

            os.rename(track, destination)

    def prompt(issue: Issue, index: int, count: int) -> str:
        return (
            promptHeader("titleTagFileConflicts", index, count)
            + "\n"
            + "Conflict between track name and file name for: "
            + bold(stripRootPath(issue["entry"].path, rootDir))
        )

    return newFix(
        rootDir=rootDir,
        issues=conflicts,
        check=check,
        callback=cb,
        prompt=prompt,
        allowEdit=True,
    )
