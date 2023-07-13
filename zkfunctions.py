
import os, re, random, pathlib
from datetime import datetime
from dateutil.relativedelta import relativedelta
from plistlib import load
from urllib.parse import urlparse, unquote


####
# Get folder size
####
def getFolderSize(folder):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder):#not sub folders
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)   
    return total_size
    
####
# Human readable single folder size
####

def sizeof_fmt(num, suffix='bytes'):
    for unit in ['',' Kilo',' Mega',' Giga',' Tera',' Peta',' Exa',' Zetta']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return

if __name__ == '__main__':
    print(sizeof_fmt(getFolderSize('/Users/will/Dropbox/zettelkasten')))
    print('-'*40) 

####
# Function for finding the path to The Archive
#####
def TheArchivePath():
    """
    Find the path to The Archive's plist file.

    Returns:
        A string representing the path to The Archive.
    """
    bundle_id = "de.zettelkasten.TheArchive"
    team_id = "FRMDA3XRGC"
    #`fileName` is the path to the plist file that contains the path to the ZK.
    fileName = os.path.expanduser(
        "~/Library/Group Containers/{0}.{1}.prefs/Library/Preferences/{0}.{1}.prefs.plist".format(team_id, bundle_id))
    with open(fileName, 'rb') as fp:
        # load is a special function for use with a plist
        pl = load(fp) 
        # 'archiveURL' is the key that pairs with the zk path
        path = urlparse(pl['archiveURL']) 
    # path is the part of the path that is formatted for use as a path.
        path = urlparse(pl['archiveURL']).path
        decoded_path = unquote(path) 
    return unquote(path) 
 

if __name__ == "__main__":
    zettelkasten = pathlib.Path(TheArchivePath())
    print(f'The Current ZK Directory. {zettelkasten}')
    print(f'## {len(os.listdir(zettelkasten))} notes in the archive.')   
    subfolders = [ f.path for f in os.scandir(zettelkasten) if f.is_dir() ]
    for i in subfolders:
        print(f'## {len(os.listdir(i))} files in {i}.')
        print(f'## {sizeof_fmt(getFolderSize(i))} in {i}.')
        print('-'*40) 


#####
# Function for finding a string in a line of a file
#####
def lines_that_contain(string, fp):
    """
    Find lines in a file that contain a given string.

    Args:
        string: A string to search for in the file.
        fp: A file object representing the file to search.

    Returns:
        A list of strings representing the lines in the file that contain the given string.
    """
    return [line for line in fp if string in line]
    
#####
# Function for getting a list of random files in the ZK 
#####
    
def zkrand(number):
    target_dir = TheArchivePath()
    counter = 0
    # Set counter to the number of notes wanted to be returned.
    print(f'## {number} random notes from the past.')
    while counter < number:
        # Create a variable "random+file" that contains a randomixed list of the files,
        random_file=random.choices(os.listdir(target_dir))
        # d = a year month day
        d = re.compile('.* (\d{8})')
        zkdate = d.match(str(random_file))[1]
        f = re.compile("\[['\"](.*\d{12})")
        year=zkdate[:4]
        zktitle = f.match(str(random_file))[1]
        #  Set "date" to a string now minus x years
        date = datetime.now() - relativedelta(years=0)
        date = date.strftime('%Y%m%d')
        # Compare current date (minus x years) with the file date and print if less than. And then update counter and do it all again,
        if date >= zkdate:
                UUID = zktitle[-12:]
                zettelname = zktitle[:-13]
                #  Print MMD formatted links
                print(f'{year} [{zettelname}](thearchive://match/{zettelname} {UUID})')
                counter += 1
                    
if __name__ == "__main__":
    print(zkrand(10))    

    
#####
# Function for determining if the ZK is growing or shrinking
##### 

# Import the required modules
import os
import fnmatch
from datetime import datetime as dt
from datetime import timedelta

# Set the path to the directory to search for files
zettelkasten = "/Users/will/Dropbox/zettelkasten/"

def trend(length, start, compare_start):
    """
    Counts the number of files in a given date range and compares it to the number of files in another date range.

    Args:
        length (int): The length of the current date range in days.
        start (int): The number of days ago to start counting from for the current date range.
        compare_start (int): The number of days ago to start counting from for the comparison date range.

    Returns:
        tuple: A tuple containing the following values:
            count (int): The number of files in the current date range.
            compare_count (int): The number of files in the comparison date range.
            length (int): The length of the current date range in days.
            direction (str): A string indicating the direction of the trend. Can be one of the following values:
                '⎯' (no change)
                '⬆︎' (increase)
                '⬇︎' (decrease)
    """

    # Get the current date
    today = dt.today()

    # Calculate the length of the trend and the date range
    trend_length = today - timedelta(days=start)
    date_range = [trend_length + timedelta(days=x) for x in range(length)]

    # Calculate the length of the comparison trend and the comparison date range
    compare_trend_length = today - timedelta(days=compare_start)
    compare_date_range = [compare_trend_length + timedelta(days=x) for x in range(length)]

    # Initialize counters for the number of files found
    count = 0
    compare_count = 0

    # Loop through all files in the directory and subdirectories
    for root, dirs, files in os.walk(zettelkasten):
        # Loop through the date range
        for date in date_range:
            # Skip dates that are before the trend length
            if date < trend_length:
                continue
            # Convert the date to a string in the format "YYYYMMDD"
            date_str = date.strftime("%Y%m%d")
            # Loop through all files that match the date string
            for file in fnmatch.filter(files, f"*{date_str}*.md"):
                # Extract the UUID from the file name
                UUID = file.split(' ')[-1].split('.')[0]
                # Increment the counter for the number of files found
                count += 1
        # Loop through the comparison date range
        for date in compare_date_range:
            # Skip dates that are before the comparison trend length
            if date < compare_trend_length:
                continue
            # Convert the date to a string in the format "YYYYMMDD"
            date_str = date.strftime("%Y%m%d")
            # Loop through all files that match the date string
            for file in fnmatch.filter(files, f"*{date_str}*.md"):
                # Extract the UUID from the file name
                UUID = file.split(' ')[-1].split('.')[0]
                # Increment the counter for the number of files found for comparison
                compare_count += 1

    # Determine the direction of the trend based on the number of files found
    direction = '⎯'  # Default direction if the number of files is the same
    if count > compare_count:
        direction = '⬆︎'  # Trend is up
    elif count < compare_count:
        direction = '⬇︎'  # Trend is down

    # Return a tuple containing the results
    return count, compare_count, length, direction

if __name__ == "__main__":
    # Set the length and start of the current and comparison date ranges
    short = 10
    long = 100
    current = trend(short, short+1, short+2)
    past = trend(long, long+1, long+2)

    # Print the results
    print(f'{current[2]}-day tend: {current[0]}/{current[1]} {current[3]}')
    print(f'{past[2]}-day trend: {past[0]}/{past[1]} {past[3]}')
 
    
#####
# Function for getting a list of random files in the ZK that are more than 1000 words
##### 
 
import os, re, random
from datetime import datetime
from dateutil.relativedelta import relativedelta

####
# Get a random file from the zettelkasten folder with more than 1000 words
####
   
def large_note_rand(minsize, maxsize, notenumber):
    target_dir = TheArchivePath()
    files = os.listdir(target_dir)
    files = [f for f in files if f.endswith('.md')]
    zettel=0
    print(f'## {notenumber} random notes for review & atomizing, between {minsize} and {maxsize} words.')    
    while zettel < notenumber:
        # open a random file
        random.shuffle(files)
        file_name, file_ext = os.path.splitext(os.path.basename(files[0]))
        d = re.compile('.* (\d{8})')
        zkdate = d.match(str(file_name))[1]
        year=zkdate[:4]
        with open(f'{target_dir}/{files[0]}', 'r') as file:
            data = file.read()
            words = data.split()
            if len(words) > minsize and len(words) < maxsize:
                zettel+=1   
                # print(f"{file_name} has {len(words)} words.")
                # add leading spaces
                # print(f'{len(words)} [{file_name}](thearchive://match/{file_name})')
                print(f'{year} {str(len(words)).ljust(4)} [{file_name}](thearchive://match/{file_name})')
        continue            
    return 

if __name__ == "__main__":
    large_note_rand(500, 1500, 10)
    
####
# Function that returns the time it takes to run a function
# Is used as a decorator
#####     
    
import os
import sys
from datetime import timedelta
from timeit import time

def stopwatch(method):
    def timed(*args, **kw):
        ts = time.perf_counter()
        result = method(*args, **kw)
        te = time.perf_counter()
        duration = timedelta(seconds=te - ts)
        print(f"{method.__name__}: {duration}")
        return result
    return timed

if __name__ == "__main__":
    @stopwatch
    def test():
        return sum(range(1000000))
    test()
    
####
# Regex search of file names in the ZK
####    

import os
import re
import glob
    
def filepaths_search(root_path: str, file_regex: str):
    return glob.glob(os.path.join(root_path, file_regex))

if __name__ == "__main__":
    print(filepaths_search(zettelkasten, "*20221218*.md"))

####
# Function for bookography progress
####    

import re
import datetime

def bookography(goal):
    """
    Calculates the progress towards a reading goal based on the number of books read compared to the years week number.

    Args:
        goal (int): The number of books to read in a year.
    
    Returns:
        tuple:
        - int: The highest book number read.
        - int: The current week of the year.
        - int: The goal for the year.
    
    Returns a tuple containing the highest book number read, the current week of the year, and the goal for the year.
    """
    # Variables
    # User needs to change this to the path of their Bookography file
    bookography = "/Users/will/Dropbox/zettelkasten/Bookography 2023 202301021454.md"
    current_date = datetime.date.today()
    current_week = current_date.isocalendar()[1]
    
    # Read the entire file
    with open(bookography, 'r') as file:
        content = file.read()
    # Search for ordered list items and extract numbers
    # regex pattern looks for lines that start with a number followed by a period
    pattern = r"^\s*\d+\."
    matches = re.findall(pattern, content, re.MULTILINE)
    # Convert matches to integers and remove the period
    numbers = [int(match.strip(".")) for match in matches]

    # Find the highest number
    if numbers:
        highest_number = max(numbers)
    else:
        highest_number = 0

    return highest_number, current_week, goal

if __name__ == "__main__":
    highest_number, current_week, goal = bookography(52)
    print(f"**I've read {highest_number} books so far this year.** \n**It is week {current_week} of my one-book-per-week challenge.**\n**My goal is to read {goal} books this year.**\n\n")

####
# Momento Mori
####     

from datetime import date, timedelta

def momento_mori():
    birth = date(1956, 9, 26)

    # Calculate the number of weeks between the birth date and today
    current = date.today()
    days = (current - birth).days
    weeks_since_birth = days / 7

    # Calculate the date for 80 years from now
    eighty_years_later = birth + timedelta(days=80*365.25)

    # Calculate the number of weeks between the birth date and 80 years later
    eighty_year_life = (eighty_years_later - birth).days / 7

    # Print the result
    print(f'## Momento Mori')
    print(f"Weeks since birth: {round(weeks_since_birth)} or {round(weeks_since_birth / eighty_year_life * 100, 1)}% of 80 years.")
    print(f'Weeks until 80: {round(eighty_year_life - weeks_since_birth)} or {round((eighty_year_life - weeks_since_birth) / round(eighty_year_life) *100, 2)}% of 80 years.')
    print(f'An 80-year life is {round(eighty_year_life)} weeks long.')
    print(f'I will be 80 on {eighty_years_later.strftime("%B/%d/%Y")}.')

if __name__ == "__main__":
    momento_mori()    