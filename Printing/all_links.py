import os
import pathlib
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from TheArchivePath import TheArchivePath
zettelkasten = pathlib.Path(TheArchivePath())
print(f'## {len(os.listdir(zettelkasten))} notes in the archive.')
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
            print(f"Reading file '{target_file}'")
            for line in f:
                if "[[" in line:
                    links.append(line)
                    links.append(line)
    else:
        print(f"No file found with target '{target}'")
    return links
        
print(all_links('202107251102'))