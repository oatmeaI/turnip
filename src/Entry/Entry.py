from Path.Path import Path
from Path.AlbumPath import AlbumPath
from Path.ArtistPath import ArtistPath
from Path.TrackPath import TrackPath
from utils.path import stripRootPath


def load(fullPath):
    strippedPath = stripRootPath(fullPath)
    parentPathParts = strippedPath.split('/')
    pathType = len(parentPathParts)
    match pathType:
        case 1:
            return ArtistPath(fullPath)
        case 2:
            return AlbumPath(fullPath)
        case 3:
            return TrackPath(fullPath)
    raise Exception('Invalid path')


class Entry:
    path: Path
    _forceCache: bool

    def __init__(self, path: str, forceCache=False) -> None:
        self.path = load(path)
        self._forceCache = forceCache

    def printPropUpdate(self, prop: str, newValue: str):
        print(f"{stripRootPath(self.path.realPath)} | {prop} -> {newValue}")
