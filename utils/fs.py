import os
import shutil
from typing import Union


def loadFolders(path: str) -> list[os.DirEntry]:
    dir = list(os.scandir(path))
    folders = list(filter(lambda d: d.is_dir()
                   and not d.name.startswith("."), dir))
    return folders


def loadTracks(path: str) -> list[os.DirEntry]:
    dir = list(os.scandir(path))
    tracks = list(
        filter(
            lambda d: d.is_file()
            and (d.name.endswith("mp3") or d.name.endswith("flac")),
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


def moveDirFiles(fromDir: str, toDir: str) -> None:
    for fileName in filter(lambda d: not d.startswith("."), os.listdir(fromDir)):
        source = fromDir + "/" + fileName
        destination = toDir + "/" + fileName
        i = 1
        while os.path.exists(destination):
            if fileName.find(".") > 0:
                name = fileName[0: fileName.index(".")]
                extension = fileName[fileName.index("."):]
                destination = toDir + "/" + name + "_" + str(i) + extension
            else:
                destination = toDir + "/" + fileName + "_" + str(i)
            i += 1
        try:
            shutil.move(source, destination)
            print(source, " -> ", destination)
        except Exception as e:
            print("Couldn't move " + source + " to " + destination, e)


def rmDir(dir: os.DirEntry) -> None:
    try:
        print("Trashing " + dir.path)
        shutil.move(dir, os.path.expanduser("~/turnip_data/trash/" + dir.name))
    except Exception as e:
        print("Couldn't remove " + dir.name + ": ", e)


def rmFile(file: str) -> None:
    try:
        trashPath = os.path.expanduser("~/turnip/trash/")
        if not os.path.exists(trashPath):
            os.makedirs(trashPath, exist_ok=True)

        fileName = file[file.rindex("/") + 1:]
        print("Trashing " + fileName)
        shutil.move(file, trashPath + fileName)
    except Exception as e:
        print("Couldn't remove " + file + ": ", e)
