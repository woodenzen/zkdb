
import os

# Set the path to the directory to search for files
zettelkasten = "/Users/will/Dropbox/zettelkasten/"

def count_target_in_file(file_path, target):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        # Read the entire file
        data = f.read()
        # Count the occurrences of the target in the file
        return data.count(target)

def count_target_occurrences(target):
    total_count = 0
    for file_name in os.listdir(zettelkasten):
        file_path = os.path.join(zettelkasten, file_name)
        if os.path.isfile(file_path):
            total_count += count_target_in_file(file_path, target)
    return total_count

if __name__ == '__main__':
    print(count_target_occurrences('#proofing'))
    print(count_target_occurrences(']]'))