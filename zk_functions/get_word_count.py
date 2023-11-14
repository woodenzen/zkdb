import os
from TheArchivePath import TheArchivePath


def get_word_count():
    # Open the file
    directory = TheArchivePath()
    total_words = 0
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            with open(directory+"/"+filename, 'r') as file:
                # Read the file
                data = file.read()
                # Split the file into a list of words
                words = data.split()
                # Add the number of words in the file to the total
                total_words += len(words)
    # Return the total number of words in all the files
    return total_words

if __name__ == "__main__":
    print(get_word_count())
            