import os
from typing import Any
from Command.Command import Command
from Command.Issue import Issue
from utils.constants import rootDir
from utils.util import compareDupes, loopTracks, findBad
from utils.path import splitFileName, stripRootPath
from utils.fs import rmFile


class TrackDuplicates(Command):
    cta = 'Possible duplicate tracks found. Select which to keep:'

    def findIssues(self) -> list[Issue]:
        keys: list[Any] = []
        currentArtist = ''

        def cb(artist, album, track) -> list[Issue]:
            nonlocal keys
            nonlocal currentArtist
            if currentArtist != artist:
                keys = []
                currentArtist = artist

            return compareDupes(track, keys, track.name)

        return loopTracks(rootDir, cb)

    def getFileSize(self, path):
        try:
            return round(os.path.getsize(path) / 1000000, 2)
        except Exception:
            return 0

    def heuristic(self, options):
        largest = 0
        default = None
        for option in options:
            if not option['value'].startswith(rootDir):
                continue
            size = self.getFileSize(option['value'])
            if size > largest:
                largest = size
                default = option
        return default

    def optionString(self, optionValue):
        fileSize = self.getFileSize(optionValue)
        return stripRootPath(optionValue) + ' (' + str(fileSize) + 'mb)'

    def similar(self, issue: Issue) -> str:
        # TODO - this doesn't work, so breaking it
        return False
        originalParts = splitFileName(issue['original'] or '')
        deltaParts = splitFileName(issue['delta'] or '')

        if not originalParts or not deltaParts:
            return issue['original'] or ''

        originalAlbum = originalParts['album']
        deltaAlbum = deltaParts['album']
        return f'{originalAlbum} > {deltaAlbum}'

    def callback(self, good: str, issue: Issue) -> None:
        bad = findBad(issue, good)
        if not bad or not os.path.exists(good) or not os.path.exists(bad):
            return
        rmFile(bad)
