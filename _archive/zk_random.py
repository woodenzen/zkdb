import os
import random
from TheArchivePath import TheArchivePath

zettelkasten = TheArchivePath()
shown_files = []

def print_random_files(directory, n):
    global shown_files
    # Get a list of all files in the directory
    files = os.listdir(directory)

    for _ in range(n):
        # If all files have been shown, reset shown_files
        if len(shown_files) == len(files):
            shown_files = []

        # Pick a random file from the files that haven't been shown yet
        file_to_show = random.choice([file for file in files if file not in shown_files])
        file_to_show = file_to_show.replace('.md', '')
        file_UUID = file_to_show[-12:]
        # Add the shown file to shown_files
        shown_files.append(file_to_show)

        # Print the name of the file
        print(f'[{file_to_show}](thearchive://match/›[[{file_UUID})')
if __name__ == "__main__":
    print_random_files(zettelkasten, 7)
