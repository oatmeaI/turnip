# TODO

Note: this is pretty messy currently; I'm going to sort through it and clean it up soon, as well as come up with an actual roadmap.

## Special characters:

-   artistTagFolderConflicts: trailing periods and other special characters in artist folders breaks
-   forward slash in conflicted track names breaks shit
-   featInTitle: forward slash in file path seems to break featInTitle for some reason
-   albumTagFolderConflicts: don't let stuff start with '.', replace '/' with '\_'

## Misc:

### V1:

-   probably just strip trailing spaces everywhere
-   one method for parsing ALL data out of file path, deprecate others
-   count command that gives statistics and issue counts
-   featInTitle is breaking on lost cause
-   artistTagConflicts isn't working?
-   [listInAlbumArtist / listInX] - detect 'and' '&' ',' in artist tags (build listInX commands)
-   always print what we're doing in CB
-   incorrect choice numbers when skipping issue options
-   allow passing different similarKey formula
-   deal with special characters in file paths everywhere
-   tidal search isn't always giving results that it should - also non-english text breaks
-   deal with multi-disc track numbers
-   conflictedTrackNumbers: this command is kind of useless, rework entirely
-   > yearTagFolderConflicts: remove "None"s from options
-   > featInTitle: clean up callback method, use infinite corrections input method
-   > featInAlbumArtist: clean up callback method, use infinite corrections input method
-   > featInAlbumArtist:83: helper for building album paths
-   > tidal.py:76: fuzzy filter instead of strict matching
-   > util.py:225: give feedback when skipping b/c no options; make configurable whether it skips or not
-   > util.py:152: dedupe options in buildOptions / from suggestions
-   > trackDuplicates: implement heuristics
-   > newFix->suggest: something less janky than just setting "key" to "NONE" - probably a new type
-   > fs.py:26: use file name helper instead of building file name by hand
-   > path.py:61: deprecate splitFileName(why?)
-   > path.py:11: deal with character substitutions in paths...not sure how
-   > tagging.py:141: Might need to transform tag values before setting into cache
-   > featInTitle->process: cyclomatic complexity warning
-   > albumTagFolderConflicts: heuristics
-   > artistTagFolderConflicts: deduping isn't working
-   > numberTagFileConflicts: heuristics, multi-disc numbers
-   > countTagConflicts: heuristics, multi-disc numbers, de-duping
-   > replace.py:28: "this breaks when the file doesn't have the special character" - not sure what this means
-   > replace: support regex
-   > replace: "auto" setting is janky
-   > replace: skips errors when track doesn't exist anymore (due to rename) - can we fix this?
-   > tagging.py:42: the config maps here are a god damn mess
-   > all find issues methods: I think returning an array is dumb? rethink
-   > find feat artists in artist tag already and strip them
-   > add option to update track count in fixMissingTracks
-   > filter ignorecache first so that we have an accurate count
-   > update fixMissingTracks heuristic - pick item with the same number of tracks as expected
-   > m4a support, since tidal sometimes gives me those
-   > dedupe lots of code for processing strings etc
-   > for example, changing a title tag should always change the filename,
-   > same for album artist tag, etc; stripping characters when saving & comparing strings...
-   > command to ensure title case everywhere
-   > detect extra songs
-   > handle file errors / changed paths on featInTitle
-   > why lots of fixConflictedArtistFolders entries for riff raff?
-   > setting to skip stuff with no good suggestions? ie year, NONE and 0000
-   > limit option for debugging
-   > improve dupe detection accuracy & efficiency
-   > > consider a better flow for dealing with albums with lots of dupes (greatest hits etc)
-   > > handle 401 from tidal
-   > > abstract find & replace
-   > > highlight stuff we're asking for confirmation on
-   > > check for type errors, untyped stuff, warnings etc everywhere
-   > > numberTagFileConflicts: dedupe options
-   > > convert 24/92 FLAC to 16/44
-   > > backup ignorecache before running?
-   > > only rip missing tracks
-   > > define desired format, functions to transform Tidal data into desired format; also tag -> filename transform
-   > > "set" command to set arbitrary tag on track / album / artist
-   > > get rid of feat in suggestions from tidal (should be able to reuse code)
-   > > ignore all of issues that look like this
-   > > some sort of undo technology?
-   > > configurable replace patterns
-   > > better display for suggestions -> choice numbers
-   > > alternate line colors?
-   > > add remix artist to artist field (maybe?)
-   > > look for deluxe editions etc I don't want
-   > > trailing slashes on rootdir break everything

### V2:

-   rip only missing tracks for missing albums? how exactly...
-   fix force option - i think tagcache gets deleted AFTER it's loaded
-   Clean up output a little bit
-   Configuration
-   write README

### V3

-   Better output
-   clean up all the places where substitutions, padding, etc happen
-   check song length in track dupes?
-   don't run string compare on pairings that have been ignored??
-   Better naming scheme for commands
-   keyed arguments with defaults pls - ie. clean up the way stuff is passed around
-   fix messy type hinting everywhere
-   tests

### V4

-   flag minimum bitrate
-   plugin architecture
-   issue caching?
-   fix file stucture issues instead of just warning
-   "buildCache" function which just loads all the data we need into caches for faster searching etc
-   writing tags takes a long time - any way to queue that, so that the user can keep going?
-   debounce / queue pickle writing
-   repeating a lot of stuff between find and fix - maybe can speed this up
-   configure file separator for different OSes?
-   better in memory caching - database?
