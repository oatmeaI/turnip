import math
from prettytable import PrettyTable
from Command.Command import TrackCommand
from Command.Issue import TrackIssue
from Entry.Album import Album
from Entry.Artist import Artist
from Entry.Track import Track


class Info(TrackCommand):
    def detectIssue(self, artist: Artist, album: Album, track: Track):
        return TrackIssue(artist=artist, album=album, track=track, original='Show Info', delta='')

    def callback(self, good, issue: TrackIssue):
        if good:
            track = issue.track

            # TODO - should be done by track class
            minutes = math.trunc(float(track.length)/60)
            seconds = math.trunc(round(float(track.length)%60))
            # TODO - should be in utility
            if seconds < 10:
                seconds = '0' + str(seconds)

            table = PrettyTable()
            table.field_names = ["Property", "Value"]
            table.add_row(["Title", track.title])
            table.add_row(["Length", str(minutes) + ":" + str(seconds)])
            table.add_row(["Album", track.album])
            table.add_row(["Year", track.year])
            table.add_row(["Artist", track.artist])
            table.add_row(["Album Artist", track.albumArtist])
            table.add_row(["Track Number", str(track.trackNumber) + '/' + str(track.trackCount)])
            table.add_row(["Path", track.path])
            table.add_row(["Bitrate", track.bitrate])
            table.add_row(["Size", str(track.size) + 'mb'])
            table.align["Property"] = "r"
            table.align["Value"] = "l"
            print(table)
