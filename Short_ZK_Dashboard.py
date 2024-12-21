# Import the required modules
import os
import random
import datetime
from avg_per_day import calculate_avg_notes_per_day
from occurances_in_zk import count_target_occurrences
from TheArchivePath import TheArchivePath
import daily_results
from zk_stats import zk_stats
from get_word_count import get_word_count
from modified import count_modified_md_files

def main(short,long):
    # Set the path to the directory to search for files
    zettelkasten = TheArchivePath()

    #####
    # Variables
    #####
    twords = get_word_count()
    tlinks = count_target_occurrences(']]')
    tzettel = 0

    # Set the length and start of the current and comparison date ranges for trending
    # short = 10
    # long = 100

    # Functions


    ## Trending Function Call
    current = daily_results.trend(short, short)
    past = daily_results.trend(long, long)
    ## Basic stats Function Call
    zk_stats()

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


    # Print the trending results
    print(f'{current[2]}-day trend: {current[0]}/{current[1]} {current[3]}')
    print(f'{past[2]}-day trend: {past[0]}/{past[1]} {past[3]}')
    print(f"{calculate_avg_notes_per_day(zettelkasten)} notes/day since day zero (20181114).")
    # proofing_count = count_proofing_files(zettelkasten)
    print(f"{count_target_occurrences('#proofing')} zettels in my proofing oven.")
    print(f'{count_modified_md_files(short)} notes were modified in the past {short} days.')
    ## Print the list of files produced in the last 10 days and their subatomic lines.
    print('\n–––––')
    # print(f'## {current[0]} new notes in 10 days.')
    # print(f' {count_modified_md_files(10)} incrementally improved over the past ten days.')
    
    # Print the list of files produced in the last 10 days and their subatomic lines.
    for entry in current[4]:
        subatomic_line = daily_results.get_subatomic_line(zettelkasten + "/" + entry)
        if not subatomic_line or len(subatomic_line) < 12:  # Check if subatomic_line is empty or shorter than 12 characters
            print(f'- {entry[:-7]}\n')
            print_line = ''  # Initialize print_line to an empty string
        else:
            print_line = '* ' + subatomic_line  # Slice subatomic_line from the 12th character onwards

            print(f'- {entry[:-7]}\n\t {print_line}')

if __name__ == '__main__':
    # main(10,100)        
    main(int(os.environ["KMVAR_numberDays"]),100)   