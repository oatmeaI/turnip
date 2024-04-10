
from mutagen.flac import FLAC
from utils.Tags import BaseTags


class FLACTags(BaseTags):
    metadata: FLAC

    def load(self):
        self._metadata = FLAC(self.trackPath)

    def _getAlbumArtist(self) -> str:
        return str(self.metadata["ALBUMARTIST"])

    def _getArtist(self) -> str:
        return str(self.metadata["ARTIST"])

    def _getTitle(self) -> str:
        return str(self.metadata["TITLE"])

    def _getAlbum(self) -> str:
        return str(self.metadata["ALBUM"])

    def _getYear(self) -> str:
        return str(self.metadata["YEAR"])

    def _getTrackNumber(self) -> int:
        return int(self.metadata['TRACKNUMBER'])

    def _getTrackCount(self) -> int:
        return int(self.metadata['TRACKCOUNT'])

    def _updateAlbumArtistTag(self, albumArtist: str) -> None:
        self.metadata['ALBUMARTIST'] = albumArtist
        self.metadata.save()

    def _updateArtistTag(self, artist: str) -> None:
        self.metadata['ARTIST'] = artist
        self.metadata.save()

    def _updateTitleTag(self, title: str) -> None:
        self.metadata['TITLE'] = title
        self.metadata.save()

    def _updateAlbumTag(self, album: str) -> None:
        self.metadata['ALBUM'] = album
        self.metadata.save()

    def _updateYearTag(self, year: str) -> None:
        self.metadata['YEAR'] = year
        self.metadata.save()

    def _updateTrackNumberTag(self, trackNumber: int) -> None:
        self.metadata['TRACKNUMBER'] = trackNumber
        self.metadata.save()

    def _updateTrackCountTag(self, trackCount: int) -> None:
        self.metadata['TRACKCOUNT'] = trackCount
        self.metadata.save()
