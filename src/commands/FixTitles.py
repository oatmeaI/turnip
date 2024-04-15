from titlecase import titlecase
from Command.Command import TrackCommand
from Command.Issue import Issue
from Command.Option import Option
from Entry.Album import Album
from Entry.Artist import Artist
from Entry.Track import Track
from tidal import tidal


def titleCallback(word, **kwargs):
    if word.lower() == 'in':
        return 'In'
    return None


class TitleIssue(Issue):
    track: Track
    pass


class FixTitles(TrackCommand):
    cta = 'Conflict between track name and file name for: '
    allowEdit = True

    def detectIssue(self, artist: Artist, album: Album, track: Track) -> list[TitleIssue]:
        found: list[TitleIssue] = []

        if track.path.title != track.tags.title:
            issue = TitleIssue(
                    artist=artist,
                    album=album,
                    original=track.tags.title,
                    delta=track.path.title,
                    track=track
                    )
            found.append(issue)
        return found

    def suggest(self, issue: TitleIssue) -> list[Option]:
        track = issue.track
        results = tidal.searchTrack(track.title, track.album, track.albumArtist)
        suggestions: list[Option] = []
        for result in results:
            option = Option(
                    key="NONE",
                    display=result.name + ' by ' + result.artist.name + ' on ' + result.album.name,
                    value=result.name
                    )
            suggestions.append(option)

        titleCasedOriginal = titlecase(
            issue.original, callback=titleCallback
        )
        titleCasedDelta = titlecase(issue.delta, callback=titleCallback)
        if titleCasedOriginal != issue.original:
            suggestions.append(Option(
                    key='NONE',
                    display=titleCasedOriginal,
                    value=titleCasedOriginal,
                )
            )
        if titleCasedDelta != issue.delta:
            suggestions.append(Option(
                    key='NONE',
                    display=titleCasedDelta,
                    value=titleCasedDelta,
                )
            )
        return suggestions

    def heuristic(self, options: list[Option]) -> Option:
        scores = []
        for option in options:
            score = 0
            value = option.value
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

    def callback(self, good: str, issue: TitleIssue) -> None:
        track = issue.track
        track.setTitle(good)
