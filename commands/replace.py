from typing_extensions import TypedDict
from typing import Union, Callable, Dict
from Command import TrackCommand
from utils.tagging import (
    getTitleTag,
    getArtistTag,
    getAlbumArtistTag,
)
import os
import re
from Song import Song
from internal_types import Issue, Option


Replacement = TypedDict(
    'Replacement',
    {
        'find': str,
        'replace': str,
        'search': Union[str, list[str]],
        'auto': bool,
        'regex': bool,
    },
)

replacements: list[Replacement] = [
    {
        'find': 'remix',
        'replace': 'Remix',
        'search': 'all',
        'auto': False,
        'regex': False,
    },
    {
        'find': ' (Album Version) [Album Version]/Album Version',
        'replace': '',
        'search': 'all',
        'auto': True,
        'regex': False,
    },
    {
        'find': r'( [\(\[]Album Version[\)\]])',
        'replace': '',
        'search': 'all',
        'auto': True,
        'regex': True,
    },
    {
        'find': '’',
        'replace': "'",
        'search': 'all',
        'auto': True,
        'regex': False,
    },
    {
        'find': '“',
        'replace': '"',
        'search': 'all',
        'auto': True,
        'regex': False,
    },
    {
        'find': '”',
        'replace': '"',
        'search': 'all',
        'auto': True,
        'regex': False,
    },
    {
        'find': ' [Song   Album Version]/Song   Album Version',
        'replace': '',
        'search': 'all',
        'auto': True,
        'regex': False,
    },
    {
        'find': '/Album Version',
        'replace': '',
        'search': 'all',
        'auto': True,
        'regex': False,
    },
    {
        'find': ' (Explicit)',
        'replace': '',
        'search': 'all',
        'auto': True,
        'regex': False,
    },
    {
        'find': r'( \(.* [Rr]emaster .*\))',
        'replace': '',
        'search': 'all',
        'auto': False,
        'regex': True,
    },
]

TagFunc = TypedDict(
    'TagFunc',
    {
        'get': Callable[[str], str | None],
        'set': Callable[[Song, str], None],
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
                if not tag['value']:
                    continue

                find = (
                    replacement['find']
                    if not replacement['regex']
                    else re.compile(replacement['find'])
                )
                matched = (
                    replacement['find'] in tag['value']
                    if not replacement['regex']
                    else find.search(tag['value'])
                )

                if tag['value'] and matched:
                    replaced = (
                        tag['value'].replace(find, replacement['replace'])
                        if not replacement['regex']
                        else find.sub(replacement['replace'], tag['value'])
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
