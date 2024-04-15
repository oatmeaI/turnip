import sys
import atexit
from commands.albumArtistTagConflicts import AlbumArtistTagConflicts
from commands.albumTagConflicts import AlbumTagConflicts
from commands.albumTagFolderConflicts import AlbumTagFolderConflicts
from commands.albumArtistFolderConflicts import AlbumArtistFolderConflicts
from commands.fixYear import FixYear
from commands.FixTitles import FixTitles
from utils.TagCache import TagCache


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
    'albumArtistTagConflicts': AlbumArtistTagConflicts,
    'albumTagConflicts': AlbumTagConflicts,
    'albumTagFolderConflicts': AlbumTagFolderConflicts,
    'albumArtistFolderConflicts': AlbumArtistFolderConflicts,
    'year': FixYear,
    'title': FixTitles,
    # 'trackDuplicates': trackDuplicates.TrackDuplicates().process,
    # 'clean': clean,
    # 'brokenFiles': emptyFolders.fixBrokenFiles,
    # 'verifyFolderStructure': folderStructure.verify,
    # 'removeEmptyFolders': emptyFolders.process,
    # 'albumDuplicates': albumDuplicates.AlbumDuplicates().process,
    # 'artistDuplicates': artistDuplicates.ArtistDuplicates().process,
    # 'featInTitle': featInTitle.process,
    # 'featInAlbum': featInAlbum.process,
    # 'numberTagFileConflicts': NumberTagFileConflicts().process,
    # 'countTagConflicts': countTagConflicts.process,
    # 'missingTrackCounts': missingTrackCounts.process,
    # 'conflictedTrackNumbers': conflictedTrackNumbers.process,
    # 'missingTrackNumbers': missingTrackNumbers.process,
    # 'featInAlbumArtist': featInAlbumArtist.process,
    # 'listInAlbumArtist': listInAlbumArtist.process,
    # 'missingTracks': missingTracks.process,
    # 'replace': replace.Replace().process,
}


def exitHandler():
    print("Saving tag cache")
    TagCache.writeCache()


def main():
    commandName = sys.argv[1]
    try:
        commands[commandName]().process()
    except Exception as e:
        exitHandler()
        raise e


atexit.register(exitHandler)
main()
