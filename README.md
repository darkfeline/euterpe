euterpe
=======

euterpe is a simple Python 3 program for syncing a music library to a music
player.

Dependencies
------------

- Python 3
- ffmpeg for transcoding songs

Installation
------------

    $ python setup.py install --user

This will install euterpe for your user.  You will need to add `~/.local/bin` to
your PATH to call euterpe.

Usage
-----

Here's an example of how you use euterpe.

Say you have a huge music library, which contains the following songs you want
to put on your portable music player:

    /home/bob/music/song1.flac
    /home/bob/music/song2.mp3
    /home/bob/music/song4.ogg
    /home/bob/music/song3.wav

Make a playlist file containing the songs:

    /home/bob/playlist.m3u
    ----------------------
    /song1.flac
    /song2.mp3
    /song4.ogg
    /song3.wav

Note the paths.  They start with slashes and they are relative to your music
library base directory.

Mount your music player somewhere like `/media/sdb1`.

Run euterpe.  You need to give it your music library's base directory, the
playlist file, and the destination path:

    $ euterpe /home/bob/music /home/bob/playlist.m3u /media/sdb1/music

This will copy all of the music supplied in the playlist from your music library
to the given destination, converting all of them to MP3 to save space,
replicating the directory structure, and escaping any FAT-unfriendly filename
characters.

You can choose between converting to MP3 or Vorbis using the flags `--mp3` and
`--vorbis`.  MP3 is default.

Bugs
----

The filename escaping for FAT is incomplete, since I could not find a
comprehensive list of bad characters so I can only add them as I run into them.
