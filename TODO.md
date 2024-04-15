# TODO

(Items marked with ! are currently blocking me from using this myself)

## Bugs

- 'ignore album/artist' options
- replace fancy ' with normal '
- delete option?
- concept of trackwise/albumwise/artistwise commands? - hacked this on yearConflicts
- recognize pt. 1 / pt. 2 etc
- find instrumentals / deluxes and remove
- ! Disc numbers
- ! Tidal search isn't always giving results that it should - also non-english text breaks
- ! conflictedTrackNumbers: this command is kind of useless, rework entirely
- add option to update track count in fixMissingTracks
- only rip missing tracks
- put in your own url for tidal ripping
- Replace: use regex for partial replacements? Not sure if I need this but it seems useful
- Feedback when we add "\_1" to a filename
- Titlecase command
- We seem to add numbers in the wrong place if the filename has . in it
- "similar resolution" thing doesn't work for trackDuplicates
- util.py:152: dedupe options in buildOptions / from suggestions
- artistTagFolderConflicts: deduping isn't working
- artistTagFolderConflicts: heuristics
- replace.py:28: "this breaks when the file doesn't have the special character" - not sure what this means
- numberTagFileConflicts: dedupe options
- Incorrect choice numbers when skipping issue options
- Issue count is incorrect after skipAllSimilar or ignoreAllSimilar
- trailing slashes on rootdir break everything
- handle 401 from tidal

## Refactoring

- find compilations / various artists that are split
- Compilation albums have various years, that's probably good...?
- Should replace happen before everything else as it would help identify duplicates etc?
- featInTitle: clean up callback method, use infinite corrections input method
- featInAlbumArtist: clean up callback method, use infinite corrections input method
- featInAlbumArtist:82: helper for building album paths
- newFix -> suggest: something less janky than just setting "key" to "NONE" - probably a new type
- replace: "auto" setting is janky
- all find issues methods: I think returning an array is dumb? rethink
- check for type errors, untyped stuff, warnings etc everywhere
- Keyed arguments with defaults pls - ie. clean up the way stuff is passed around

## Incremental Features

- clean caches command - delete stuff for files that no longer exist
- Strip trailing spaces everywhere
- strict duplicate track mode that only searches within artist folder for better speed
- Add "count" command that gives statistics and issue counts
- [listInAlbumArtist / listInX] - detect 'and' '&' ',' in artist tags (build listInX commands)
- Always print what we're doing in CB
- tidal.py:76: fuzzy filter instead of strict matching
- util.py:225: give feedback when skipping b/c no options; make configurable whether it skips or not
- trackDuplicates: implement heuristics
- albumTagFolderConflicts: heuristics
- numberTagFileConflicts: heuristics, multi-disc numbers
- countTagConflicts: heuristics, multi-disc numbers, de-duping
- replace: skips errors when track doesn't exist anymore (due to rename) - can we fix this?
- find feat artists in artist tag already and strip them
- update fixMissingTracks heuristic - pick item with the same number of tracks as expected
- limit option for debugging
- highlight stuff we're asking for confirmation on
- backup ignorecache before running?
- X Custom issue display (ie. list size for mp3)

## Big Features

- o abstract find & replace
- o consider a better flow for dealing with albums with lots of dupes (greatest hits etc)
- o look for deluxe editions etc I don't want
- command to ensure title case everywhere (a command somewhere is enforcing title case a side effect; that's bad)
- detect extra songs
- improve dupe detection accuracy & efficiency
- convert 24/92 FLAC to 16/44?
- define desired format, functions to transform Tidal data into desired format; also tag -> filename transform
- get rid of feat in suggestions from tidal (should be able to reuse code)
- some sort of undo technology?
- add remix artist to artist field (maybe?)
- Clean up UI, output, input, etc
- Configuration options
- Don't run string compare on pairings that have been ignored??
- Better naming scheme for commands
- Tests
- Flag minimum bitrate
- Plugin architecture?
- Issue caching?
- Fix file structure issues instead of just warning
- Add "buildCache" function which just loads all the data we need into caches for faster searching etc
- Writing tags takes a long time - any way to queue that, so that the user can keep going?
- Configure file separator for different OSes?
