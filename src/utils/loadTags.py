
import pathlib
from utils.FLACTags import FLACTags
from utils.MP3Tags import MP3Tags
from utils.MP4Tags import MP4Tags
from utils.Tags import BaseTags


def loadTags(path: str, forceCache=False) -> BaseTags:
    extension = pathlib.Path(path).suffix
    match extension:
        case '.mp3':
            return MP3Tags(path, forceCache)
        case '.m4a':
            return MP4Tags(path, forceCache)
        case '.flac':
            return FLACTags(path, forceCache)
        case _:
            raise Exception('Not recognized')
