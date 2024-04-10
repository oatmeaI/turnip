from utils.util import newFix, loopTracks
from utils.path import stripRootPath
from utils.userio import promptHeader, formatCommandName
from utils.constants import rootDir
from internal_types import Issue


class Command:
    cta = ''
    allowEdit = False
    skipIssueValues = False
    suggestionLimit = 3
    # TODO add hint for what "similar" means

    def similar(self, issue: Issue) -> str:
        return (issue['original'] or '') + '>' + (issue['delta'] or '')

    def skip(self, issue: Issue) -> str:
        return (issue['original'] or '') + '>' + (issue['delta'] or '')

    def findIssues(self):
        return []

    def callback(self, good, issue):
        return None

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
        return f"{promptHeader(self.__class__.__name__, index, count)}\n{self.cta} {stripRootPath(issue['entry'].path.realPath)}"

    def process(self) -> int:
        print('\n' + formatCommandName(self.__class__.__name__))
        issues = self.findIssues()

        return newFix(
            issues=issues,
            prompt=self.prompt,
            callback=self.callback,
            heuristic=self.heuristic,
            suggest=self.suggest,
            check=self.check,
            allowEdit=self.allowEdit,
            skipIssueValues=self.skipIssueValues,
            suggestionLimit=self.suggestionLimit,
            similar=self.similar,
            auto=self.auto,
            optionString=self.optionString,
            skip=self.skip,
        )


class TrackCommand(Command):
    def detectIssue(self, artist, album, track):
        return []

    def findIssues(self):
        return loopTracks(rootDir, self.detectIssue)
