import atexit
from typing import Set
from commands.FeatInAlbum import FeatInAlbum
from commands.FeatInArtist import FeatInArtist
from commands.FeatInTitle import FeatInTitle
from commands.Info import Info
from commands.RemoveEmptyFolders import RemoveEmptyFolders
from commands.FixAlbumArtist import FixAlbumArtist
# from commands.albumArtistTagConflicts import AlbumArtistTagConflicts
# from commands.albumTagFolderConflicts import AlbumTagFolderConflicts
# from commands.albumArtistFolderConflicts import AlbumArtistFolderConflicts
from commands.FixAlbum import FixAlbum
from commands.Replace import Replace
from commands.Set import SetCommand
from commands.fixYear import FixYear
from commands.FixTitles import FixTitles
from commands.ArtistDuplicates import ArtistDuplicates
from commands.AlbumDuplicates import AlbumDuplicates
from commands.TrackDuplicates import TrackDuplicates
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

# TODO why is writing to the tagcache so much
# TODO - no results from Tidal for some stuff, why?
commands = {
    'removeEmptyFolders': RemoveEmptyFolders,
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
    'replace': Replace,
    'info': Info,
    'set': SetCommand
    # 'clean': clean,
    # 'brokenFiles': emptyFolders.fixBrokenFiles,
    # 'verifyFolderStructure': folderStructure.verify,
    # 'numberTagFileConflicts': NumberTagFileConflicts().process,
    # 'countTagConflicts': countTagConflicts.process,
    # 'missingTrackCounts': missingTrackCounts.process,
    # 'conflictedTrackNumbers': conflictedTrackNumbers.process,
    # 'missingTrackNumbers': missingTrackNumbers.process,
    # 'featInAlbumArtist': featInAlbumArtist.process,
    # 'listInAlbumArtist': listInAlbumArtist.process,
    # 'missingTracks': missingTracks.process,
}


def exitHandler():
    print("Saving tag cache")
    TagCache.writeCache()


def main():
    try:
        commands[args.command]().process()
    except Exception as e:
        exitHandler()
        raise e


atexit.register(exitHandler)
main()
