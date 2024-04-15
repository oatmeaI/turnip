import unicodedata
import pathlib
from utils.path import rename, stripRootPath, unsanitize


class Path:
    realPath: str
    strippedPath: str
    pathObject: pathlib.Path
    parentPathParts: list[str]

    def __init__(self, fullPath: str):
        self.realPath = fullPath
        self.strippedPath = stripRootPath(fullPath)
        self.pathObject = pathlib.Path(self.strippedPath)
        self.parentPathParts = self.pathObject.as_posix().split('/')

    def normalizeString(self, string):
        return unicodedata.normalize('NFC', unsanitize(string))

    def move(self):
        newPath = self.buildPath()

        print(f"{stripRootPath(self.realPath)} -> {stripRootPath(newPath)}")

        rename(self.realPath, newPath)
        self.realPath = newPath

    def buildPath(self) -> str:
        raise Exception('Not implemented')
