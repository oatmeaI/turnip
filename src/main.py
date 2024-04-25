import atexit
from Search.SearchService import SearchService
from Search.Spotify.SpotifyGateway import SpotifyGateway
from commands.CheckFileNames import CheckFileNames
from commands.CheckInfo import CheckInfo
from commands.FeatInAlbum import FeatInAlbum
from commands.FeatInAlbumArtist import FeatInAlbumArtist
from commands.FeatInArtist import FeatInArtist
from commands.FeatInTitle import FeatInTitle
from commands.Info import Info
from commands.ListInAlbumArtist import ListInAlbumArtist
from commands.NumberTagFileConflicts import NumberTagFileConflicts
from commands.RemoveBrokenFiles import RemoveBrokenFiles
from commands.RemoveEmptyFolders import RemoveEmptyFolders
from commands.FixAlbumArtist import FixAlbumArtist
# from commands.albumArtistTagConflicts import AlbumArtistTagConflicts
# from commands.albumTagFolderConflicts import AlbumTagFolderConflicts
# from commands.albumArtistFolderConflicts import AlbumArtistFolderConflicts
from commands.FixAlbum import FixAlbum
from commands.Replace import Replace
from commands.Set import SetTag
from commands.fixYear import FixYear
from commands.FixTitles import FixTitles
from commands.ArtistDuplicates import ArtistDuplicates
from commands.AlbumDuplicates import AlbumDuplicates
from commands.TrackDuplicates import TrackDuplicates
from commands.FolderStructure import FolderStructure
from utils.TagCache import TagCache
from utils.constants import args


# def clean():
#     count = 0
#
#     FolderStructure().process()
#     count = emptyFolders.process()
#
#     count += artistDuplicates.ArtistDuplicates().process()
#     count += albumDuplicates.AlbumDuplicates().process()
#     count += trackDuplicates.TrackDuplicates().process()
#
#     count += AlbumArtistTagConflicts().process()
#     count += AlbumArtistFolderConflicts().process()
#     count += albumTagConflicts.process(rootDir)
#     count += albumTagFolderConflicts.process()
#     count += yearTagFolderConflicts.process()
#
#     count += featInTitle.process()
#
#     count += TitleTagFileConflicts().process()
#     count += NumberTagFileConflicts().process()
#     count += featInAlbumArtist.process(rootDir)
#     count += listInAlbumArtist.process(rootDir)
#     count += featInAlbum.process()
#     count += replace.Replace().process()
#
#     count += countTagConflicts.process(rootDir)
#     count += missingTrackCounts.process(rootDir)
#     count += conflictedTrackNumbers.process(rootDir)
#     count += missingTrackNumbers.process()
#
#     count += missingTracks.process()
#
#     print(str(count) + ' issues resolved')

commands = {
    'verifyFolderStructure': FolderStructure,
    'removeEmptyFolders': RemoveEmptyFolders,
    'brokenFiles': RemoveBrokenFiles,
    'albumArtist': FixAlbumArtist,
    'album': FixAlbum,
    'year': FixYear,
    'title': FixTitles,
    'artistDuplicates': ArtistDuplicates,
    'albumDuplicates': AlbumDuplicates,
    'trackDuplicates': TrackDuplicates,
    'featInTitle': FeatInTitle,
    'featInAlbum': FeatInAlbum,
    'featInArtist': FeatInArtist,
    'listInAlbumArtist': ListInAlbumArtist,
    'featInAlbumArtist': FeatInAlbumArtist,
    'numberTagFileConflicts': NumberTagFileConflicts,
    'replace': Replace,
    'info': Info,
    'set': SetTag,
    'checkInfo': CheckInfo,
    'checkFileNames': CheckFileNames
    # 'countTagConflicts': countTagConflicts.process,
    # 'missingTrackCounts': missingTrackCounts.process,
    # 'conflictedTrackNumbers': conflictedTrackNumbers.process,
    # 'missingTrackNumbers': missingTrackNumbers.process,
    # 'missingTracks': missingTracks.process,
}


def exitHandler():
    print("Saving tag cache")
    TagCache.writeCache()
    print("Closing Spotify connection")
    SearchService.tearDown()


def clean():
    for command in commands.keys():
        commands[command]().process()


def main():
    try:
        if args.command == 'clean':
            clean()
        else:
            commands[args.command]().process()
    except Exception as e:
        exitHandler()
        raise e


atexit.register(exitHandler)
main()
