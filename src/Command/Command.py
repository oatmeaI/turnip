import copy
import os
import pickle
from typing import Any, Dict
from Command.Issue import Issue
from Command.Option import Option
from utils.path import stripRootPath
from utils.util import getInput, loopTracks
from utils.userio import chooseFromList, confirm, green, promptHeader, formatCommandName, red
from utils.constants import rootDir


class Command:
    title = ''
    cta = ''
    allowEdit = False
    skipIssueValues = False
    suggestionLimit = 6
    _ignoreCache: list[str] = []
    _skipSimilar: list[str] = []
    _skipArtists: list[str] = []
    _skipAlbums: list[str] = []
    _resolutions: Dict[Any, Any] = {}
    _shouldUseSimilar: list[Any] = []
    # TODO add hint for what "similar" means

    def __init__(self):
        if not os.path.exists('ignoreCache.pickle'):
            self._ignoreCache = []
        else:
            with open('ignoreCache.pickle', 'rb') as f:
                self._ignoreCache = pickle.load(f)

    def findIssues(self):
        return []

    def callback(self, good, issue):
        raise Exception('not implemented')

    def heuristic(self, options):
        return options[0]

    def suggest(self, issue):
        return []

    def check(self, issue):
        return True

    def auto(self, issue):
        return False

    def optionString(self, optionValue: str) -> str:
        return stripRootPath(optionValue)

    def prompt(self, issue: Issue, index: int, count: int):
        header = promptHeader(self.__class__.__name__, index, count)
        path = stripRootPath(issue.entry.path.realPath)
        return f"{header}\n{self.cta} {path}"

    def shouldProcess(self, issue: Issue) -> bool:
        if issue.key in self._ignoreCache:
            return False

        # TODO - different key for similar, probably
        if issue.key in self._skipSimilar:
            return False

        if issue.key in self._ignoreCache:
            return False

        if issue.album and issue.album.path.album in self._skipAlbums:
            return False

        if issue.artist and issue.artist.path.albumArtist in self._skipArtists:
            return False

        return True

    def buildOptions(self, issue: Issue) -> list[Option]:
        options: list[Option] = []

        if issue.original and not self.skipIssueValues:
            options.append(Option(
                key='1',
                value=issue.original,
                display=red(self.optionString(issue.original))
            ))

        if issue.delta and not self.skipIssueValues:
            options.append(Option(
                key=str(len(options) + 1),
                value=issue.delta,
                display=green(self.optionString(issue.delta)),
            ))

        suggestions = self.suggest(issue)

        i = len(options) + 1
        end = min(len(suggestions), self.suggestionLimit)

        for suggestion in suggestions[0:end]:
            suggestion.key = str(i)
            options.append(suggestion)
            i += 1

        options.append(Option(key='s', value='skip', display='skip'))
        options.append(Option(key='L', value='skipArtist', display='skip this artist'))
        options.append(Option(key='J', value='skipAlbum', display='skip this album'))
        options.append(Option(key='K', value='skipsimilar', display='skip all similar'))
        options.append(Option(key='S', value='skip all', display='skip all'))
        options.append(Option(key='I', value='ignoresimilar', display='ignore all similar'))
        options.append(Option(key='i', value='ignore', display='ignore'))

        default = self.heuristic(options)

        if self.allowEdit:
            options.append(Option(key='e', value='edit', display='edit'))

        if default:
            options.append(Option(key='', value=default['value'], display=default.display))

        return options

    def _writeIgnoreCache(self):
        with open('ignoreCache.pickle', 'wb') as f:
            pickle.dump(self._ignoreCache, f, protocol=pickle.HIGHEST_PROTOCOL)

    def handleSimilar(self, issue: Issue):
        if issue.key in self._resolutions:
            if issue.key in self._shouldUseSimilar:
                self.callback(self._resolutions[issue.key], issue)
                return True
            print(
                'Similar resolution recorded for '
                + red(issue.original or '')
                + ': '
                + green(self._resolutions[issue.key])
            )
            useSimilar = confirm('Would you like to use this?', default=True)
            if useSimilar:
                alwaysUseSimilar = confirm("Would you like to use this for all similar issues?", default=True)
                if alwaysUseSimilar:
                    self._shouldUseSimilar.append(issue.key)
                self.callback(self._resolutions[issue.key], issue)
                return True

    # TODO split up more
    def process(self) -> int:
        print('\n' + formatCommandName(self.__class__.__name__))

        print(self.title)
        issues = self.findIssues()
        filteredIssues = list(filter(self.shouldProcess, issues))

        i = 0
        count = 0
        for issue in filteredIssues:
            i += 1
            if issue.key in self._ignoreCache:
                print("Ignoring...")
                continue

            if not self.check(issue):
                print("Skipping because check failed...", issue.entry.path.realPath)
                continue

            if not self.shouldProcess(issue):
                print("Skipping" + issue.entry.path.realPath)
                continue

            print(self.prompt(issue, i, len(filteredIssues)))

            options = self.buildOptions(issue)
            # skip items with no suggestions except to skip
            if len(options) < 9:
                print("Skipping because no options")
                continue

            print('')  # New line

            autoResolve = self.auto(issue)
            defaultOption = self.heuristic(options) # TODO - I feel like this happens twice
            if autoResolve and defaultOption:
                print('Auto...')
                resp = defaultOption.value
                self.callback(resp, issue)
                count += 1
                continue

            handled = self.handleSimilar(issue)
            if handled:
                print('Skipping...')
                continue

            resp = chooseFromList(options)

            if resp == 'skip all':
                break

            if resp == 'skip':
                continue

            if resp == 'ignore':
                self._ignoreCache.append(issue.key)
                self._writeIgnoreCache()
                continue

            if resp == 'ignoresimilar':
                self._ignoreCache.append(issue.key)
                self._writeIgnoreCache()
                continue

            if resp == 'skipsimilar':
                self._skipSimilar.append(issue.key)
                continue

            if resp == 'skipAlbum':
                self._skipAlbums.append(issue.album.path.album)
                continue

            if resp == 'skipArtist':
                print('here')
                self._skipArtists.append(issue.artist.path.albumArtist)
                print(self._skipArtists)
                continue

            if resp == 'edit':
                resp = getInput()

            self._resolutions[issue.key] = resp

            self.callback(resp, issue)

            count += 1

        return count


class TrackCommand(Command):
    def detectIssue(self, artist, album, track):
        return []

    def findIssues(self):
        return loopTracks(rootDir, self.detectIssue)
