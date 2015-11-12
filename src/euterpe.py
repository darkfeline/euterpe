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
import shutil
import logging
import re


FORMATS = [
    ('--mp3', '.mp3', 'libmp3lame'),
    ('--vorbis', '.ogg', 'libvorbis'),
]


def convert(enc, src, dst):
    """Convert audio file src to target format."""
    subprocess.call(['ffmpeg', '-i', src, '-acodec', enc,
                     '-map_metadata', '0', dst])


def fat_escape(path):
    """Escape characters for FAT file system."""
    return re.sub(r'[*:;<>?"|]', '_', path)


def main():

    logging.basicConfig(level='INFO')

    # Set up argument parsing.
    parser = argparse.ArgumentParser()
    parser.add_argument('source')
    parser.add_argument('playlist')
    parser.add_argument('dest')
    group = parser.add_mutually_exclusive_group()
    for flag, ext, enc in FORMATS:
        group.add_argument(flag, dest='format', action='store_const',
                           const=(ext, enc))
    args = parser.parse_args()

    # Unpack desired file extension and encoder.
    if args.format is None:
        ext, enc = FORMATS[0][1:]
    else:
        ext, enc = args.format

    with open(args.playlist) as playlist:
        for path in playlist:
            path = path.rstrip('\n').lstrip('/')
            source = os.path.join(args.source, path)
            dest = os.path.join(args.dest, path)
            dest = fat_escape(dest)

            # If the source file is already in the right format, copy it over.
            if os.path.splitext(source)[1] == ext:
                if not os.path.exists(dest):
                    os.makedirs(os.path.dirname(dest), exist_ok=True)
                    logging.info('Copying %s to %s...', source, dest)
                    shutil.copyfile(source, dest)
                else:
                    logging.info('%s exists.', dest)
            # If the source file is not in the right format, convert it.
            else:
                dest = os.path.splitext(dest)[0] + ext
                if not os.path.exists(dest):
                    os.makedirs(os.path.dirname(dest), exist_ok=True)
                    logging.info('Converting %s to %s using %s...',
                                 source, dest, enc)
                    convert(enc, source, dest)
                else:
                    logging.info('%s exists.', dest)
