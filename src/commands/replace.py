from typing_extensions import TypedDict
from typing import Optional, Pattern, Union, Callable, Dict
from Command.Command import TrackCommand
from Command.Issue import TrackIssue
from Command.Option import Option
from Entry.Album import Album
from Entry.Artist import Artist
from Entry.Track import Track
from utils.tagging import (
    getTitleTag,
    getArtistTag,
    getAlbumArtistTag,
    getAlbumTag
)
import os
import re


class Replacement():
    find: str
    replace: str
    search: Union[str, list[str]]
    auto: bool
    foundTag: str

    def __init__(self, find, replace, search, auto):
        self.find = find
        self.replace = replace
        self.search = search
        self.auto = auto

    def isFound(self, track: Track) -> Optional[list[str]]:
        # TODO - I only use 'all', but should support others lol
        # TODO this feels dumb
        # TODO this seems like a bad return format
        if self.find in track.artist:
            return ['artist', track.artist]
        if self.find in track.album:
            return ['album', track.album]
        if self.find in track.albumArtist:
            return ['albumArtist', track.albumArtist]
        if self.find in track.title:
            return ['title', track.title]

        return None

    def doReplace(self, value: str) -> str:
        return value.replace(self.find, self.replace)


class RegexReplacement(Replacement):
    findPattern: Pattern

    def __init__(self, find, replace, search, auto):
        super(RegexReplacement, self).__init__(find, replace, search, auto)
        self.findPattern = re.compile(find)

    def isFound(self, track: Track) -> Optional[list[str]]:
        if re.search(self.findPattern, track.artist):
            return ['artist', track.artist]
        if re.search(self.findPattern, track.album):
            return ['album', track.album]
        if re.search(self.findPattern, track.albumArtist):
            return ['albumArtist', track.albumArtist]
        if re.search(self.findPattern, track.title):
            return ['title', track.title]

        return None

    def doReplace(self, value: str) -> str:
        return re.sub(self.findPattern, self.replace, value)


replacements: list[Replacement] = [
    Replacement(
        find='remix',
        replace='Remix',
        search='all',
        auto=False,
    ),
    Replacement(
        find=' (Album Version) [Album Version]/Album Version',
        replace='',
        search='all',
        auto=True,
    ),
    Replacement(
        find=r'( [\(\[]Album Version[\)\]])',
        replace='',
        search='all',
        auto=True,
    ),
    Replacement(
        find='’',
        replace="'",
        search='all',
        auto=True,
    ),
    Replacement(
        find='“',
        replace='"',
        search='all',
        auto=True,
    ),
    Replacement(
        find='”',
        replace='"',
        search='all',
        auto=True,
    ),
    Replacement(
        find=' [Song   Album Version]/Song   Album Version',
        replace='',
        search='all',
        auto=True,
    ),
    Replacement(
        find='/Album Version',
        replace='',
        search='all',
        auto=True,
    ),
    Replacement(
        find=' (Explicit)',
        replace='',
        search='all',
        auto=True,
    ),
    Replacement(
        find=' [Explicit]',
        replace='',
        search='all',
        auto=True,
    ),
    RegexReplacement(
        find=r'( \([^\)]*[Rr]emaster[^\)]*\))',
        replace='',
        search='all',
        auto=False,
    ),
    RegexReplacement(
        find=r'(.*) - (.* [rR]emix)',
        replace=r'\1 (\2)',
        search='all',
        auto=False,
    ),
    RegexReplacement(
        find=r'(.*) \[(.*[rR]emix)\]',
        replace=r'\1 (\2)',
        search='all',
        auto=False,
    ),
    RegexReplacement(
        find=r' (\(.*\) )?\[(.*)\][/_].*',
        replace=[r' (\2)', ''],
        search='all',
        auto=False,
    ),
]


class Replace(TrackCommand):
    cta = 'Replace found'
    allowEdit = True

    def detectIssue(self, artist: Artist, album: Album, track: Track) -> list[TrackIssue]:
        foundIssues = []

        for replacement in replacements:
            found = replacement.isFound(track)
            if not found:
                continue

            # TODO bad names
            [tagName, tagValue] = found

            replaced = replacement.doReplace(tagValue)

            issue = TrackIssue(
                    artist=artist,
                    album=album,
                    track=track,
                    delta=replaced,
                    original=tagValue,
                    data=tagName
                    )

            foundIssues.append(issue)
        return foundIssues

    # def suggest(self, issue):
    #     key = (
    #         issue['entry'].path
    #         + issue['original']
    #         + issue['delta']
    #         + issue['data']
    #     )
    #     if key in self.suggestions:
    #         suggest = self.suggestions[key]
    #         return [{'key': suggest, 'value': suggest}]
    #     return []

    def heuristic(self, options: list[Option]):
        return options[1]

    def callback(self, good: str, issue: TrackIssue) -> None:
        track = issue.track
        tag = issue.data

        match tag:
            case 'artist':
                track.setArtist(good)
            case 'album':
                track.setAlbum(good)
            case 'albumArtist':
                track.setAlbumArtist(good)
            case 'title':
                track.setTitle(good)
