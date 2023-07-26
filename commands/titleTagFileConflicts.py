from titlecase import titlecase
from internal_types import Issue, Option
from Command import TrackCommand
from Song import Song
from utils.util import loopTracks, newFix
from utils.tagging import getTitleTag, setTitleTag
from utils.userio import promptHeader, bold
from utils.path import buildFileName, splitFileName, stripRootPath, renameFile
from tidal import tidal
import os


class TitleTagFileConflicts(TrackCommand):
    cta = "Conflict between track name and file name for: "
    allowEdit = True

    def detectIssue(self, artist, album, track):
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

    def check(self, issue: Issue) -> bool:
        return os.path.exists(issue["entry"])

    def suggest(self, issue: Issue) -> list[Option]:
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

    def callback(self, good: str, issue: Issue) -> None:
        track = Song(issue["entry"].path)

        if not os.path.exists(issue["entry"]):
            return

        track.setTitle(good)
