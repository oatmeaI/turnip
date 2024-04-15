import os


def rip(url: str) -> None:
    os.system("rip url " + url + " --ignore-db")
