import sys
from thefuzz import fuzz
from Command.Issue import Issue
from Command.Option import Option
from Entry.Album import Album
from Entry.Artist import Artist
from Entry.Track import Track
from utils.fs import loadFolders
from utils.userio import chooseFromList, red, green, confirm
from utils.path import stripRootPath, splitFileName
from utils.tagging import getTrackTime
from utils.constants import rootDir
import json
from typing import Callable, Optional
import copy
import os


def loopArtists(rootDir: str, cb: Callable[[Artist], list]) -> list:
    i = 0
    artists = loadFolders(rootDir)
    results = []
    for artist in artists:
        # if artist.name != "All Time Low":
        #     continue
        i += 1
        results += cb(Artist(artist.path))
        if i > 1:
            sys.stdout.write('\033[F')
            sys.stdout.write('\033[K')
        # if i > 1:
        # return results
        print(i, '/', len(artists), artist.name)
    return results


def loopAlbums(
    rootDir: str, cb: Callable[[Artist, Album], list]
) -> list:
    def loop(artist: Artist):
        results = []
        albums = artist.albums
        for album in albums:
            results += cb(artist, album)
        return results

    return loopArtists(rootDir, loop)


def loopTracks(
    rootDir: str, cb: Callable[[Artist, Album, Track], list]
) -> list:
    def loop(artist, album):
        results = []
        tracks = album.tracks
        for track in tracks:
            results += cb(artist, album, track)
        return results

    return loopAlbums(rootDir, loop)


def compare(a: os.DirEntry, b: os.DirEntry) -> int:
    THRESHOLD = 80
    aParts = stripRootPath(a.path).split('/')
    bParts = stripRootPath(b.path).split('/')
    ratio = 0

    pathType = len(aParts)

    artistAScrubbed = aParts[0].lower()
    artistBScrubbed = bParts[0].lower()

    if artistAScrubbed.startswith('the'):
        artistAScrubbed = artistAScrubbed[3:]
    if artistBScrubbed.startswith('the'):
        artistBScrubbed = artistBScrubbed[3:]

    artistRatio = fuzz.ratio(artistAScrubbed, artistBScrubbed)
    if artistRatio < THRESHOLD:
        return False

    if pathType == 1:
        return artistRatio > THRESHOLD

    if pathType == 2:
        albumAScrubbed = splitFileName(a.path)['album'].lower()
        albumBScrubbed = splitFileName(b.path)['album'].lower()
        ratio = fuzz.ratio(albumAScrubbed, albumBScrubbed)
        return ratio > THRESHOLD

    if pathType == 3:  # Track
        # Only detect dupes in same album - TODO - put this in a flag
        albumAScrubbed = splitFileName(a.path)['album'].lower()
        albumBScrubbed = splitFileName(b.path)['album'].lower()
        albumRatio = fuzz.ratio(albumAScrubbed, albumBScrubbed)

        titleAScrubbed = aParts[2].lower()
        titleBScrubbed = bParts[2].lower()

        if (
            'remix' in titleAScrubbed
            and 'remix' not in titleBScrubbed
            or ('remix' in titleBScrubbed and 'remix' not in titleAScrubbed)
        ):
            return False

        ratio = fuzz.ratio(titleAScrubbed, titleBScrubbed)
        if ratio > THRESHOLD and albumRatio > THRESHOLD:
            return True
            aLength = getTrackTime(a)
            bLength = getTrackTime(b)
            dupe = abs(aLength - bLength) < max(
                aLength / 100, 1
            )  # TODO - can play with these to tweak detection
            return dupe

        return False

    return False


def compareDupes(
    entry: os.DirEntry, seenEntries: list[str], key: str
) -> list[Issue]:
    def doCompare(seen: str):
        return compare(entry, seen['dir'])

    dupes = list(filter(doCompare, seenEntries))
    found: list[Issue] = []
    for dupe in dupes:
        issue = {
            'data': None,
            'entry': entry,
            'original': entry.path,
            'delta': dupe['dir'].path,
        }
        reverse = next(
            (
                x
                for x in found
                if x['original'] == issue['delta']
                and x['delta'] == issue['original']
            ),
            None,
        )
        if issue in found or reverse:
            continue
        found.append(issue)
    seenEntries.append({'dir': entry, 'key': key})
    return found


def readIgnoreCache():
    try:
        file = open('./ignoreCache.json', 'r')
        ignoreCache = json.load(file)
        file.close()
        return ignoreCache
    except Exception:
        return []


def writeIgnoreCache(cache):
    file = open('./ignoreCache.json', 'w')
    json.dump(cache, file)
    file.close()


ignoreCache = readIgnoreCache()


def findBad(issue: Issue, good: str) -> Optional[str]:
    return (
        issue['original']
        if good == issue['delta']
        else (issue['delta'] if good == issue['original'] else None)
    )


def check(issue: Issue) -> bool:
    if issue['original'] and not os.path.exists(issue['original']):
        return False

    if issue['delta'] and not os.path.exists(issue['delta']):
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
    optionString: Callable[[str], str],
) -> list[Option]:
    options: list[Option] = []

    if issue['original'] and not skipIssueValues:
        options.append(Option(
            key='1',
            value=issue.original,
            display=red(optionString(issue.original))
        ))

    if issue['delta'] and not skipIssueValues:
        options.append(Option(
            key=str(len(options) + 1),
            value=issue.delta,
            display=green(optionString(issue.delta)),
        ))

    suggestions = suggest(issue)

    i = len(options) + 1
    end = max(len(suggestions) - 1, suggestionLimit)
    for suggestion in suggestions[0:end]:
        suggestion['key'] = str(i)
        options.append(suggestion)
        i += 1

    options.append(Option(key='s', value='skip', display='skip'))
    options.append(
        Option(key='K', value='skipsimilar', display='skip all similar')
    )
    options.append(Option(key='I', value='ignoresimilar', display='ignore all similar'))
    options.append(Option(key='S', value='skip all', display='skip all'))
    options.append(Option(key='i', value='ignore', display='ignore'))

    default = heuristic(options)

    if allowEdit:
        options.append(Option(key='e', value='edit', display='edit'))

    if default:
        options.append(Option(key='', value=default['value'], display=default.display))

    return options


def getInput(prompt=''):
    resp = False

    value = ''
    while not resp:
        print(prompt) if prompt else None
        value = input('> ')
        resp = confirm('Confirm ' + value + '?', default=True)
    return value


def newFix(
    issues: list[Issue],
    prompt: Callable[[Issue, int, int], str],
    callback: Callable[[str, Issue], None],
    heuristic: Callable[[list[Option]], Option] = lambda x: x[0],
    suggest: Callable[[Issue], list[Option]] = lambda x: [],
    similar: Callable[[Issue], str] = lambda issue: (issue.original or '')
    + '>'
    + (issue['delta'] or ''),
    skip: Optional[Callable[[Issue], str]] = None,
    check: Callable[[Issue], bool] = lambda x: True,
    allowEdit: bool = False,
    skipIssueValues: bool = False,
    suggestionLimit: int = 3,
    auto: Callable[[Issue], bool] = lambda x: False,
    optionString: Callable[[str], str] = lambda x: x,
) -> int:
    count = 0
    i = 0
    skipSimilar = []
    resolutions = {}
    shouldUseSimilar = []

    def shouldProcess(issue: Issue) -> bool:
        ignoreIssue = copy.copy(issue)
        # ignoreIssue.entry = issue.entry.path

        if ignoreIssue in ignoreCache:
            return False

        similarKey = similar(issue)
        skipKey = skip(issue) if skip else similarKey
        if skipKey in skipSimilar:
            return False

        if skipKey in ignoreCache:
            return False

        return True

    filteredIssues = list(filter(shouldProcess, issues))

    for issue in filteredIssues:
        i += 1
        ignoreIssue = copy.copy(issue)
        # ignoreIssue['entry'] = issue['entry'].path
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
            optionString,
        )

        # skip items with no suggestions except to skip
        if options[-1]['value'] == 'skip':
            continue

        if not shouldProcess(issue):
            print('Skipping...')
            continue

        print('')  # New line

        autoResolve = auto(issue)
        defaultOption = heuristic(options)
        if autoResolve and defaultOption:
            resp = defaultOption.value
            callback(resp, issue)
            count += 1
            continue

        similarKey = similar(issue)
        skipKey = skip(issue) if skip else similarKey
        if similarKey and similarKey in resolutions:
            if similarKey in shouldUseSimilar:
                callback(resolutions[similarKey], issue)
                continue
            print(
                'Similar resolution recorded for '
                + red(issue.original or '')
                + ': '
                + green(resolutions[similarKey])
            )
            useSimilar = confirm('Would you like to use this?', default=True)
            if useSimilar:
                alwaysUseSimilar = confirm("Would you like to use this for all similar issues?", default=True)
                if alwaysUseSimilar:
                    shouldUseSimilar.append(similarKey)
                callback(resolutions[similarKey], issue)
                continue

        resp = chooseFromList(options)

        if resp == 'skip all':
            break

        if resp == 'skip':
            continue

        if resp == 'ignore':
            issue['entry'] = issue['entry'].path
            ignoreCache.append(issue)
            writeIgnoreCache(ignoreCache)
            continue

        if resp == 'ignoresimilar':
            ignoreCache.append(skipKey)
            writeIgnoreCache(ignoreCache)
            continue

        if resp == 'skipsimilar':
            skipSimilar.append(skipKey)
            continue

        if resp == 'edit':
            resp = getInput()

        resolutions[similarKey] = resp

        callback(resp, issue)

        count += 1

    return count
