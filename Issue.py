from typing import Any, Optional
from Entry import Entry


class Issue:
    data: Optional[Any]
    entry: Entry
    original: str
    delta: str

    def __init__(self, entry, original, delta, data):
        self.data = data
        self.entry = entry
        self.original = original
        self.delta = delta

    @property
    def key(self):
        return str(self.data) + self.entry.path.realPath + self.original + self.delta


    def __eq__(self, other):
        try:
            return self.key == other.key
        except AttributeError:
            return False

    # TODO - this is just for backward compat
    def __getitem__(self, key: str):
        match key:
            case 'data':
                return self.data
            case 'entry':
                return self.entry
            case 'original':
                return self.original
            case 'delta':
                return self.delta

    # TODO - this is just for backward compat
    def __setitem__(self, key: str, value):
        match key:
            case 'data':
                self.data = value
            case 'entry':
                self.entry = value
            case 'original':
                self.original = value
            case 'delta':
                self.delta = value
