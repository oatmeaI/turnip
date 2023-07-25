from utils.constants import rootDir
from utils.util import compareDupes, loopArtists, newFix, findBad
from utils.userio import promptHeader, formatCommandName
from internal_types import Issue, Key
from utils.fs import moveDirFiles


class Command:
    cta = ""
    allowEdit = False
    skipIssueValues = False
    suggestionLimit = 3

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

    def prompt(self, issue: Issue, index: int, count: int):
        return f"{promptHeader(self.__class__.__name__, index, count)}\n{self.cta}"

    def process(self) -> int:
        print("\n" + formatCommandName(self.__class__.__name__))
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
        )


class ArtistDuplicates(Command):
    cta = "Possible artist duplicates found. Select which to keep:"

    def findIssues(self) -> list[Issue]:
        keys: list[Key] = []

        def cb(artist):
            return compareDupes(artist, keys, artist.name)

        return loopArtists(rootDir, cb)

    def callback(self, good: str, issue: Issue) -> None:
        bad = findBad(issue, good)
        if bad and good:
            moveDirFiles(bad, good)


# def findArtistDupes(rootDir: str) -> list[Issue]:
#     keys: list[Key] = []
#
#     def cb(artist):
#         return compareDupes(artist, keys, artist.name)
#
#     return loopArtists(rootDir, cb)


# def process(rootDir: str) -> int:
# print(formatCommandName(__file__))
# artistDupes = findArtistDupes(rootDir)

# def callback(good: str, issue: Issue) -> None:
#     bad = findBad(issue, good)
#     if bad and good:
#         moveDirFiles(bad, good)

# def prompt(issue: Issue, index: int, count: int):
#     return (
#         promptHeader(__file__, index, count)
#         + "\n"
#         + "Possible artist duplicates found. Select which to keep:"
#     )
#
# return newFix(issues=artistDupes, callback=callback, prompt=prompt)
