import os
import re
import shutil
from utils.constants import rootDir


def loadFolders(path: str) -> list[os.DirEntry]:
    dir = list(os.scandir(path))
    folders = list(
        filter(lambda d: d.is_dir() and not d.name.startswith('.'), dir)
    )
    return folders


def loadTracks(path: str) -> list[os.DirEntry]:
    dir = list(os.scandir(path))
    tracks = list(
        filter(
            lambda d: d.is_file()
            and (d.name.endswith('mp3') or d.name.endswith('flac') or d.name.endswith('m4a')),
            dir,
        )
    )
    return tracks


def ensureDirExists(path: str) -> None:
    if not os.path.exists(path):
        os.mkdir(path)


def moveFileWithFallback(fromDir: str, toDir: str) -> None:
    # TODO - make this do what moveDirFiles is doing in the loop below, and then use this there
    return


# TODO - this is duplicated because of a circular import; need to clean all these up
def stripRootPath(string: str):
    stripped = re.sub(rootDir, '', string)
    return stripped[1:] if stripped.startswith('/') else stripped


def moveDirFiles(fromDir: str, toDir: str) -> None:
    # TODO - is there a way to do this with less boilerplate?
    table = Columns()
    rows = list(filter(lambda d: not d.startswith('.'), os.listdir(fromDir)))

    def columnA(row):
        return stripRootPath(fromDir + '/' + row)

    def columnB(row):
        return stripRootPath(toDir + '/' + row)

    table.setup(rows, columnA, columnB)

    for fileName in rows:
        source = fromDir + '/' + fileName
        destination = toDir + '/' + fileName
        i = 1
        while os.path.exists(destination):
            if fileName.find('.') > 0:
                name = fileName[0 : fileName.index('.')]
                extension = fileName[fileName.index('.') :]
                destination = toDir + '/' + name + '_' + str(i) + extension
            else:
                destination = toDir + '/' + fileName + '_' + str(i)
            i += 1
        try:
            shutil.move(source, destination)
            table.printRow(fileName)
        except Exception as e:
            print("Couldn't move " + source + ' to ' + destination, e)


# TODO - do we ever need more than two columns?
# TODO - move to io
class Columns:
    def setup(self, rows, columnA, columnB):
        longest = 0
        for row in rows:
            columnALength = len(columnA(row))
            columnBLength = len(columnB(row))
            totalLength = columnBLength + columnALength

            if totalLength > longest:
                longest = totalLength

        if longest % 2 > 0:
            longest += 1

        self.longest = longest
        self.columnA = columnA
        self.columnB = columnB

    def printRow(self, row):
        columnA = self.columnA(row)
        columnB = self.columnB(row)

        diff = self.longest - len(columnA + columnB)

        spacer = ''.join([' ' for x in range(int(diff / 2))])
        output = ''.join([columnA, spacer, '  ->  ', columnB])

        print(output)


def rmDir(dir: os.DirEntry) -> None:
    try:
        destination = os.path.expanduser('~/turnip_data/trash/' + dir.name)
        while os.path.exists(destination):
            destination = destination + '1'
        shutil.move(dir, destination)
    except Exception as e:
        print("Couldn't remove " + dir.name + ': ', e)


def rmFile(file: str) -> None:
    try:
        trashPath = os.path.expanduser('~/turnip_data/trash/')
        if not os.path.exists(trashPath):
            os.makedirs(trashPath, exist_ok=True)

        fileName = file[file.rindex('/') + 1 :]
        print('Trashing ' + fileName)
        shutil.move(file, trashPath + fileName)
    except Exception as e:
        print("Couldn't remove " + file + ': ', e)
