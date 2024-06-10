import pathlib
import os, re, random
from collections import defaultdict
from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta


# import pyperclip

# path to zettelkasten

target_dir = pathlib.Path("/Users/will/Dropbox/zettelkasten/")

# Regex

date_pattern = re.compile(r"\d{8}")
link_pattern = re.compile(r"(?<!{UUID_sign})\[\[.*?\d{8}]]")

# Initialize a lot of counters

tbooks = 0
tblogs = 0
tpodcast = 0
tarticles = 0
tyoutube = 0
tproof = 0
ttwodo = 0
tvideo = 0
twords = 0
tlinks = 0
tzettel = 0
day0 = date(2018, 11, 14)
atom = ""
counter = 0

# Death Watch

birth = date(1956, 9, 26)
today = date.today()
eighty = date(2036, 9, 26)
covid = date(2020, 3, 14)
since = today - birth
until = eighty - today
quarintine = today - covid
percentSince = round(since.days / 29220 * 100, 1)
percentLeft = round(until.days / 29220 * 100, 1)
percentOfTotal = round(quarintine.days / 29220 * 100, 2)

# Get counts for various date parameters.

yesterday_count = 0
yesterday = date.today() - timedelta(1)
tencount = 0
tencountfiles = []
hundredcount = 0
one_week_ago_count = 0
one_week_ago = datetime.now() - relativedelta(weeks=1)
three_weeks_ago_count = 0
three_weeks_ago = datetime.now() - relativedelta(weeks=3)
six_months_ago_count = 0
six_months_ago = datetime.now() - relativedelta(months=6)
one_yr_ago_count = 0
one_yr_ago = datetime.now() - relativedelta(years=1)
two_yrs_ago_count = 0
two_yrs_ago = datetime.now() - relativedelta(years=2)
three_yrs_ago_count = 0
three_yrs_ago = datetime.now() - relativedelta(years=3)
four_yrs_ago_count = 0
four_yrs_ago = datetime.now() - relativedelta(years=4)
tengap = 10
hundredgap = 100

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

for uuid in sorted(files, reverse=True):

    for filename in files[uuid]:
        file_name = os.path.basename(filename).rsplit(".", 1)[0]

        # Yesterday

        if uuid == yesterday.strftime("%Y%m%d"):
            yesterday_count += 1

        # 10 day gap

        for i in range(tengap):
            targetdate = (date.today() - timedelta(+i)).strftime('%Y%m%d')
            if targetdate == uuid:
                tencountfiles.append(datetime.strptime(uuid, '%Y%m%d').strftime(
                    '%m/%d/%Y') + " :: [" + file_name.rsplit((uuid), 1)[0] + "](thearchive://match/" + file_name + ")")
                tencount += 1

        for i in range(tengap):
            targetdate = (date.today() - timedelta(+i)).strftime("%Y%m%d")
            if targetdate == uuid:
                with open(filename, "r") as fp:
                    atom = ""
                    for line in lines_that_contain("Subatomic: ", fp):
                        atom = "-" + line.split(":")[1]
                #   Archive format
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
                #   Original format
                #   tencountfiles.append(datetime.strptime(uuid, '%Y%m%d').strftime(
                #         '%m/%d/%Y') + " :: [" + file_name.rsplit((uuid), 1)[0] + "](thearchive://match/" + file_name + ") \n\t\t\t\t -" + atom)
                tencount += 1

        # 100 day gap

        for i in range(hundredgap):
            targetdate = (date.today() - timedelta(+i)).strftime("%Y%m%d")
            if targetdate == uuid:
                hundredcount += 1

        # 1 week gap

        if uuid == one_week_ago.strftime("%Y%m%d"):
            one_week_ago_count += 1




                
# Print and output

output1 = f""" 
**Zettelkasten Review**

{'–'*4}
[{yesterday_count} notes created on {yesterday.strftime('%Y%m%d')}](thearchive://match/›[[{yesterday.strftime('%Y%m%d')}) yesterday.
[{one_week_ago_count} notes created on {one_week_ago.strftime('%Y%m%d')}](thearchive://match/›[[{one_week_ago.strftime('%Y%m%d')}) one week ago.

"""
print(f'{output1}')
