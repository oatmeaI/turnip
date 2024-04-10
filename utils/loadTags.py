
import pathlib
from utils.FLACTags import FLACTags
from utils.MP3Tags import MP3Tags
from utils.MP4Tags import MP4Tags
from utils.Tags import BaseTags


def loadTags(path: str) -> BaseTags:
    extension = pathlib.Path(path).suffix
    match extension:
        case '.mp3':
            return MP3Tags(path)
        case '.m4a':
            return MP4Tags(path)
        case '.flac':
            return FLACTags(path)
        case _:
            raise Exception('Not recognized')
