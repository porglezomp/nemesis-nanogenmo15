#!/usr/bin/python
from __future__ import division, print_function
import urllib2
import re
import os
import time

start = re.compile('\*\*\* START OF THIS PROJECT GUTENBERG .*? \*\*\*')
end = re.compile('\*\*\* END OF THIS PROJECT GUTENBERG .*? \*\*\*')
title = re.compile('Title: .*')

def ensure_isdir(dirname):
    if not os.path.exists(dirname):
        os.path.makedirs(dirname)
    elif not os.path.isdir(dirname):
        print("Error: `{}` exists but is not a directory".format(dirname))
        exit(1)

# Download books in the books list
RAW_BOOKS_DIR = 'raw-books'
ensure_isdir(RAW_BOOKS_DIR)
already_downloaded = os.listdir(RAW_BOOKS_DIR)
time_delay = False
did_download = False
with open('BOOKS', 'r') as f:
    for line in f:
        line = line.strip()
        # Skip empty lines and comments
        if not line or line[0] == '#':
            continue

        url = line
        rawname = url.split('/')[-1]
        if rawname not in already_downloaded:
            did_download = True
            if time_delay:
                print("Waiting 15 seconds to avoid rate limit problems...")
                time.sleep(15)

            print("Downloading `{}`...".format(rawname))
            book = urllib2.urlopen(url).read()
            path = os.path.join(RAW_BOOKS_DIR, rawname)
            with open(path, 'w') as out:
                print("Saved to `{}`.".format(path))
                out.write(book)
            time_delay = True
if did_download:
    print("\nDownloads complete.\n")
