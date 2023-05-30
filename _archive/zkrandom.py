#! /usr/local/bin/python3

import os, re, random
from datetime import datetime
from dateutil.relativedelta import relativedelta
from zkfunctions import TheArchivePath

    
def zkrand():
    target_dir = TheArchivePath()
    counter = 0
    # Set counter to the number of notes wanted to be returned. 
    while counter < 4:
        # Create a variable "random+file" that contains a randomixed list of the files,
        random_file=random.choices(os.listdir(target_dir))
        # d = a year month day
        d = re.compile('.* (\d{8})')
        zkdate = d.match(str(random_file)).group(1)
        f = re.compile("\[['\"](.*\d{12})")
        zktitle = f.match(str(random_file)).group(1)
        #  Set "date" to a string now minus x years
        date = datetime.now() - relativedelta(years=1)
        date = date.strftime('%Y%m%d')
        # Compare current date (minus x years) with the file date and print if less than. And then update counter and do it all again,
        if date >= zkdate:
                UUID = zktitle[-12:]
                zettelname = zktitle[:-13]
                #  Print MMD formatted links
                print(f'[{zettelname}](thearchive://match/{zettelname} {UUID})')
                counter += 1
                    
if __name__ == "__main__":
    zkrand()