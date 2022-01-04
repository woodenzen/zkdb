#!/usr/bin/env python3
# encoding: utf-8

import pathlib
import re
from collections import defaultdict
import os
# import pyperclip
from datetime import date
# from datetime import datetime
from datetime import timedelta
import random
from dateutil.relativedelta import relativedelta
import Foundation, AppKit

def lines_that_contain(string, fp):
    return [line for line in fp if string in line]

def pbcopy(s):
    "Copy string argument to clipboard"
    newStr = Foundation.NSString.stringWithString_(s).nsstring()
    newData = newStr.dataUsingEncoding_(Foundation.NSUTF8StringEncoding)
    board = AppKit.NSPasteboard.generalPasteboard()
    board.declareTypes_owner_([AppKit.NSStringPboardType], None)
    board.setData_forType_(newData, AppKit.NSStringPboardType)

def pbpaste():
    "Returns contents of clipboard"
    board = AppKit.NSPasteboard.generalPasteboard()
    content = board.stringForType_(AppKit.NSStringPboardType)
    return content

# path to zettelkasten

target_dir = pathlib.Path("/Users/will/Dropbox/zettelkasten/")

# Regex

date_pattern = re.compile(r"\d{8}")
uuid_pattern = re.compile(r"\d{12}")

# Initialize a lot of counters

# tencount = 0
zettel_list = []
gap = 15

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

for uuid in sorted(files, reverse=True):

    for filename in files[uuid]:
        file_name = os.path.basename(filename).rsplit('.', 1)[0]
        full_uuid = os.path.basename(file_name).rsplit(' ')[-1]

        for i in range(gap):
            targetdate = (date.today() - timedelta(+i)).strftime('%Y%m%d')
            if targetdate == uuid:
                with open(filename, "r") as fp:
                    for line in lines_that_contain("Subatomic: ", fp):
                        atom = line.split(":")[1]
                        zettel_list.append(file_name.rsplit((uuid), 1)[0] + "\n   -" + atom)                # tencount += 1                # tencount += 1                # tencount += 1                # tencount += 1                # tencount += 1# 100 day gap        # for i in range(hundredgap):        #     targetdate = (date.today() - timedelta(+i)).strftime('%Y%m%d')        #     if targetdate == uuid:        #         hundredcount += 1# 1 year gap       # one_yr_ago = datetime.now() - relativedelta(years=1)       # if uuid == one_yr_ago.strftime('%Y%m%d'):       #     one_yr_ago_count +=  2 year ga       # two_yrs_ago = datetime.now() - relativedelta(years=2)       # if uuid == two_yrs_ago.strftime('%Y%m%d'):       #     two_yrs_ago_count +=  3 year ga       # three_yrs_ago = datetime.now() - relativedelta(years=3)       # if uuid == three_yrs_ago.strftime('%Y%m%d'):       #     three_yrs_ago_count += 1

# Print and output

output = f""" 

Below are the titles and a one-sentence summary/meaning/'stinger' of zettel 
I've birthed into existence and their ideas I'm grappling with.
 
I would **love** to talk to you about anything on this list.
If any of this is of interest to you, please start a thread here, [DM me](https://forum.zettelkasten.de/messages/add), or [get in touch via email](https://forum.zettelkasten.de/profile/Will).

"""
ran_notes = (random.sample(zettel_list, 7))
for newnotes in ran_notes:
    output += newnotes

# print(output)
# print(type(output))
pbcopy(output)

