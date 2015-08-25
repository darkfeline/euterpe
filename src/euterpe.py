"""euterpe.py

Given a playlist file and a music directory tree:

    artist/album/songs.flac

Mirror all of the files in the playlist from the music directory to a target
directory, keeping the directory tree structure.  Also, convert all non-MP3
songs to MP3 (or other desired format).

"""

import argparse
import os
import subprocess


FORMATS = [
    ('--mp3', '.mp3', 'libmp3lame'),
    ('--vorbis', '.ogg', 'libvorbis'),
]


def convert(enc, src, dst):
    """Convert audio file src to target format."""
    subprocess.call(['ffmpeg', '-i', src, '-acodec', enc, dst])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source')
    parser.add_argument('playlist')
    parser.add_argument('dest')
    group = parser.add_mutually_exclusive_group()
    for flag, ext, enc in FORMATS:
        group.add_argument(flag, dest='format', action='store_const',
                           const=(ext, enc))
    args = parser.parse_args()
    if args.format is None:
        ext, enc = FORMATS[0][1:]
    else:
        ext, enc = args.format

    with open(args.playlist) as playlist:
        for path in playlist:
            # Copy the file.
            source = path.rstrip('\n').lstrip('/')
            source = os.path.join(args.source, source)
            dest = os.path.join(args.dest, path)
            if os.path.exists(dest):
                continue
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            os.link(source, dest)
            # Convert if necessary.
            if os.path.splitext(dest)[1].lower() != ext:
                new_dest = os.path.splitext(dest)[0] + ext
                convert(enc, dest, new_dest)
                os.unlink(dest)
