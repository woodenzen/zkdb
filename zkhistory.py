import re
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from TheArchivePath import TheArchivePath
from zk_random import print_random_files

zettelkasten = TheArchivePath()

def get_date_string(days_ago):
    """Return a string of the date for today - x number of days in the format %Y%m%d.
        Like 20210101 for today - 1 day. It is the compared to the regular expression in get_files_by_pattern() to match the date in the filename.

    Args:
        days_ago (int): The number of days ago.

    Returns:
        str: A string of the date for today - x numebr of days in the format %Y%m%d.
    """
    # get the date for today - x number of days
    date_x_days_ago = datetime.now() - timedelta(days=days_ago)
    # format the date as a string in the format %Y%m%d
    date_string = date_x_days_ago.strftime("%Y%m%d")
    # return the date string
    return date_string

def get_files_by_pattern():
    """Return a dictionary of the number of files for each unique pattern match the pattern in a directory.

    Returns:
        dict: A dictionary of the number of files for each unique pattern match the pattern in a directory.
    """
    # create a dictionary to store the results
    results = defaultdict(int)
    # create a regular expression object
    directory = Path(TheArchivePath())
    pattern = re.compile(r"20\d{6}")
    # iterate over the files in the ZK
    for file in Path(directory).iterdir():
        # if the file is a directory, skip it
        if file.is_dir():
            continue
        # if the file is not a directory, match the pattern.search
        match = pattern.search(file.name)
        # if there is a match, increment the count for that match
        if match:
            results[match.group()] += 1
    # return the results
    return results

if __name__ == "__main__":

    output_strings = {
    (1, 1, True): "[{files_count} note created on {date_string}](thearchive://match/›[[{date_string}) yesterday.",
    (1, False, True): "[{files_count} note created on {date_string}](thearchive://match/›[[{date_string}) yesterday.",
    (False, 1, True): "[{files_count} notes created on {date_string}](thearchive://match/›[[{date_string}) yesterday.",
    (False, False, True): "[{files_count} notes created on {date_string}](thearchive://match/›[[{date_string}) {years} years ago.",
    (1, 1, False): "[{files_count} note created on {date_string}](thearchive://match/›[[{date_string}) {days} days ago.",
    (1, False, False): "[{files_count} note created on {date_string}](thearchive://match/›[[{date_string}) {years} years ago.",
    (False, 1, False): "[{files_count} notes created on {date_string}](thearchive://match/›[[{date_string}) {days} days ago.",
    (False, False, False): "[{files_count} notes created on {date_string}](thearchive://match/›[[{date_string}) {years} years ago."
}

# iterate over the days for the review
for days in [1, 10, 100]: 
    # get the date string
    date_string = get_date_string(days)
    # get the number of files for the date string
    files_count = get_files_by_pattern()[date_string]
    # get the number of years
    years = int(days/365)
    # get the days string
    days_str = days if days < 365 else years
    # get the key for the output string
    key = (files_count == 1, days < 365, days == 1)
    # get the output string
    output_str = output_strings.get(key, output_strings[(False, False, False)]) # type: ignore
    # print the output string
    print(f"{output_str.format(files_count=files_count, date_string=date_string, days=days_str, years=years)}")  
print(f"## Random Note Review Schedule")
print_random_files(zettelkasten, 7)




