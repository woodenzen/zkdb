

import os, re, random
from datetime import datetime
from dateutil.relativedelta import relativedelta


 # Get a random file from the zettelkasten folder with more than 1000 words
   
def large_note_rand(minsize, maxsize, target):
    target_dir = "/Users/will/Dropbox/zettelkasten"
    files = os.listdir(target_dir)
    files = [f for f in files if f.endswith('.md')]
    zettel=0
    while zettel < target:
        # open a random file
        random.shuffle(files)
        file_name, file_ext = os.path.splitext(os.path.basename(files[0]))
        with open(f'{target_dir}/{files[0]}', 'r') as file:
            data = file.read()
            words = data.split()
            if len(words) > minsize and len(words) < maxsize:
                print(f"{file_name} has {len(words)} words.")
                zettel+=1
        continue            
        return print(f"{file_name} has {len(words)} words.")            
if __name__ == "__main__":
    large_note_rand(800, 1400, 6)