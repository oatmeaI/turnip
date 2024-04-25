from Command.Command import Command
from Command.Issue import ArtistIssue, Issue
from Entry.Artist import Artist
from utils.compare import compare
from utils.constants import rootDir
from utils.util import loopArtists, findBad
from utils.fs import moveDirFiles


class ArtistDuplicates(Command):
    cta = "Possible artist duplicates found. Select which to keep:"
    seen: list[Artist]

    def findIssues(self) -> list[ArtistIssue]:
        self.seen = []

        def cb(artist: Artist) -> list[Issue]:
            found: list[Issue] = []

            for otherArtist in self.seen:
                if compare(artist.path.albumArtist, otherArtist.path.albumArtist):
                    found.append(ArtistIssue(
                        artist=artist,
                        original=otherArtist.path.realPath,
                        delta=artist.path.realPath
                        ))
            self.seen.append(artist)
            return found

        return loopArtists(rootDir, cb)

    def callback(self, good: str, issue: Issue) -> None:
        bad = findBad(issue, good)
        if bad and good:
            moveDirFiles(bad, good)
