import os
import pathlib
import sys
import re
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from TheArchivePath import TheArchivePath

zettelkasten = pathlib.Path(TheArchivePath())

import os
import re

def all_links(target):
    links = []
    target_file = None
    for note in os.listdir(zettelkasten):
        if target in note:
            target_file = os.path.join(zettelkasten, note)
            break

    if target_file is not None:
        # Process the target file
        with open(target_file, 'r') as f:
            for line in f:
                matches = re.findall(r'\b\d{12}\b', line)
                links.extend(matches)
    else:
        print(f"No file found with target '{target}'")
    return links

def append_to_test_md(links):
    with open('test.md', 'a') as test_md:
        for i, link in enumerate(links):
            for note in os.listdir(zettelkasten):
                if link in note:
                    with open(os.path.join(zettelkasten, note), 'r') as f:
                        if i != 0:  # Don't prepend separator to the first file
                            test_md.write('\n\n★★★★★\n\n')
                        test_md.write(f.read())

if __name__ == "__main__":
    # Empty the test.md file
    with open('test.md', 'w') as test_md:
        test_md.write('')
    
    links = all_links('202206100711')
    with open('test.md', 'a') as test_md:
        for link in links:
            append_to_test_md(links)