from typing_extensions import TypedDict
from typing import Union, Callable, Dict
from Command import TrackCommand
from utils.tagging import (
    getTitleTag,
    getArtistTag,
    getAlbumArtistTag,
)
import os
from Song import Song
from utils.util import newFix, loopTracks
from internal_types import Issue, Option
from utils.constants import rootDir
from utils.path import stripRootPath
from utils.userio import promptHeader, bold, red, green, yellow


Replacement = TypedDict(
    'Replacement',
    {
        'find': str,
        'replace': str,
        'search': Union[str, list[str]],
        'auto': bool,
    },
)

replacements: list[Replacement] = [
    {'find': 'remix', 'replace': 'Remix', 'search': 'all', 'auto': False},
    {
        'find': ' (Album Version) [Album Version]/Album Version',
        'replace': '',
        'search': 'all',
        'auto': True,
    },
    {'find': ' (Album Version)', 'replace': "", 'search': 'all', 'auto': True},
    {'find': '’', 'replace': "'", 'search': 'all', 'auto': True},
    {
        'find': '“',
        'replace': '"',
        'search': 'all',
        'auto': True,
    },
    {'find': '”', 'replace': '"', 'search': 'all', 'auto': True},
]

TagFunc = TypedDict(
    'TagFunc',
    {
        'get': Callable[[str], str | None],
        'set': Callable[[os.DirEntry, str], None],
    },
)

tagFuncs: Dict[str, TagFunc] = {
    'title': {
        'get': getTitleTag,
        'set': lambda t, newTitle: t.setTitle(newTitle),
    },
    'artist': {
        'get': getArtistTag,
        'set': lambda t, newArtist: t.setArtist(newArtist),
    },
    'albumArtist': {
        'get': getAlbumArtistTag,
        'set': lambda t, newArtist: t.setAlbumArtist(newArtist),
    },
}


class Replace(TrackCommand):
    cta = 'Replace found'
    allowEdit = True

    def detectIssue(self, artist, album, track) -> list[Issue]:
        found: list[Issue] = []

        for replacement in replacements:
            searches = (
                tagFuncs.keys()
                if replacement['search'] == 'all'
                else replacement['search']
            )

            tags = []
            for search in searches:
                tags.append(
                    {
                        'tag': search,
                        'value': tagFuncs[search]['get'](track.path),
                    }
                )

            for tag in tags:
                if tag['value'] and replacement['find'] in tag['value']:
                    replaced = tag['value'].replace(
                        replacement['find'], replacement['replace']
                    )
                    issue: Issue = {
                        'entry': track,
                        'delta': replaced,
                        'original': tag['value'],
                        'data': tag['tag'],
                    }
                    if 'auto' not in replacement or not replacement['auto']:
                        issue['original'] = tag['value']
                    found.append(issue)
        return found

    def heuristic(self, options: list[Option]) -> Option:
        return options[1]

    def callback(self, good: str, issue: Issue) -> None:
        track = issue['entry']
        if not os.path.exists(track):
            return
        tag = issue['data']
        if not tag:
            return
        print('Updating ' + track.path + ' - setting ' + tag + ' to ' + good)
        song = Song(track.path)
        tagFuncs[tag]['set'](song, good)


def findReplacements(rootDir: str) -> list[Issue]:
    def cb(
        artist: os.DirEntry, album: os.DirEntry, track: os.DirEntry
    ) -> list[Issue]:
        found: list[Issue] = []

        for replacement in replacements:
            searches = (
                tagFuncs.keys()
                if replacement['search'] == 'all'
                else replacement['search']
            )

            tags = []
            for search in searches:
                tags.append(
                    {
                        'tag': search,
                        'value': tagFuncs[search]['get'](track.path),
                    }
                )

            for tag in tags:
                if tag['value'] and replacement['find'] in tag['value']:
                    replaced = tag['value'].replace(
                        replacement['find'], replacement['replace']
                    )
                    issue: Issue = {
                        'entry': track,
                        'delta': replaced,
                        'original': tag['value'],
                        'data': tag['tag'],
                    }
                    if 'auto' not in replacement or not replacement['auto']:
                        issue['original'] = tag['value']
                    found.append(issue)
        return found

    return loopTracks(rootDir, cb)


def process() -> int:
    issues = findReplacements(rootDir)

    def prompt(issue: Issue, index: int, count: int) -> str:
        return (
            promptHeader('replace', index, count)
            + '\n'
            + 'Replacement found at '
            + bold(stripRootPath(issue['entry'].path))
            + '\n'
            + 'Replace '
            + red(issue['original'] or '')
            + ' with '
            + green(issue['delta'] or '')
            + ' in '
            + yellow((issue['data'] or ''))
            + '?'
        )

    # print some info about what's current and what's new so I can know if I should skip or apply
    def cb(good: str, issue: Issue) -> None:
        track = issue['entry']
        if not os.path.exists(track):
            return
        tag = issue['data']
        if not tag:
            return
        print('Updating ' + track.path + ' - setting ' + tag + ' to ' + good)
        song = Song(track.path)
        tagFuncs[tag]['set'](song, good)

    def heuristic(options: list[Option]) -> Option:
        return options[1]

    return newFix(
        issues=issues,
        prompt=prompt,
        callback=cb,
        allowEdit=True,
        heuristic=heuristic,
    )
