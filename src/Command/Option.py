from typing import Optional


class Option:
    key: Optional[str]
    value: str
    display: Optional[str]

    def __init__(self, key, value, display):
        self.key = key
        self.value = value
        self.display = display

    # TODO - this is just for backward compat
    def __getitem__(self, key: str):
        match key:
            case 'key':
                return self.key
            case 'value':
                return self.value
            case 'display':
                return self.display
        raise Exception("asdf")

    # TODO - this is just for backward compat
    def __setitem__(self, key: str, value):
        match key:
            case 'key':
                self.key = value
            case 'value':
                self.value = value
            case 'display':
                self.display = value
