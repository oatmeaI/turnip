from titlecase import titlecase
from internal_types import Issue, Option
from Command import TrackCommand
from Song import Song
from utils.tagging import getTitleTag
from utils.path import splitFileName
from tidal import tidal
import os
import unicodedata


def titleCallback(word, **kwargs):
    if word.lower() == 'in':
        return 'In'
    return None


class TitleTagFileConflicts(TrackCommand):
    cta = 'Conflict between track name and file name for: '
    allowEdit = True

    def detectIssue(self, artist, album, track):
        found: list[Issue] = []
        parts = splitFileName(track.path)
        if not parts:
            return found
        fileName = unicodedata.normalize('NFD', str(parts['title']))
        tagName = unicodedata.normalize('NFD', str(getTitleTag(track.path)))

        if fileName != tagName:
            found.append(
                {
                    'data': None,
                    'entry': track,
                    'original': tagName,
                    'delta': fileName,
                }
            )
        return found

    def check(self, issue: Issue) -> bool:
        return os.path.exists(issue['entry'])

    def skip(self, issue: Issue) -> str:
        track = Song(issue['entry'].path)
        return track.parts['album'] if track.parts else ''

    def suggest(self, issue: Issue) -> list[Option]:
        entry = issue['entry']
        split = splitFileName(entry.path)
        if not split:
            return []
        trackName = split['title'] if split['title'] else ''
        albumName = split['album'] if split['album'] else ''
        results = tidal.searchTrack(trackName, albumName, split['artist'])
        suggestions: list[Option] = []
        for result in results:
            suggestions.append(
                {
                    'key': 'NONE',
                    'display': result.name
                    + ' by '
                    + result.artist.name
                    + ' on '
                    + result.album.name,
                    'value': result.name,
                }
            )
        titleCasedOriginal = titlecase(
            issue['original'], callback=titleCallback
        )
        titleCasedDelta = titlecase(issue['delta'], callback=titleCallback)
        if titleCasedOriginal != issue['original']:
            suggestions.append(
                {
                    'key': 'NONE',
                    'display': titleCasedOriginal,
                    'value': titleCasedOriginal,
                }
            )
        if titleCasedDelta != issue['delta']:
            suggestions.append(
                {
                    'key': 'NONE',
                    'display': titleCasedDelta,
                    'value': titleCasedDelta,
                }
            )
        return suggestions

    def heuristic(self, options) -> Option:
        scores = []
        for option in options:
            score = 0
            value = option['value']
            if value is None or value == 'None':
                score -= 9999
            if titlecase(value, callback=titleCallback) == value:
                score += 5
            if value[:-1].isnumeric():
                score -= 2
            if '_' in value:
                score -= 1

            scores.append({'option': option, 'score': score})

        default = scores[0]
        for score in scores:
            if score['score'] > default['score']:
                default = score

        return default['option']

    def callback(self, good: str, issue: Issue) -> None:
        track = Song(issue['entry'].path)

        if not os.path.exists(issue['entry']):
            return

        track.setTitle(good)
