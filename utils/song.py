import os


def setTitle(track: os.DirEntry, title: str):
    # - set tag
    # - escape title
    # - set filename, preserving track number, etc (do this in a separate module)


def setTrackNumber(track: os.DirEntry, number: int):
    # - set tag (I think tagging module takes care of transforms)
    # - pad number
    # - set number in filename, preserving everything else
