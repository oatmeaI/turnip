# TODO

(Items marked with ! are currently blocking me from using this myself)

## Bugs

-   ! Disc numbers
-   X SkipSimilar for TitleTagFileConflicts should skip album
    -   ! same for numberTagFileConflicts
-   ! similarKey for countTagConflicts is wrong
    -   ! same for missingTrackCounts
    -   ! same for missingTrackNumbers
-   ! Case sensitivity is fucked
-   ! replace: support regex (will require config to work also)
-   ! conflictedTrackNumbers is kinda useless, can't tell what it's doing
-   ! AlbumTagConflicts doesn't run
-   ! Crash in ArtistTagConflicts
-   ! Tidal search isn't always giving results that it should - also non-english text breaks
-   ! skipSimilar in duplicate tracks will skip other tracks from the same 2 albums (for dealing with greatest hits, etc)
-   ! conflictedTrackNumbers: this command is kind of useless, rework entirely
-   ! add option to update track count in fixMissingTracks
-   ! only rip missing tracks
-   ! put in your own url for tidal ripping
-   Feedback when we add "_1" to a filename
-   Unicode normalization in central place
-   Titlecase command
-   We seem to add numbers in the wrong place if the filename has . in it
-   Does similar work for yearTagFolderConflicts?
-   Don't enter the same album more than once in yearTagFolderConflicts
-   "similar resolution" thing doesn't work for trackDuplicates
-   util.py:152: dedupe options in buildOptions / from suggestions
-   tagging.py:141: Might need to transform tag values before setting into cache
-   artistTagFolderConflicts: deduping isn't working
-   artistTagFolderConflicts: heuristics
-   replace.py:28: "this breaks when the file doesn't have the special character" - not sure what this means
-   numberTagFileConflicts: dedupe options
-   Incorrect choice numbers when skipping issue options
-   Issue count is incorrect after skipAllSimilar or ignoreAllSimilar
-   trailing slashes on rootdir break everything
-   handle 401 from tidal

## Refactoring

-   Move Command class to central location, migrate everything to use the Command class
-   featInTitle: clean up callback method, use infinite corrections input method
-   featInAlbumArtist: clean up callback method, use infinite corrections input method
-   featInAlbumArtist:82: helper for building album paths
-   newFix -> suggest: something less janky than just setting "key" to "NONE" - probably a new type
-   fs.py:26: use file name helper instead of building file name by hand
-   featInTitle -> process: cyclomatic complexity warning
-   replace: "auto" setting is janky
-   tagging.py:42: the config maps here are a god damn mess
-   all find issues methods: I think returning an array is dumb? rethink
-   dedupe lots of code for processing strings etc (for example, changing a title tag should always change the filename)
-   check for type errors, untyped stuff, warnings etc everywhere
-   Keyed arguments with defaults pls - ie. clean up the way stuff is passed around

## Incremental Features

-	clean caches command - delete stuff for files that no longer exist
-   Strip trailing spaces everywhere
-   strict duplicate track mode that only searches within artist folder for better speed
-   findMissingYear
-   Add "count" command that gives statistics and issue counts
-   [listInAlbumArtist / listInX] - detect 'and' '&' ',' in artist tags (build listInX commands)
-   Always print what we're doing in CB
-   Allow passing different similarKey formula
-   tidal.py:76: fuzzy filter instead of strict matching
-   util.py:225: give feedback when skipping b/c no options; make configurable whether it skips or not
-   trackDuplicates: implement heuristics
-   albumTagFolderConflicts: heuristics
-   numberTagFileConflicts: heuristics, multi-disc numbers
-   countTagConflicts: heuristics, multi-disc numbers, de-duping
-   replace: skips errors when track doesn't exist anymore (due to rename) - can we fix this?
-   find feat artists in artist tag already and strip them
-   update fixMissingTracks heuristic - pick item with the same number of tracks as expected
-   setting to skip stuff with no good suggestions? ie year, NONE and 0000
-   limit option for debugging
-   highlight stuff we're asking for confirmation on
-   backup ignorecache before running?
- 	X Custom issue display (ie. list size for mp3)

## Big Features

-   o abstract find & replace
-   o consider a better flow for dealing with albums with lots of dupes (greatest hits etc)
-   o "set" command to set arbitrary tag on track / album / artist
-   o look for deluxe editions etc I don't want
-   m4a support, since tidal sometimes gives me those
-   command to ensure title case everywhere (a command somewhere is enforcing title case a side effect; that's bad)
-   detect extra songs
-   improve dupe detection accuracy & efficiency
-   convert 24/92 FLAC to 16/44?
-   define desired format, functions to transform Tidal data into desired format; also tag -> filename transform
-   get rid of feat in suggestions from tidal (should be able to reuse code)
-   some sort of undo technology?
-   add remix artist to artist field (maybe?)
-   Clean up UI, output, input, etc
-   Configuration options
-   Don't run string compare on pairings that have been ignored??
-   Better naming scheme for commands
-   Tests
-   Flag minimum bitrate
-   Plugin architecture?
-   Issue caching?
-   Fix file stucture issues instead of just warning
-   Add "buildCache" function which just loads all the data we need into caches for faster searching etc
-   Writing tags takes a long time - any way to queue that, so that the user can keep going?
-   Configure file separator for different OSes?
-   Debounce / queue pickle writing
