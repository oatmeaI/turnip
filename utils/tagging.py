import mutagen
import pickle
import os
from typing import Optional
from typing_extensions import TypedDict


def readTagCache():
    if not os.path.exists('tagCache.pickle'):
        return {}
    with open('tagCache.pickle', 'rb') as f:
        return pickle.load(f)
    # file = open("./tagCache.json", "r")
    # cache = json.load(file)
    # file.close()
    # return cache


tagCache = readTagCache()


def writeTagCache():
    with open('tagCache.pickle', 'wb') as f:
        pickle.dump(tagCache, f, protocol=pickle.HIGHEST_PROTOCOL)


# file = open("./tagCache.json", "w")
# json.dump(tagCache, file)
# file.close()


tagNames = {
    'trackNumber': 'trackNumber',
    'trackCount': 'trackCount',
    'albumArtist': 'albumArtist',
    'album': 'album',
    'year': 'year',
    'title': 'title',
    'artist': 'artist',
}

tagNameMap = {}
tagNameMap[tagNames['trackNumber']] = {'MP3': 'TRCK', 'FLAC': 'TRACKNUMBER'}
tagNameMap[tagNames['trackCount']] = {'MP3': 'TRCK', 'FLAC': 'TRACKTOTAL'}
tagNameMap[tagNames['album']] = {
    'MP3': 'TALB',
    'FLAC': 'ALBUM',
}
tagNameMap[tagNames['albumArtist']] = {
    'MP3': 'TPE2',
    'FLAC': 'ALBUMARTIST',
}
tagNameMap[tagNames['year']] = {
    'MP3': 'TDRC',
    'FLAC': 'YEAR',
}
tagNameMap[tagNames['title']] = {
    'MP3': 'TIT2',
    'FLAC': 'TITLE',
}
tagNameMap[tagNames['artist']] = {
    'MP3': 'TPE1',
    'FLAC': 'ARTIST',
}

tagSetMap = {}
tagSetMap[tagNames['trackNumber']] = {
    'MP3': lambda value: mutagen.id3.TRCK(encoding=3, text=value),
    'FLAC': lambda value: value,
}
tagSetMap[tagNames['trackCount']] = {
    'MP3': lambda value: mutagen.id3.TRCK(encoding=3, text=value),
    'FLAC': lambda value: value,
}
tagSetMap[tagNames['album']] = {
    'MP3': lambda value: mutagen.id3.TALB(encoding=3, text=value),
    'FLAC': lambda value: value,
}
tagSetMap[tagNames['albumArtist']] = {
    'MP3': lambda value: mutagen.id3.TPE2(encoding=3, text=value),
    'FLAC': lambda value: value,
}
tagSetMap[tagNames['year']] = {
    'MP3': lambda value: mutagen.id3.TDRC(encoding=3, text=value),
    'FLAC': lambda value: value,
}
tagSetMap[tagNames['title']] = {
    'MP3': lambda value: mutagen.id3.TIT2(encoding=3, text=value),
    'FLAC': lambda value: value,
}
tagSetMap[tagNames['artist']] = {
    'MP3': lambda value: mutagen.id3.TPE1(encoding=3, text=value),
    'FLAC': lambda value: value,
}

tagObjectMap = {
    'MP3': lambda: mutagen.id3.ID3(),
    'FLAC': lambda: mutagen._vorbis.VCommentDict(),
}


def getTag(tagName: str, track: str) -> Optional[str]:
    global i
    # print(i)
    if track in tagCache and tagName in tagCache[track]:
        return tagCache[track][tagName]

    if track not in tagCache:
        tagCache[track] = {}

    try:
        f = mutagen.File(track)
    except:
        print(track)
        return

    for tag in tagNames:
        mappedTagName = tagNameMap[tag][type(f).__name__]
        try:
            f.tags[mappedTagName]
        except Exception as e:
            tagCache[track][tag] = None
            continue

        tagContent = str(
            f.tags[mappedTagName]
            if not hasattr(f.tags[mappedTagName], '__len__')
            else f.tags[mappedTagName][0]
        )
        tagCache[track][tag] = tagContent

    writeTagCache()
    return tagCache[track][tagName]


def setTag(tagName: str, value: str, track: str):
    try:
        # track = _track.replace("”", '"').replace("“", '"').replace("\\'", "'")
        f = mutagen.File(track)
        tagKey = tagNameMap[tagName][type(f).__name__]
        if not f.tags:
            f.tags = tagObjectMap[type(f).__name__]()
        f.tags[tagKey] = tagSetMap[tagName][type(f).__name__](value)

        f.save(track)
        if track in tagCache:
            tagCache[track][tagName] = value
        else:
            tagCache[track] = {}
            tagCache[track][tagName] = value
        writeTagCache()
    except:
        return


def getAlbumTag(track: str) -> Optional[str]:
    return getTag(tagNames['album'], track)


def setAlbumTag(track: str, albumName: str) -> None:
    setTag(tagNames['album'], albumName, track)


def getAlbumArtistTag(track: str) -> Optional[str]:
    return getTag(tagNames['albumArtist'], track)


def setAlbumArtistTag(track: str, artistName: str) -> None:
    setTag(tagNames['albumArtist'], artistName, track)


def getYearTag(track: str) -> Optional[str]:
    tagContent = getTag(tagNames['year'], track)
    if tagContent and '-' in tagContent:
        parts = tagContent.split('-')
        year = parts[0]
        tagCache[track]['year'] = year
        return year
    return tagContent


def setYearTag(track: str, year: str) -> None:
    setTag(tagNames['year'], str(year), track)


def getTitleTag(track: str) -> Optional[str]:
    return getTag(tagNames['title'], track)


def setTitleTag(track: str, title: str) -> None:
    setTag(tagNames['title'], title, track)


def getArtistTag(track: str) -> Optional[str]:
    return getTag(tagNames['artist'], track)


def setArtistTag(track: str, title: str) -> None:
    setTag(tagNames['artist'], title, track)


def getTrackNumberTag(track: str) -> Optional[int]:
    tagContent = getTag(tagNames['trackNumber'], track)
    # Ideally, this should be handled by MP3 specific code
    if tagContent and track.endswith('mp3'):
        num = tagContent.split('/')[0]
        if num == 'None':
            return None
        return int(num) if num else None
    return int(tagContent) if tagContent else None


def setTrackNumberTag(track: str, number: int) -> None:
    trackCount = getTag(tagNames['trackCount'], track)
    if trackCount and track.endswith('mp3'):
        trackNumber = (
            str(number) + '/' + trackCount.split('/')[1]
            if len(trackCount.split('/')) > 1
            else str(number)
        )
    else:
        trackNumber = str(number)
    setTag(tagNames['trackNumber'], trackNumber, track)


def getTrackCountTag(track: str) -> Optional[int]:
    tagContent = getTag(tagNames['trackCount'], track)
    # Ideally, this should be handled by MP3 specific code
    if tagContent and '/' in tagContent:
        num = tagContent.split('/')[1]
        if num == 'None':
            return None
        try:
            return int(num) if num else None
        except:
            return None
    return int(tagContent) if tagContent else None


def setTrackCountTag(track: str, count: int) -> None:
    trackNumber = getTag(tagNames['trackNumber'], track)
    if trackNumber and track.endswith('mp3'):
        trackCount = trackNumber.split('/')[0] + '/' + str(count)
    else:
        trackCount = str(count)
    print(trackNumber, trackCount, count)
    setTag(tagNames['trackCount'], trackCount, track)


def getTrackTime(track: os.DirEntry) -> int:
    try:
        if track.path not in tagCache or 'time' not in tagCache[track.path]:
            if track.path not in tagCache:
                tagCache[track.path] = {}
            f = mutagen.File(track.path)
            tagCache[track.path]['time'] = f.info.length
        return tagCache[track.path]['time']
    except:
        return 0
