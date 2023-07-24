from thefuzz import fuzz
from titlecase import titlecase
from utils.fs import loadFolders, loadTracks
from utils.userio import chooseFromList, red, green, confirm
from utils.path import splitTrackName, stripRootPath
import json
from internal_types import Issue, Key, Option
from typing import Callable, Optional
import copy
import os


def loopArtists(rootDir: str, cb: Callable[[os.DirEntry], list]) -> list:
    i = 0
    artists = loadFolders(rootDir)
    results = []
    for artist in artists:
        # if artist.name != "All Time Low":
        #     continue
        i += 1
        results += cb(artist)
        # if i > 1:
        #     sys.stdout.write("\033[F")
        #     sys.stdout.write("\033[K")
        # if i > 20:
        # return results
        print(i, "/", len(artists), artist.name)
    return results


def loopAlbums(rootDir: str, cb: Callable[[os.DirEntry, os.DirEntry], list]) -> list:
    def loop(artist):
        results = []
        albums = loadFolders(artist.path)
        for album in albums:
            results += cb(artist, album)
        return results

    return loopArtists(rootDir, loop)


def loopTracks(
    rootDir: str, cb: Callable[[os.DirEntry, os.DirEntry, os.DirEntry], list]
) -> list:
    def loop(artist, album):
        results = []
        tracks = loadTracks(album.path)
        for track in tracks:
            results += cb(artist, album, track)
        return results

    return loopAlbums(rootDir, loop)


def compare(a: str, b: str) -> int:
    if splitTrackName(a) and splitTrackName(b):
        aScrubbed = splitTrackName(a)["name"].lower()
        bScrubbed = splitTrackName(b)["name"].lower()
    else:
        aScrubbed = a.lower()
        bScrubbed = b.lower()
    if (
        "remix" in aScrubbed
        and "remix" not in bScrubbed
        or ("remix" in bScrubbed and "remix" not in aScrubbed)
    ):
        return False
    ratio = fuzz.ratio(aScrubbed, bScrubbed)
    return ratio > 85


def compareDupes(dir: os.DirEntry, keys: list[Key], key: str) -> list[Issue]:
    dupes = filter(lambda d: compare(d["key"], key), keys)
    found: list[Issue] = []
    for dupe in dupes:
        found.append(
            {
                "data": None,
                "entry": dir,
                "original": dir.path,
                "delta": dupe["dir"].path,
            }
        )
    keys.append({"dir": dir, "key": key})
    return found


def readIgnoreCache():
    try:
        file = open("./ignoreCache.json", "r")
        ignoreCache = json.load(file)
        file.close()
        return ignoreCache
    except Exception:
        return []


def writeIgnoreCache(cache):
    file = open("./ignoreCache.json", "w")
    json.dump(cache, file)
    file.close()


ignoreCache = readIgnoreCache()


def findBad(issue: Issue, good: str) -> Optional[str]:
    return (
        issue["original"]
        if good == issue["delta"]
        else (issue["delta"] if good == issue["original"] else None)
    )


def check(issue: Issue) -> bool:
    if issue["original"] and not os.path.exists(issue["original"]):
        return False

    if issue["delta"] and not os.path.exists(issue["delta"]):
        return False
    return True


def buildOptions(
    issue: Issue,
    suggest: Callable[[Issue], list[Option]],
    heuristic: Callable[[list[Option]], Option],
    allowEdit: bool,
    skipIssueValues: bool,
    suggestionLimit: int,
    rootDir: str,
) -> list[Option]:
    options: list[Option] = []

    if issue["original"] and not skipIssueValues:
        options.append(
            {
                "key": "1",
                "value": issue["original"],
                "display": red(stripRootPath(issue["original"], rootDir)),
            }
        )

    if issue["delta"] and not skipIssueValues:
        options.append(
            {
                "key": "2",
                "value": issue["delta"],
                "display": green(stripRootPath(issue["delta"], rootDir)),
            }
        )

    suggestions = suggest(issue)

    i = 3
    end = max(len(suggestions) - 1, suggestionLimit)
    for suggestion in suggestions[0:end]:
        suggestion["key"] = str(i)
        options.append(suggestion)
        i += 1

    options.append({"key": "K", "value": "skipsimilar",
                   "display": "skip all similar"})
    options.append(
        {"key": "I", "value": "ignoresimilar", "display": "ignore all similar"}
    )
    options.append({"key": "s", "value": "skip", "display": "skip"})
    options.append({"key": "S", "value": "skip all", "display": "skip all"})
    options.append({"key": "i", "value": "ignore", "display": "ignore"})

    default = heuristic(options)

    if allowEdit:
        options.append({"key": "e", "value": "edit", "display": "edit"})

    if default:
        options.append(
            {"key": "", "value": default["value"],
                "display": default["display"]}
        )

    return options


def getInput(prompt=""):
    resp = False

    while not resp:
        print(prompt) if prompt else None
        value = input("> ")
        resp = confirm("Confirm " + value + "?", default=True)
    return value


def newFix(
    issues: list[Issue],
    prompt: Callable[[Issue, int, int], str],
    callback: Callable[[str, Issue], None],
    rootDir: str,
    heuristic: Callable[[list[Option]], Option] = lambda x: x[0],
    suggest: Callable[[Issue], list[Option]] = lambda x: [],
    check: Callable[[Issue], bool] = lambda x: True,
    allowEdit: bool = False,
    skipIssueValues: bool = False,
    suggestionLimit: int = 3,
) -> int:
    count = 0
    i = 0
    skipSimilar = []
    resolutions = {}

    def shouldProcess(issue: Issue) -> bool:
        ignoreIssue = copy.copy(issue)
        ignoreIssue["entry"] = issue["entry"].path

        if ignoreIssue in ignoreCache:
            return False

        similarKey = (issue["original"] or "") + ">" + (issue["delta"] or "")
        if similarKey in skipSimilar:
            return False

        if similarKey in ignoreCache:
            return False

        return True

    filteredIssues = list(filter(shouldProcess, issues))

    for issue in filteredIssues:
        i += 1
        ignoreIssue = copy.copy(issue)
        ignoreIssue["entry"] = issue["entry"].path
        if ignoreIssue in ignoreCache:
            continue

        if not check(issue):
            continue

        print(prompt(issue, i, len(filteredIssues)))

        options = buildOptions(
            issue,
            suggest,
            heuristic,
            allowEdit,
            skipIssueValues,
            suggestionLimit,
            rootDir,
        )

        # skip items with no suggestions except to skip
        if options[-1]["value"] == "skip":
            continue

        similarKey = (issue["original"] or "") + ">" + (issue["delta"] or "")
        if similarKey in skipSimilar:
            print("Skipping...")
            continue

        if similarKey in ignoreCache:
            continue

        print("")  # New line

        if similarKey in resolutions:
            print(
                "Similar resolution recorded for "
                + red(issue["original"] or "")
                + ": "
                + green(resolutions[similarKey])
            )
            useSimilar = confirm("Would you like to use this?", default=True)
            if useSimilar:
                callback(resolutions[similarKey], issue)
                continue

        resp = chooseFromList(options)

        if resp == "skip all":
            break

        if resp == "skip":
            continue

        if resp == "ignore":
            issue["entry"] = issue["entry"].path
            ignoreCache.append(issue)
            writeIgnoreCache(ignoreCache)
            continue

        if resp == "ignoresimilar":
            ignoreCache.append(similarKey)
            writeIgnoreCache(ignoreCache)
            continue

        if resp == "skipsimilar":
            skipSimilar.append(similarKey)
            continue

        if resp == "edit":
            resp = getInput()

        resolutions[similarKey] = resp

        callback(resp, issue)

        count += 1

    return count