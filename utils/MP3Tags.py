from typing import Optional
from mutagen.id3._frames import TRCK, TALB, TPE2, TDRC, TIT2, TPE1
from mutagen.mp3 import MP3
from utils.Tags import BaseTags


class MP3Tags(BaseTags):
    metadata: MP3

    def load(self):
        self._metadata = MP3(self.trackPath)

    def _getAlbumArtist(self) -> Optional[str]:
        if 'TPE2' not in self.metadata:
            return None
        return str(self.metadata["TPE2"])

    def _getArtist(self) -> str:
        return str(self.metadata["TPE1"])

    def _getTitle(self) -> str:
        return str(self.metadata["TIT2"])

    def _getAlbum(self) -> Optional[str]:
        if "TALB" not in self.metadata:
            return None
        return str(self.metadata["TALB"])

    def _getYear(self) -> Optional[str]:
        if 'TDRC' not in self.metadata:
            return None
        return str(self.metadata["TDRC"])

    def _getTrackNumber(self) -> Optional[int]:
        if "TRCK" not in self.metadata:
            return None
        trackString = str(self.metadata["TRCK"])
        if not trackString:
            return None
        num = trackString.split('/')[0]
        return int(num)

    def _getTrackCount(self) -> Optional[int]:
        if "TRCK" not in self.metadata:
            return None
        trackString = str(self.metadata["TRCK"])
        if not trackString:
            return None
        split = trackString.split('/')
        if len(split) < 2:
            return None
        if not split[1]:
            return None

        return int(split[1])

    def _updateAlbumArtistTag(self, albumArtist: str) -> None:
        self.metadata["TPE2"] = TPE2(encoding=3, text=albumArtist)
        self.metadata.save()

    def _updateArtistTag(self, artist: str) -> None:
        self.metadata["TPE1"] = TPE1(encoding=3, text=artist)
        self.metadata.save()

    def _updateTitleTag(self, title: str) -> None:
        self.metadata["TIT2"] = TIT2(encoding=3, text=title)
        self.metadata.save()

    def _updateAlbumTag(self, album: str) -> None:
        self.metadata["TALB"] = TALB(encoding=3, text=album)
        self.metadata.save()

    def _updateYearTag(self, year: str) -> None:
        self.metadata["TDRC"] = TDRC(encoding=3, text=year)
        self.metadata.save()

    def _updateTrackNumberTag(self, trackNumber: int) -> None:
        trackCount = str(self.trackCount) if self.trackCount else ''
        trackString = str(trackNumber) + "/" + trackCount
        self.metadata["TRCK"] = TRCK(encoding=3, text=trackString)
        self.metadata.save()

    def _updateTrackCountTag(self, trackCount: int) -> None:
        trackString = str(self.trackNumber) + "/" + str(trackCount)
        self.metadata["TRCK"] = TRCK(encoding=3, text=trackString)
        self.metadata.save()
