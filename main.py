import sys
from commands import folderStructure
from commands import emptyFolders
from commands import trackDuplicates
from commands import albumDuplicates
from commands import artistDuplicates
from commands import artistTagConflicts
from commands.artistFolderConflicts import ArtistFolderConflicts
from commands import albumTagConflicts
from commands import albumTagFolderConflicts
from commands import yearTagFolderConflicts
from commands.titleTagFileConflicts import TitleTagFileConflicts
from commands.folderStructure import FolderStructure
from commands import numberTagFileConflicts
from commands import countTagConflicts
from commands import missingTrackCounts
from commands import conflictedTrackNumbers
from commands import missingTrackNumbers
from commands import missingTracks
from commands import featInTitle
from commands import featInAlbumArtist
from commands import featInAlbum
from commands import listInAlbumArtist
from commands import replace
from utils.tagging import writeTagCache
from utils.constants import rootDir


def clean():
    count = 0

    FolderStructure().process()
    count = emptyFolders.process()

    count += artistDuplicates.ArtistDuplicates().process()
    count += albumDuplicates.AlbumDuplicates().process()
    count += trackDuplicates.TrackDuplicates().process()

    count += artistTagConflicts.ArtistTagConflicts().process()
    count += ArtistFolderConflicts().process()
    count += albumTagConflicts.process(rootDir)
    count += albumTagFolderConflicts.process()
    count += yearTagFolderConflicts.process()

    count += featInTitle.process()

    count += TitleTagFileConflicts().process()
    count += numberTagFileConflicts.process(rootDir)
    count += featInAlbumArtist.process(rootDir)
    count += listInAlbumArtist.process(rootDir)
    count += featInAlbum.process()
    count += replace.Replace().process()

    count += countTagConflicts.process(rootDir)
    count += missingTrackCounts.process(rootDir)
    count += conflictedTrackNumbers.process(rootDir)
    count += missingTrackNumbers.process()

    count += missingTracks.process()

    print(str(count) + ' issues resolved')


commands = {
    'clean': clean,
    'brokenFiles': emptyFolders.fixBrokenFiles,
    'verifyFolderStructure': folderStructure.verify,
    'removeEmptyFolders': emptyFolders.process,
    'trackDuplicates': trackDuplicates.TrackDuplicates().process,
    'albumDuplicates': albumDuplicates.AlbumDuplicates().process,
    'artistDuplicates': artistDuplicates.ArtistDuplicates().process,
    'artistTagConflicts': artistTagConflicts.ArtistTagConflicts().process,
    'artistFolderConflicts': ArtistFolderConflicts().process,
    'albumTagConflicts': albumTagConflicts.process,
    'albumTagFolderConflicts': albumTagFolderConflicts.process,
    'yearTagFolderConflicts': yearTagFolderConflicts.process,
    'featInTitle': featInTitle.process,
    'featInAlbum': featInAlbum.process,
    'titleTagFileConflicts': TitleTagFileConflicts().process,
    'numberTagFileConflicts': numberTagFileConflicts.process,
    'countTagConflicts': countTagConflicts.process,
    'missingTrackCounts': missingTrackCounts.process,
    'conflictedTrackNumbers': conflictedTrackNumbers.process,
    'missingTrackNumbers': missingTrackNumbers.process,
    'featInAlbumArtist': featInAlbumArtist.process,
    'listInAlbumArtist': listInAlbumArtist.process,
    'missingTracks': missingTracks.process,
    'replace': replace.Replace().process,
}


def main():
    commandName = sys.argv[1]
    commands[commandName]()
    writeTagCache()


main()
