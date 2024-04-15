
from typing import Optional
from mutagen.mp4 import MP4
from utils.Tags import BaseTags


class MP4Tags(BaseTags):
    metadata: MP4

    def load(self):
        self._metadata = MP4(self.trackPath)

    def _getAlbumArtist(self) -> str:
        return str(self.metadata["aART"][0])

    def _getArtist(self) -> str:
        return str(self.metadata["\xa9ART"][0])

    def _getTitle(self) -> str:
        return str(self.metadata['\xa9nam'][0])

    def _getAlbum(self) -> str:
        return str(self.metadata['\xa9alb'][0])

    def _getYear(self) -> Optional[str]:
        if "\xa9day" not in self.metadata:
            return None
        return str(self.metadata['\xa9day'][0])

    def _getTrackNumber(self) -> Optional[int]:
        if 'trkn' not in self.metadata:
            return None
        return self.metadata['trkn'][0][0]

    def _getTrackCount(self) -> Optional[int]:
        if 'trkn' not in self.metadata:
            return None
        if len(self.metadata['trkn']) < 1:
            return None
        if len(self.metadata['trkn'][0]) < 2:
            return None
        return self.metadata['trkn'][0][1]

    def _updateAlbumArtistTag(self, albumArtist: str) -> None:
        self.metadata["aART"] = albumArtist
        self.metadata.save()

    def _updateArtistTag(self, artist: str) -> None:
        self.metadata["\xa9ART"] = artist
        self.metadata.save()

    def _updateTitleTag(self, title: str) -> None:
        self.metadata["\xa9nam"] = title
        self.metadata.save()

    def _updateAlbumTag(self, album: str) -> None:
        self.metadata["\xa9alb"] = album
        self.metadata.save()

    def _updateYearTag(self, year: str) -> None:
        self.metadata["\xa9day"] = [str(year)]
        self.metadata.save()

    def _updateTrackNumberTag(self, trackNumber: int) -> None:
        tagValue = (trackNumber, self.trackCount)
        if 'trkn' not in self.metadata:
            self.metadata['trkn'] = [tagValue]
        else:
            self.metadata['trkn'][0] = tagValue
        self.metadata.save()

    def _updateTrackCountTag(self, trackCount: int) -> None:
        self.metadata['trkn'][0] = (self.trackNumber, trackCount)
        self.metadata.save()
