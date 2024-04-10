from TrackNameParts import TrackNameParts
from utils.path import stripRootPath


class Entry:
    path: TrackNameParts

    def __init__(self, path: str) -> None:
        self.path = TrackNameParts(path)

    def printPropUpdate(self, prop: str, newValue: str):
        print(f"{stripRootPath(self.path.realPath)} | {prop} -> {newValue}")
