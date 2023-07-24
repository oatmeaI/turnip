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
from utils.fs import rmFile
from utils.tagging import writeTagCache


def clean(rootDir):
    count = 0
    print("\n\nChecking file structure...")
    folderStructure.verify(rootDir)
    count = emptyFolders.process(rootDir)

    print("\n\nLooking for duplicates...")
    count += artistDuplicates.process(rootDir)
    count += albumDuplicates.process(rootDir)
    count += trackDuplicates.process(rootDir)

    print("\n\nChecking metadata...")
    count += artistTagConflicts.process(rootDir)
    count += artistTagFolderConflicts.process(rootDir)
    count += albumTagConflicts.process(rootDir)
    count += albumTagFolderConflicts.process(rootDir)
    count += yearTagFolderConflicts.process(rootDir)

    count += featInTitle.process(rootDir)

    count += titleTagFileConflicts.process(rootDir)
    count += numberTagFileConflicts.process(rootDir)
    count += featInAlbumArtist.process(rootDir)
    count += listInAlbumArtist.process(rootDir)
    count += featInAlbum.process(rootDir)
    count += replace.process(rootDir)

    print("\n\nChecking track counts...")
    count += countTagConflicts.process(rootDir)
    count += missingTrackCounts.process(rootDir)
    count += conflictedTrackNumbers.process(rootDir)
    count += missingTrackNumbers.process(rootDir)

    print("\n\nLooking for missing tracks...")
    count += missingTracks.process(rootDir)

    print(str(count) + " issues resolved")


commands = {
    "clean": clean,
    "verifyFolderStructure": folderStructure.verify,
    "removeEmptyFolders": emptyFolders.process,
    "trackDuplicates": trackDuplicates.process,
    "albumDuplicates": albumDuplicates.process,
    "artistDuplicates": artistDuplicates.process,
    "artistTagConflicts": artistTagConflicts.process,
    "artistTagFolderConflicts": artistTagFolderConflicts.process,
    "albumTagConflicts": albumTagConflicts.process,
    "albumTagFolderConflicts": albumTagFolderConflicts.process,
    "yearTagFolderConflicts": yearTagFolderConflicts.process,
    "featInTitle": featInTitle.process,
    "featInAlbum": featInAlbum.process,
    "titleTagFileConflicts": titleTagFileConflicts.process,
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
    dir = sys.argv[2]

    commands[commandName](dir)
    writeTagCache()


main()