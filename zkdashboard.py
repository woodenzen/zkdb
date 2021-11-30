#!/usr/bin/env python3

import pathlib
import re
from collections import defaultdict
import os
from datetime import date, datetime, timedelta
import random
from dateutil.relativedelta import relativedelta
import pyperclip
from archive_path import TheArchive
import textwrap
from argparse import ArgumentParser, HelpFormatter


class RawFormatter(HelpFormatter):
    def _fill_text(self, text, width, indent):
        return "\n".join([textwrap.fill(line, width) for line in textwrap.indent(textwrap.dedent(text), indent).splitlines()])

# Function


def zettel(x):
    yr_ago_count = 0
    yr_ago = datetime.now() - relativedelta(years=x)
    if uuid == yr_ago.strftime('%Y%m%d'):
        yr_ago_count += 1
        return yr_ago_count, yr_ago.strftime('%Y%m%d')


program_descripton = f'''
     Zettelkasten Dashboard v1.0
     Created by Will Simpson on November 15, 2021 

     Puts stats and/or review links in clipboard for 
     pasteing in your journaling app of choice.

    USAGE:
    '''


parser = ArgumentParser(description=program_descripton,
                        formatter_class=RawFormatter)

# parser = argparse.ArgumentParser(description='Zettelkasten Dashboard Dashboard contents are copied to the clipboard\rfor pasting where ever you want.')
parser.add_argument('-s',
                    action='store_true', help='Just Basic Stats')
parser.add_argument('-a', action='store_true', help='Archive style links')
parser.add_argument('-m',
                    action='store_true', help='Markdown style links.')
args = parser.parse_args()

# Check for the presence of atleast one argument

# args = vars(parser.parse_args())
# if not any(args.values()):
#     parser.error('No arguments provided.')


# path to zettelkasten

target_dir = pathlib.Path(TheArchive.path())

# Regex

date_pattern = re.compile(r"\d{8}")
link_pattern = re.compile(r"(?<!{UUID_sign})\[\[.*?\d{8}]]")

# Initialize a lot of counters
# output = "zero"

twords = 0
tlinks = 0
tzettel = 0
yesterday_count = 0
tencount = 0
tencountfiles = []
a_tencountfiles = []
hundredcount = 0
one_yr_ago_count = 0
two_yrs_ago_count = 0
three_yrs_ago_count = 0
tengap = 10
hundredgap = 100
day0 = date(2018, 11, 14)
today = date.today()

# Iteration for counting tags, links (tlinks), wc (twords), total zettel (tzettel)

for filename in os.listdir(target_dir):
    if filename.endswith(".md"):
        file = open((os.path.join(target_dir, filename)), "r")
        data = file.read()
        links = data.count("]]")
        tlinks += links
        per_word = data.split()
        twords += len(per_word)
        tzettel += 1

        continue
    else:
        continue


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


# Output


if args.s == 1:

    s_output = f""" 
{'-'*40}

   {twords} Total word count
   {tlinks - tzettel} Total link count
   {tzettel} Total zettel count

{'-'*40}"""
    # print(s_output)
    pyperclip.copy(s_output)
###
#   Archive/wiki links

if args.a == 1:

    # Get counts for various date parameters.

    for uuid in sorted(files, reverse=True):

        for filename in files[uuid]:
            file_name = os.path.basename(filename).rsplit('.', 1)[0]

    # Yesterday

            yesterday = datetime.now() - relativedelta(days=1)
            if uuid == yesterday.strftime('%Y%m%d'):
                yesterday_count += 1

    # 10 day gap

            for i in range(tengap):
                targetdate = (date.today() - timedelta(+i)).strftime('%Y%m%d')
                if targetdate == uuid:
                    # tencountfiles.append(datetime.strptime(uuid, '%Y%m%d').strftime(
                    #     '%m/%d/%Y') + " :: [" + file_name.rsplit((uuid), 1)[0] + "](thearchive://match/" + file_name + ")")
                    a_tencountfiles.append(datetime.strptime(uuid, '%Y%m%d').strftime(
                        '%m/%d/%Y') + " :: [[" + file_name + "]]")
                    tencount += 1

    # 100 day gap

            for i in range(hundredgap):
                targetdate = (date.today() - timedelta(+i)).strftime('%Y%m%d')
                if targetdate == uuid:
                    hundredcount += 1

    # 1 year gap

            one_yr_ago = datetime.now() - relativedelta(years=1)
            if uuid == one_yr_ago.strftime('%Y%m%d'):
                one_yr_ago_count += 1

    # 2 year gap

            two_yrs_ago = datetime.now() - relativedelta(years=2)
            if uuid == two_yrs_ago.strftime('%Y%m%d'):
                two_yrs_ago_count += 1

    # 3 year gap

            three_yrs_ago = datetime.now() - relativedelta(years=3)
            if uuid == three_yrs_ago.strftime('%Y%m%d'):
                three_yrs_ago_count += 1

    a_output = f"""{'-'*40}

   {yesterday_count} new zettel yesterday :: [[{yesterday.strftime('%Y%m%d')}]].
   {one_yr_ago_count} notes created one year ago :: [[{one_yr_ago.strftime('%Y%m%d')}]].
   {two_yrs_ago_count} notes created two years ago :: [[{two_yrs_ago.strftime('%Y%m%d')}]].
   {three_yrs_ago_count} notes created three years ago :: [[{three_yrs_ago.strftime('%Y%m%d')}]].
   {tencount} new zettel in {tengap} days.
   {hundredcount} new zettel in {hundredgap} days.
   {tzettel / (today - day0).days:.1f} zettel created on average since day zero.

{'-'*40}

   # {tencount} Notes created in the last 10 days

"""

    for newnotes in a_tencountfiles:
        a_output += newnotes + '\n'
    # print(a_output)
    if args.s == 1 and args.a == 1:
        c_output = s_output + a_output
        pyperclip.copy(c_output)
    else:
        pyperclip.copy(a_output)

# markdown links

if args.m == 1:

     # Get counts for various date parameters.

    for uuid in sorted(files, reverse=True):

        for filename in files[uuid]:
            file_name = os.path.basename(filename).rsplit('.', 1)[0]

    # Yesterday

            yesterday = datetime.now() - relativedelta(days=1)
            if uuid == yesterday.strftime('%Y%m%d'):
                yesterday_count += 1

    # 10 day gap

            for i in range(tengap):
                targetdate = (date.today() - timedelta(+i)).strftime('%Y%m%d')
                if targetdate == uuid:
                    tencountfiles.append(datetime.strptime(uuid, '%Y%m%d').strftime(
                        '%m/%d/%Y') + " :: [" + file_name.rsplit((uuid), 1)[0] + "](thearchive://match/" + file_name.replace(' ', '%20') + ")")
                    # tencountfiles.append(datetime.strptime(uuid, '%Y%m%d').strftime(
                    #     '%m/%d/%Y') + " :: [[" + file_name + "]]")
                    tencount += 1

    # 100 day gap

            for i in range(hundredgap):
                targetdate = (date.today() - timedelta(+i)).strftime('%Y%m%d')
                if targetdate == uuid:
                    hundredcount += 1

    # 1 year gap

            one_yr_ago = datetime.now() - relativedelta(years=1)
            if uuid == one_yr_ago.strftime('%Y%m%d'):
                one_yr_ago_count += 1

    # 2 year gap

            two_yrs_ago = datetime.now() - relativedelta(years=2)
            if uuid == two_yrs_ago.strftime('%Y%m%d'):
                two_yrs_ago_count += 1

    # 3 year gap

            three_yrs_ago = datetime.now() - relativedelta(years=3)
            if uuid == three_yrs_ago.strftime('%Y%m%d'):
                three_yrs_ago_count += 1

    m_output = f""" 
{'-'*40}

  [{yesterday_count} new zettel yesterday.](thearchive://match/›[[{yesterday.strftime('%Y%m%d')}).
  [{one_yr_ago_count} notes created on {one_yr_ago.strftime('%Y%m%d')}](thearchive://match/›[[{one_yr_ago.strftime('%Y%m%d')}).
  [{two_yrs_ago_count} notes created on {two_yrs_ago.strftime('%Y%m%d')}](thearchive://match/›[[{two_yrs_ago.strftime('%Y%m%d')}).
  [{three_yrs_ago_count} notes created on {three_yrs_ago.strftime('%Y%m%d')}](thearchive://match/›[[{three_yrs_ago.strftime('%Y%m%d')}).
  {tencount} new zettel in {tengap} days.
  {hundredcount} new zettel in {hundredgap} days.
  {tzettel / (today - day0).days:.1f} zettel created on average since day zero.

{'-'*40}

    # {tencount} Notes created in the last 10 days

"""

    for newnotes in tencountfiles:
        m_output += newnotes + '\n'

    # print(m_output)
    # print(args)

    if args.s == 1 and args.m == 1:
        c_output = s_output + m_output
        pyperclip.copy(c_output)
    else:
        pyperclip.copy(m_output)
