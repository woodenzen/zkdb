#!/usr/local/bin/python3.9
# encoding: utf-8

import pathlib
import os, re, random
from collections import defaultdict
from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from bear_rand import zkrand
from plistlib import load
from urllib.parse import urlparse

#####
# Function for finding the path to The Archive
#####
# Set the active archive path
def TheArchivePath():
#  Variables that ultimately revel The Archive's plist file.
    bundle_id = "de.zettelkasten.TheArchive"
    team_id = "FRMDA3XRGC"
    fileName = os.path.expanduser(
        "~/Library/Group Containers/{0}.{1}.prefs/Library/Preferences/{0}.{1}.prefs.plist".format(team_id, bundle_id))
    with open(fileName, 'rb') as fp:
        pl = load(fp) # load is a special function for use with a plist
        path = urlparse(pl['archiveURL']) # 'archiveURL' is the key that pairs with the zk path
    return (path.path) # path is the part of the path that is formatted for use as a path.

#####
# Variables
#####
# path to zettelkasten
target_dir = pathlib.Path(TheArchivePath())

# Regex
date_pattern = re.compile(r"\d{8}")
link_pattern = re.compile(r"(?<!{UUID_sign})\[\[.*?\d{8}]]")

# Initialize counters and variables
tzettel = 0
day0 = date(2018, 11, 14)
atom = ""
counter = 0
today = date.today()

#####
# Functions
#####
def lines_that_contain(string, fp):
    return [line for line in fp if string in line]


# Iteration for counting total zettel (tzettel)
for filename in os.listdir(target_dir):
    if filename.endswith(".md"):
        tzettel += 1


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

    # Get counts for various date parameters.
    tencount = 0
    tencountfiles = []
    hundredcount = 0
    tengap = 7
    hundredgap = 100

for uuid in sorted(files, reverse=True):
    for filename in files[uuid]:
        file_name = os.path.basename(filename).rsplit(".", 1)[0]
        for i in range(tengap):
            targetdate = (date.today() - timedelta(+i)).strftime("%Y%m%d")
            if targetdate == uuid:
                with open(filename, "r") as fp:
                    atom = ""
                    for line in lines_that_contain("Subatomic: ", fp):
                        atom = "-" + line.split(":")[1]
                #   Archive formatted links if the placement of the output is destined for The Archive
                        # tencountfiles.append(file_name.rsplit((uuid), 1)[0] + "[[" + full_uuid + "]]\n   -" + atom)
                #   Markdown format
                tencountfiles.append(
                    "- "
                    + file_name.rsplit((uuid), 1)[0]
                    + "["
                    + uuid
                    + "](thearchive://match/"
                    + file_name
                    + ")\n\t\t"
                    + atom
                )
                tencount += 1

        # 100 day gap
        for i in range(hundredgap):
            targetdate = (date.today() - timedelta(+i)).strftime("%Y%m%d")
            if targetdate == uuid:
                hundredcount += 1

# Output
zkrand()

output = f""" 
{'-'*40}
{tencount} new zettel in the last {tengap} days.
{hundredcount} new zettel in the last {hundredgap} days.
{tzettel / (today - day0).days:.2f} zettel created on average since day zero.
{'-'*40}

"""

for newnotes in tencountfiles:
    output += newnotes + "\r"

print(f'{output}') 