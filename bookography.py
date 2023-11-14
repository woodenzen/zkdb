####
# Function for bookography progress
####    

import re
from datetime import datetime, date

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
    current_date = date.today()
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
