# Turnip

Turnip is an opinionated suite of tools for managing a collection of music files.
Turnip is not a music library.
Turnip currently supports MP3 and FLAC.
Turnip is _extremely_ rough, and probably borderline unusable currently.

## Usage

Turnip is made up of several commands, each of which do _one_ simple thing to the files in your music library, like ensuring that the filename and the title tag match up, or looking for possible duplicate tracks. It also has a "clean" command, which runs all the commands in sequence. You can either pick and choose which commands to run on your collection, or you can just run "clean" to do everything.

## Opinions

Soon, I'll add some writing here about the opinions Turnip enforces, why I think they're good, and how I'm considering making them more flexible/configurable in the future.

## Prior Art

Turnip is quite obviously inspired by _beets_, which is an incredible piece of software that didn't quite fit my needs. Beets is a music library with some tagging features, while Turnip is a set of tools for managing metadata and file organization of a bunch of music files.

## Roadmap

See TODO.md

## Questions

Q: Why Tidal instead of MusicBrainz / Spotify / Discogs, etc?
A: Because Tidal is what the account that I have, and it was quick to get working. I would like to add support for other metadata services in the future.

Q: Why only FLAC and MP3?
A: Because those are the files I have - again, I certainly plan to add support for more.

Q: Why does the code look so weird?
A: Basically, because I haven't writting Python or OOP in a while, so I just kinda made up some patterns for doing (Semi-)functional programming in Python.
