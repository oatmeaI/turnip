from utils.path import splitFileName, buildFileName, rename
from utils.path import stripRootPath


class Entry:
    # TODO - not really a "side" effect, more like the main event. gotta be a better way to structure this
    propUpdateSideEffects = {}

    def __init__(self, path: str) -> None:
        self.path = path
        self.parts = splitFileName(path)

    def printPropUpdate(self, prop: str, newValue: str):
        print(f"{stripRootPath(self.path)} | {prop} -> {newValue}")

    def updateProp(self, propName: str, value: str) -> None:
        # TODO - don't print if no changes are made (side effects make this complicated)
        self.printPropUpdate(propName, value)

        sideEffect = self.propUpdateSideEffects[propName]
        sideEffect(self.path, value)

        self.parts[propName] = value

        self.updatePath()

    def updatePath(self) -> None:
        newPath = buildFileName(self.parts)

        if newPath == self.path:
            return

        print(f"{stripRootPath(self.path)} -> {newPath}")

        rename(self.path, newPath)
        self.path = newPath
