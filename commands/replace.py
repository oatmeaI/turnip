from typing_extensions import TypedDict
from typing import Union, Callable, Dict
from utils.tagging import (
    getTitleTag,
    setTitleTag,
    getArtistTag,
    setArtistTag,
    getAlbumArtistTag,
    setAlbumArtistTag,
)
import os
from utils.util import newFix, loopTracks
from internal_types import Issue, Option
from utils.path import updateFileName, splitFileName, stripRootPath
from utils.userio import promptHeader, bold, red, green, yellow


Replacement = TypedDict(
    "Replacement",
    {"find": str, "replace": str,
        "search": Union[str, list[str]], "auto": bool},
)

replacements: list[Replacement] = [
    {"find": "remix", "replace": "Remix", "search": "all", "auto": False},
    {"find": " (Album Version)", "replace": "", "search": "all", "auto": True},
    {"find": "’", "replace": "'", "search": "all", "auto": True},
    {
        "find": "“",
        "replace": '"',
        "search": "all",
        "auto": True,
    },
    {"find": "”", "replace": '"', "search": "all", "auto": True},
]

TagFunc = TypedDict(
    "TagFunc", {"get": Callable[[str], str | None],
                "set": Callable[[str, str], None]}
)

tagFuncs: Dict[str, TagFunc] = {
    "title": {"get": getTitleTag, "set": setTitleTag},
    "artist": {"get": getArtistTag, "set": setArtistTag},
    "albumArtist": {"get": getAlbumArtistTag, "set": setAlbumArtistTag},
    "filename": {
        "get": lambda track: (splitFileName(track) or {"name": ""})["name"],
        "set": lambda track, newName: updateFileName(track, newName),
    },
}


def findReplacements(rootDir: str) -> list[Issue]:
    def cb(artist: os.DirEntry, album: os.DirEntry, track: os.DirEntry) -> list[Issue]:
        found: list[Issue] = []

        for replacement in replacements:
            searches = (
                tagFuncs.keys()
                if replacement["search"] == "all"
                else replacement["search"]
            )

            tags = []
            for search in searches:
                tags.append(
                    {"tag": search, "value": tagFuncs[search]["get"](
                        track.path)}
                )

            for tag in tags:
                if tag["value"] and replacement["find"] in tag["value"]:
                    replaced = tag["value"].replace(
                        replacement["find"], replacement["replace"]
                    )
                    issue: Issue = {
                        "entry": track,
                        "delta": replaced,
                        "original": tag["value"],
                        "data": tag["tag"],
                    }
                    if "auto" not in replacement or not replacement["auto"]:
                        issue["original"] = tag["value"]
                    found.append(issue)
        return found

    return loopTracks(rootDir, cb)


def process(rootDir: str) -> int:
    issues = findReplacements(rootDir)

    def prompt(issue: Issue, index: int, count: int) -> str:
        return (
            promptHeader("replace", index, count)
            + "\n"
            + "Replacement found at "
            + bold(stripRootPath(issue["entry"].path, rootDir))
            + "\n"
            + "Replace "
            + red(issue["original"] or "")
            + " with "
            + green(issue["delta"] or "")
            + " in "
            + yellow((issue["data"] or ""))
            + "?"
        )

    # print some info about what's current and what's new so I can know if I should skip or apply
    def cb(good: str, issue: Issue) -> None:
        track = issue["entry"]
        if not os.path.exists(track):
            return
        tag = issue["data"]
        if not tag:
            return
        print("Updating " + track.path + " - setting " + tag + " to " + good)
        tagFuncs[tag]["set"](track.path, good)
        if tag == "title":
            updateFileName(track.path, good)

    def heuristic(options: list[Option]) -> Option:
        return options[1]

    return newFix(
        rootDir=rootDir,
        issues=issues,
        prompt=prompt,
        callback=cb,
        allowEdit=True,
        heuristic=heuristic,
    )
