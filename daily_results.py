import os
import fnmatch
from datetime import datetime as dt
from datetime import timedelta
from avg_per_day import calculate_avg_notes_per_day
from occurances_in_zk import count_target_occurrences
from get_word_count import get_word_count
from modified import count_modified_md_files

# Set the path to the directory to search for files
zettelkasten = "/Users/will/Dropbox/zettelkasten/"

def get_subatomic_line(file_name):
    blog = None  # Initialize the blog variable
    # Open the file
    with open(file_name, 'r') as file:
        # Loop through each line in the file
        for line in file:
            # Check if the line starts with "Subatomic: " or "description: "
            if line.startswith("Subatomic: ") or line.startswith("description: "):
                # If the line starts with "description: ", set blog to "post"
                if line.startswith("description: "):
                    blog = "post"
                # Split the line at the first colon and get the part after the colon
                result_line = line.split(':', 1)[1].strip()
                # If blog is "post", concatenate " Blog Post" to the result_line
                if blog == "post":
                    result_line += " ★Blog Post★"
                return result_line
    # If no matching line is found, return an empty string
    return ""

# Define a function to extract the date from the file name
def extract_date(file_name):
    # Extract the last 12 characters before the "."
    date_str = file_name.split('.')[0][-12:]
    # Convert the date and time string to a datetime object
    date = dt.strptime(date_str, "%Y%m%d%H%M")
    return date

def count_target_occurrences_in_file(file_name, target):
    count = 0
    with open(file_name, 'r') as file:
        for line in file:
            count += line.count(target)
    return count

def trend(length, compare_length):
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
    trend_length = today - timedelta(days=length)
    date_range = [trend_length + timedelta(days=x) for x in range(length+1)]

    # Calculate the length of the comparison trend and the comparison date range
    compare_trend_length = today - timedelta(days=compare_length)
    compare_date_range = [compare_trend_length + timedelta(days=x-length) for x in range(compare_length)]

    # Initialize counters for the number of files found
    count = 0
    compare_count = 0
    entry_list = []

    # Loop through all files in the directory
    for entry in os.scandir(zettelkasten):
        # Check if the entry is a file
        if entry.is_file():
            # Check if the file name ends with ".md"
            if entry.name.endswith('.md'):
                # Loop through the date range
                for date in date_range:
                    # Convert the date to a string in the format "YYYYMMDD"
                    date_str = date.strftime("%Y%m%d")
                    # Check if the file name contains the date string
                    if date_str in entry.name:
                        # Increment the counter for the number of files found
                        count += 1
                        # Append the file name to the list of files found
                        entry_list.append(entry.name)
                # Loop through the comparison date range
                for date in compare_date_range:
                    # Convert the date to a string in the format "YYYYMMDD"
                    date_str = date.strftime("%Y%m%d")
                    # Check if the file name contains the date string
                    if date_str in entry.name:
                        # Increment the counter for the number of files found for comparison
                        compare_count += 1

    # Reverse Sort the entry list by the date in the file name
    sorted_entry_list = sorted(entry_list, key=extract_date, reverse=True)

    # Determine the direction of the trend based on the number of files found
    direction = '⎯'  # Default direction if the number of files is the same
    if count > compare_count:
        direction = '⬆︎'  # Trend is up
    elif count < compare_count:
        direction = '⬇︎'  # Trend is down

    # Return a tuple containing the results
    return count, compare_count, length, direction, sorted_entry_list

if __name__ == "__main__":
    # Set the length and start of the current and comparison date ranges
    short = 10
    long = 100
    current = trend(short, short)
    past = trend(long, long)
    #####
    # Variables
    #####
    twords = get_word_count()
    tlinks = count_target_occurrences(']]')
    tzettel = 0
    
        ## Print the dashboard

    output = f"""
    {'–'*5}
## Zettelkasten Statistics
           ★★★★★ 
    {twords} Total word count
    {tlinks-len(os.listdir(zettelkasten))} Total link count
    {len(os.listdir(zettelkasten))} Total zettel count
           ★★★★★
    """
    print(f'{output}')
    
    print(f'{current[2]}-day trend: {current[0]}/{current[1]} {current[3]}')
    print(f'{past[2]}-day trend: {past[0]}/{past[1]} {past[3]}')
    print(f"{calculate_avg_notes_per_day(zettelkasten)} notes per day on average since day zero (20181114).")
    proofing_count = count_target_occurrences('#proofing')
    print(f"{proofing_count} notes wanting attention in my \#proofing_oven.")
    print(f'{current[0]} new notes in the last {short} days.')
    # print(f'{count_modified_md_files(zettelkasten)} notes modified in the last {short} days.\n')
 
    # Count occurrences of '#blog-post' in the files within the 'short' period
    blog_post_count = 0
    for entry in current[4]:
        blog_post_count += count_target_occurrences_in_file(zettelkasten + "/" + entry, '#blog-post')
    print(f"{blog_post_count} blog posts in the last {short} days for a total of {count_target_occurrences('#blog-post')} zettel as blog posts.")

    for entry in current[4]:
        subatomic_line = get_subatomic_line(zettelkasten + "/" + entry)
        # Check if subatomic_line has enough content
        if not subatomic_line or len(subatomic_line) < 12:
            print(f'- {entry[:-7]}')  # Print the filename without the last 7 characters
        else:
            print_line = '* ' + subatomic_line  # Slice subatomic_line from the 12th character onwards
            print(f'- {entry[:-7]}\n\t {print_line}')  # Print the filename and the processed subatomic_line