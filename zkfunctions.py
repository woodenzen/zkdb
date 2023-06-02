
import os, re, random, pathlib
from datetime import datetime
from dateutil.relativedelta import relativedelta
from plistlib import load
from urllib.parse import urlparse


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
    return (path.path) 

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

import os, pathlib, re
from datetime import datetime
from datetime import timedelta

# path to zettelkasten
zettelkasten = pathlib.Path(TheArchivePath())

def trend(current, previous, length):
    """
    Count and compare the number of files modified during the current and previous time periods.

    Args:
        current (int): The number of days ago to start the current time period.
        previous (int): The number of days ago to start the previous time period.
        length (int): The length of the time period to count files for.

    Returns:
        A tuple containing the number of files modified during the current and previous time periods,
        and a trend indicator ('⎯' for no change, '⬆︎' for an increase, '⬇︎' for a decrease).
    """
    current_timestamp = datetime.now() - timedelta(days=current)
    previous_timestamp = datetime.now() - timedelta(days=(current + length))
    current_count = 0
    previous_count = 0
    for f in os.listdir(zettelkasten):
        if f.endswith('.md'):
            file_date_str = re.findall(r'\d{8}', f)[0]
            file_date = datetime.strptime(file_date_str, '%Y%m%d')
            if (current_timestamp - file_date).days <= (length):
                current_count += 1
            elif (previous_timestamp - file_date).days <= length and (current_timestamp - file_date).days > length:
                previous_count += 1
    trend = '⎯'
    if current_count > previous_count:
        trend = '⬆︎'
    elif current_count < previous_count :
        trend = '⬇︎'
    return current_count, previous_count, trend, length

if __name__ == "__main__":
    # print(trend(0, 11, 10))
    # print(trend(0, 101, 100))
    tenday_trend_result = trend(0, 11, 10)
    # tenday_previous_count = tenday_trend_result[1]
    hundredday_trend_result = trend(0, 101, 100)  
    # hundredday_count = hundredday_trend_result[0]  
    print(f'{tenday_trend_result[3]}-day trend: {tenday_trend_result[0]} {tenday_trend_result[1]} {tenday_trend_result[2]}')
    print(f'{hundredday_trend_result[3]}-day trend: {hundredday_trend_result[0]} {hundredday_trend_result[1]} {hundredday_trend_result[2]}')
    
    
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