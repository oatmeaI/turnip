import sys
from commands import folderStructure
from commands import emptyFolders
from commands import trackDuplicates
from commands import albumDuplicates
from commands import artistDuplicates
from commands import artistTagConflicts
from commands import artistTagFolderConflicts
from commands import albumTagConflicts
from commands import albumTagFolderConflicts
from commands import yearTagFolderConflicts
from commands import titleTagFileConflicts
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

    folderStructure.verify(rootDir)
    count = emptyFolders.process(rootDir)

    count += artistDuplicates.ArtistDuplicates().process()
    count += albumDuplicates.AlbumDuplicates().process()
    count += trackDuplicates.TrackDuplicates().process()

    count += artistTagConflicts.ArtistTagConflicts().process()
    count += artistTagFolderConflicts.ArtistTagFolderConflicts().process()
    count += albumTagConflicts.process(rootDir)
    count += albumTagFolderConflicts.process(rootDir)
    count += yearTagFolderConflicts.process(rootDir)

    count += featInTitle.process(rootDir)

    count += titleTagFileConflicts.TitleTagFileConflicts().process()
    count += numberTagFileConflicts.process(rootDir)
    count += featInAlbumArtist.process(rootDir)
    count += listInAlbumArtist.process(rootDir)
    count += featInAlbum.process(rootDir)
    count += replace.process(rootDir)

    count += countTagConflicts.process(rootDir)
    count += missingTrackCounts.process(rootDir)
    count += conflictedTrackNumbers.process(rootDir)
    count += missingTrackNumbers.process(rootDir)

    count += missingTracks.process(rootDir)

    print(str(count) + " issues resolved")


commands = {
    "clean": clean,
    "verifyFolderStructure": folderStructure.verify,
    "removeEmptyFolders": emptyFolders.process,
    "trackDuplicates": trackDuplicates.process,
    "albumDuplicates": albumDuplicates.process,
    "artistDuplicates": artistDuplicates.ArtistDuplicates().process,
    "artistTagConflicts": artistTagConflicts.ArtistTagConflicts().process,
    "artistTagFolderConflicts": artistTagFolderConflicts.ArtistTagFolderConflicts().process,
    "albumTagConflicts": albumTagConflicts.process,
    "albumTagFolderConflicts": albumTagFolderConflicts.process,
    "yearTagFolderConflicts": yearTagFolderConflicts.process,
    "featInTitle": featInTitle.process,
    "featInAlbum": featInAlbum.process,
    "titleTagFileConflicts": titleTagFileConflicts.TitleTagFileConflicts().process,
    "numberTagFileConflicts": numberTagFileConflicts.process,
    "countTagConflicts": countTagConflicts.process,
    "missingTrackCounts": missingTrackCounts.process,
    "conflictedTrackNumbers": conflictedTrackNumbers.process,
    "missingTrackNumbers": missingTrackNumbers.process,
    "featInAlbumArtist": featInAlbumArtist.process,
    "listInAlbumArtist": listInAlbumArtist.process,
    "missingTracks": missingTracks.process,
    "replace": replace.process,
}


def main():
    commandName = sys.argv[1]
    # rootDir = sys.argv[2]

    commands[commandName]()
    writeTagCache()


main()
