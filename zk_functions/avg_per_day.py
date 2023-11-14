from datetime import date
import os

def calculate_avg_notes_per_day(zettelkasten):
    # Get the current date
    current_date = date.today()

    # Calculate the number of days since day0
    day0 = date(2018, 11, 14)
    days_since_day0 = (current_date - day0).days

    # Get the list of all notes in the directory
    notes = os.listdir(zettelkasten)

    # Calculate the total number of notes
    total_notes = len(notes)

    # Define a lambda function to calculate the average number of notes created per day
    avg_notes_per_day = lambda total_notes, days: round(total_notes / days, 2)

    # Apply the lambda function and return the result
    return avg_notes_per_day(total_notes, days_since_day0)