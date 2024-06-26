import os
from Command.Command import Command
from Command.Issue import Issue
from Command.Option import Option
from Entry.Album import Album
from Entry.Artist import Artist
from utils.util import loopAlbums
from utils.constants import rootDir
from tidal import tidal

# TODO - don't detect on fuller dates
# TODO - skip/resolve per album


class YearIssue(Issue):
    artist: Artist
    album: Album
    folderYear: str

    def __init__(self, artist, album, folderYear, original, delta):
        super(YearIssue, self).__init__(artist=artist, album=album, original=original, delta=delta)
        self.folderYear = folderYear


class YearConflicts(Command):
    foundAlbums: list[str]
    allowEdit = True

    def findIssues(self):
        self.foundAlbums = []

        def cb(artist: Artist, album: Album) -> list[YearIssue]:
            found: list[YearIssue] = []

            # TODO - kinda janky; sometimes tags have full dates, we don't want to get rid of those
            # Need better logic here, probably in the Tags class
            folderYear = album.path.year[0:4]
            foundYearTag = None

            for track in album.tracks:
                yearTag = str(track.tags.year or '')[0:4]
                issue = YearIssue(
                        artist=artist,
                        album=album,
                        folderYear=folderYear,
                        original=str(foundYearTag),
                        delta=str(yearTag)
                )
                tagDiff = (yearTag and foundYearTag and foundYearTag != yearTag)
                folderDiff = yearTag != folderYear
                issueLogged = album.path.album in self.foundAlbums
                noYear = not yearTag and not folderYear and not foundYearTag

                if (tagDiff or folderDiff or noYear) and not issueLogged:
                    found.append(issue)
                    self.foundAlbums.append(album.path.album)
            return found

        return loopAlbums(rootDir, cb)

    def suggest(self, issue: YearIssue) -> list[Option]:
        suggestions: list[Option] = []

        if issue.folderYear:
            option = Option(key="NONE", display=issue.folderYear, value=issue.folderYear)
            suggestions.append(option)

        results = tidal.searchAlbum(issue.album.path.album, issue.album.path.albumArtist)
        for result in results:
            display = result.name  + " by " + result.artist.name + ": " + str(result.year)
            option = Option(key="NONE", display=display, value=result.year)
            suggestions.append(option)

        return suggestions

    def heuristic(self, options: list[Option]) -> Option:
        for option in options:
            if option.value.isdigit() and int(option.value) > 0:
                return option

        return options[0]

    def callback(self, good: str, issue: YearIssue) -> None:
        album = issue.album

        if not os.path.exists(album.path.realPath):
            return

        for track in album.tracks:
            yearTag = track.tags.year
            if yearTag != good:
                track.tags.setYear(good)

        if album.path.year != str(good):
            album.path.setYear(good)
