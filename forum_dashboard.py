#!/usr/bin/env python3
# encoding: utf-8

import os
import pathlib
import re
from collections import defaultdict
from datetime import date, timedelta

# path to zettelkasten
target_dir = pathlib.Path("/Users/will/Dropbox/zettelkasten/")

# Regex
date_pattern = re.compile(r"\d{8}")
link_pattern = re.compile(r"(?<!{UUID_sign})\[\[.*?\d{8}]]")

# Functions
def lines_that_equal(line_to_match, fp):
    return [line for line in fp if line == line_to_match]


def lines_that_contain(string, fp):
    return [line for line in fp if string in line]


def lines_that_start_with(string, fp):
    return [line for line in fp if line.startswith(string)]


def lines_that_end_with(string, fp):
    return [line for line in fp if line.endswith(string)]


# Files is a dictionary mapping of a date to the list of files with that date
files = defaultdict(list)
for child in target_dir.iterdir():
    # Skip directories
    if child.is_dir():
        continue
    match = date_pattern.search(child.name)
    # Skip files that do not match the date pattern
    if match is None:
        continue
    file_date = match.group()
    files[file_date].append(child)
    
# Variables    
atom = ""
counter = 0
tencount = 0
tencountfiles = []
tengap = 7

for uuid in sorted(files, reverse=True):
    for filename in files[uuid]:
        file_name = os.path.basename(filename).rsplit(".", 1)[0]
        for i in range(tengap):
            targetdate = (date.today() - timedelta(+i)).strftime("%Y%m%d")
            if targetdate == uuid:
                with open(filename, "r") as fp:
                    atom = ""
                    for line in lines_that_contain("Subatomic: ", fp):
                        atom = line.split(":")[1]
                tencountfiles.append(     
                    file_name.rsplit((uuid), 1)[0]
                    +"\r"
                    +" -"
                    + atom
                    +"\r"
                )
                tencount += 1

output = f"""# What I'm Working On
## {tencount} New Zettel in the Last {tengap} Days.
Titles and one-sentence summary of atomic zettel. These are the ideas I'm currently wrestling with. They represent a {tengap}-day window of new notes.

This is generated with nothing held back. I would **love** to talk to you about anything on this list. If any of this is of interest to you, please start a thread here, [DM me](https://forum.zettelkasten.de/messages/add), or [get in touch via email](https://forum.zettelkasten.de/profile/Will).

{'-'*40}

"""

for newnotes in tencountfiles:
    output += newnotes 

print(f'{output}') 