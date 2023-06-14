# Import the required modules
import os
import fnmatch
from datetime import datetime as dt
from datetime import timedelta


# Set the path to the directory to search for files using the TheArchivePath() function
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
    short = 7
    long = 30
    current = trend(short, short+1, short+2)
    past = trend(long, long+1, long+2)

    # Print the results
    print(f'{current[2]}-day trend: {current[0]}/{current[1]} {current[3]}')
    print(f'{past[2]}-day trend: {past[0]}/{past[1]} {past[3]}')