from thefuzz import fuzz
from Command.Command import TrackCommand
from Command.Issue import Issue, TrackIssue
from Command.Option import Option
from Entry.Album import Album
from Entry.Artist import Artist
from Entry.Track import Track
from Search.SearchResult import TrackSearchResult
from Search.SearchService import SearchService
from utils.fs import stripRootPath
from utils.userio import chooseFromList, promptHeader

# TODO transform search values before comparing
# TODO better feedback about what's happening


class CheckInfo(TrackCommand):
    allowEdit = True

    def score(self, track: Track, result: TrackSearchResult):
        titleScore = fuzz.ratio(track.title, result.track)
        artistScore = fuzz.ratio(track.artist, result.artist)
        albumScore = fuzz.ratio(track.album, result.album)
        return (titleScore+artistScore+albumScore)/3

    def detectIssue(self, artist: Artist, album: Album, track: Track):
        results = SearchService.searchTrack(track)
        if len(results) < 1:
            return None

        if len(results) > 1:
            score = self.score(track, results[0])
            if score > 80:
                searchResult = results[0]
            else:
                print(" ")
                options = [Option(key="s", value="skip", display="skip")]
                for i, result in enumerate(results):
                    if i > 10:
                        break
                    display = f"{result.track} by {result.artist} on {result.album}"
                    options.append(Option(key=str(i+1), value=i, display=display))

                choice = chooseFromList(options)

                if choice == "skip":
                    return None

                searchResult = results[int(choice)]
        else:
            searchResult = results[0]

        # TODO - dedupe this code
        found = []
        if searchResult.artist != track.artist:
            found.append(TrackIssue(
                artist=artist,
                album=album,
                track=track,
                original=track.artist,
                delta=searchResult.artist,
                data='artist'
                ))

        if searchResult.track != track.title:
            found.append(TrackIssue(
                artist=artist,
                album=album,
                track=track,
                original=track.title,
                delta=searchResult.track,
                data='title'
                ))

        if searchResult.album != track.album:
            found.append(TrackIssue(
                artist=artist,
                album=album,
                track=track,
                original=track.album,
                delta=searchResult.album,
                data='album'
                ))

        if str(searchResult.year) != track.year:
            found.append(TrackIssue(
                artist=artist,
                album=album,
                track=track,
                original=track.year,
                delta=str(searchResult.year),
                data='year'
                ))

        # TODO - comparing artist to album artist here...
        if searchResult.artist != track.albumArtist:
            found.append(TrackIssue(
                artist=artist,
                album=album,
                track=track,
                original=track.albumArtist,
                delta=searchResult.artist,
                data='albumArtist'
                ))
        return found

    def prompt(self, issue: TrackIssue, index: int, count: int):
        header = promptHeader(self.__class__.__name__, index, count)
        path = stripRootPath(issue.track.path.realPath)
        return f"{header}\n{self.cta} {path} -> {issue.data}"

    def callback(self, good, issue: TrackIssue):
        if issue.data == 'album':
            issue.track.setAlbum(good)
        if issue.data == 'title':
            issue.track.setTitle(good)
        if issue.data == 'artist':
            issue.track.setArtist(good)
        if issue.data == 'albumArtist':
            issue.track.setAlbumArtist(good)
        if issue.data == 'year':
            issue.track.setYear(good)
