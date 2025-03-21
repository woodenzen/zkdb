import os
import re

# Define the directory to search
zettelkasten = '/Users/will/Dropbox/zettelkasten'

# Define the search terms
search_term1 = "Question: "
search_term2 = "?" 
search_term3 = "interact" # Uncomment the following lines to use environment variables
# search_term2 = os.environ["KMVAR_searchTerm"]

# Compile the regular expression pattern
pattern1 = re.compile(rf'{re.escape(search_term1)}')
pattern2 = re.compile(rf'{re.escape(search_term2)}')
pattern3 = re.compile(rf'{re.escape(search_term3)}')

# List to store the matching file names
matching_files = []

# Walk through the directory
for root, dirs, files in os.walk(zettelkasten):
    for file in files:
        if file.endswith(".md"):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    if pattern1.search(line):
                        if pattern3.search(line):
                            matching_files.append(os.path.splitext(file)[0])
                            break  # Stop reading the file once a match is found
                    if pattern2.search(line):
                        if pattern3.search(line):
                            matching_files.append(os.path.splitext(file)[0])
                            break  # Stop reading the file once a match is found

# Extract the last 12 characters and format the output
output = " OR ".join(f"›[[{file[-12:]}]]" for file in matching_files)

# Print the formatted output
print(output)