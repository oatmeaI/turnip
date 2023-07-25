from titlecase import titlecase
from internal_types import Issue, Option
from utils.util import loopTracks, newFix
from utils.tagging import getTitleTag, setTitleTag
from utils.userio import promptHeader, bold
from utils.path import buildFileName, splitFileName, stripRootPath, renameFile
from tidal import tidal
import os


def findConflictedTrackNames(rootDir: str) -> list[Issue]:
    def cb(artist: os.DirEntry, album: os.DirEntry, track: os.DirEntry) -> list[Issue]:
        found: list[Issue] = []
        parts = splitFileName(track.path)
        if not parts:
            return found
        fileName = parts["title"]
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
        split = splitFileName(entry.path)
        if not split:
            return []
        trackName = split["title"] if split["title"] else ""
        albumName = split["album"] if split["album"] else ""
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
        fileName = parts["title"]

        if getTitleTag(track.path) != good:
            setTitleTag(track.path, good)
        if fileName != good:
            parts["title"] = good
            destination = buildFileName(parts)
            renameFile(track, destination)

    def prompt(issue: Issue, index: int, count: int) -> str:
        return (
            promptHeader("titleTagFileConflicts", index, count)
            + "\n"
            + "Conflict between track name and file name for: "
            + bold(stripRootPath(issue["entry"].path))
        )

    return newFix(
        issues=conflicts,
        check=check,
        callback=cb,
        prompt=prompt,
        allowEdit=True,
    )
