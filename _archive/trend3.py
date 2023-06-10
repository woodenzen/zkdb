import os, pathlib
import fnmatch
from datetime import datetime, timedelta

# path to zettelkasten
zettelkasten = pathlib.Path("/Users/will/Dropbox/zettelkasten/")

def trend(length):
    """
    Returns the number of files in the zettelkasten directory that match a date pattern
    for the last n days, where n is the length parameter. This is uesd to calculate the trend.
        
    The date pattern is YYYYMMDD, and the files are markdown files.

    The function returns a tuple of the number of files that match the pattern and the length parameter.    
    """
    # calculate date range for the last ten days
    today = datetime.now()
    ten_days_ago = today - timedelta(days=length)
    date_range = [ten_days_ago + timedelta(days=x) for x in range(length)]

    # use fnmatch to filter the file names based on a pattern that matches the date string
    count = 0
    for root, dirs, files in os.walk(zettelkasten):
        for date in date_range:
            date_str = date.strftime("%Y%m%d")
            for file in fnmatch.filter(files, f"*{date_str}*.md"):
                count += 1
    return count, length

if __name__ == "__main__":

    # if the trend is zero, the number of files is the same
    # if the trend is positive, the number of files is increasing
    # if the trend is negative, the number of files is decreasing
    # the direction variable is used to indicate the direction of the trend

    direction = '⎯'
    if trend(10) > trend(10+1):
        direction = '⬆︎'
    elif trend(100) < trend(100+1) :
        direction = '⬇︎'

    # print the trend for the last 10 days and the last 100 days    

    print(f'{trend(10)[1]} day tend: {trend(10)[0]}/{trend(10+1)[0]} {direction}')
    print(f'{trend(100)[1]} day trend: {trend(100)[0]}/{trend(100+1)[0]} {direction}')

 