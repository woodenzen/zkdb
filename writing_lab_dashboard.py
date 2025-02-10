import re
import os
import datetime
from datetime import date, timedelta

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
    bookography = "/Users/will/Dropbox/zettelkasten/Bookography 2025 202501010627.md"
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
    
    # Count lines starting with "*"
    abandoned = sum(1 for line in content.split("\n") if line.strip().startswith("*"))
    
    # Find the highest number
    if numbers:
        highest_number = max(numbers)
    else:
        highest_number = 0

    return highest_number, current_week, goal, abandoned

def writing(writing_goal):
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
    writeography = "/Users/will/Dropbox/zettelkasten/Writeography 2025 202501010931.md"
    current_date = datetime.date.today()
    current_week = current_date.isocalendar()[1]
    
    # Read the entire file
    with open(writeography, 'r') as file:
        content = file.read()
    # Search for ordered list items and extract numbers
    # regex pattern looks for lines that start with a number followed by a period
    pattern = r"^\s*\d+\."
    matches = re.findall(pattern, content, re.MULTILINE)
    # Convert matches to integers and remove the period
    numbers = [int(match.strip(".")) for match in matches]
    
    # Count lines starting with "*"
    writing_abandoned = sum(1 for line in content.split("\n") if line.strip().startswith("*"))
    
    # Find the highest number
    if numbers:
        writing_highest_number = max(numbers)
    else:
        writing_highest_number = 0

    return writing_highest_number, current_week, writing_goal, writing_abandoned

def journal(journal_goal):
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
    journalography = "/Users/will/Dropbox/zettelkasten/Journalography 202501270607.md"
    current_date = datetime.date.today()
    current_week = current_date.isocalendar()[1]
    
    # Read the entire file
    with open(journalography, 'r') as file:
        content = file.read()
    # Search for ordered list items and extract numbers
    # regex pattern looks for lines that start with a number followed by a period
    pattern = r"^\s*\d+\."
    matches = re.findall(pattern, content, re.MULTILINE)
    # Convert matches to integers and remove the period
    numbers = [int(match.strip(".")) for match in matches]
    
    # Count lines starting with "*"
    journal_abandoned = sum(1 for line in content.split("\n") if line.strip().startswith("*"))
    
    # Find the highest number
    if numbers:
        journal_highest_number = max(numbers)
    else:
        journal_highest_number = 0

    return journal_highest_number, current_week, journal_goal, journal_abandoned

def momento_mori():
    birth = date(1956, 9, 26)

    # Calculate the number of weeks between the birth date and today
    current = date.today()
    days = (current - birth).days
    weeks_since_birth = days / 7

    # Calculate the date for 80 years from now
    eighty_years_later = birth + timedelta(days=80*365.25)

    # Calculate the number of weeks between the birth date and 80 years later
    eighty_year_life = (eighty_years_later - birth).days

    spent_life = (eighty_years_later - birth).days

    return days, eighty_year_life, eighty_years_later

def count_target_in_file(file_path, target):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        # Read the entire file
        data = f.read()
        # Count the occurrences of the target in the file
        return data.count(target)

def count_target_occurrences(target):

    # Variables
    # User needs to change this to the path of their Bookography file
    zettelkasten = "/Users/will/Dropbox/zettelkasten/"
    
    total_count = 0
    for file_name in os.listdir(zettelkasten):
        file_path = os.path.join(zettelkasten, file_name)
        if os.path.isfile(file_path):
            total_count += count_target_in_file(file_path, target)
    return total_count

if __name__ == "__main__":
    zettelkasten = "/Users/will/Dropbox/zettelkasten/"
    highest_number, current_week, goal, abandoned = bookography(52)
    writing_highest_number, current_week, goal, writing_abandoned = writing(52)
    journal_highest_number, current_week, goal, journal_abandoned = journal(52)
    days, eighty_year_life, eighty_years_later = momento_mori()  # Call the function and store its return values
    proofing_count = count_target_occurrences('#proofing')
    zettel_count = count_target_occurrences('›[[')
    
    print()
    print(f"**I've read {highest_number} books this year. I'm on a pace to read {round(highest_number/current_week*52)} books.**") 
    print(f"**I've written {writing_highest_number} essays this year. I'm on a pace to write {round(writing_highest_number/current_week*52)} essays.**") 
    print(f"**I've read {journal_highest_number} journal articles this year. I'm on a pace to read {round(journal_highest_number/current_week*52)} journal articles.**") 
    print(f"**This is day {(days)} with {29220 - (days)} days until I'm 80 in 2036. I'm {round(days / eighty_year_life * 100, 1)}% done.**")
    print(f"**My proofing oven contains {proofing_count} notes out of {len(os.listdir(zettelkasten))} in total.**")


