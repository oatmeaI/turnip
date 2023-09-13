from typing_extensions import TypedDict
from typing import Optional
import os

Issue = TypedDict(
    'Issue',
    {
        'entry': os.DirEntry,
        'original': Optional[str],
        'delta': Optional[str],
        'data': Optional[str],
    },
)

Option = TypedDict(
    'Option', {'key': str, 'value': str, 'display': Optional[str]}
)

Ignore = TypedDict('Ignore', {})

TrackNameParts = TypedDict(
    'TrackNameParts',
    {
        'title': str,
        'number': Optional[str],
        'disc': Optional[str],
        'extension': str,
        'artist': str,
        'album': str,
        'year': str,
    },
)

Key = TypedDict('Key', {'dir': os.DirEntry, 'key': str})
