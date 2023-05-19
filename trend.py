
import os, pathlib
from datetime import datetime
from datetime import timedelta

# path to zettelkasten
zettelkasten = pathlib.Path("/Users/will/Dropbox/zettelkasten/")

def trend(days_ago, num_days):
    count = 0
    target_date = datetime.now() - timedelta(days=days_ago)
    target_date_str = target_date.strftime('%Y%m%d')
    
    for i in range(num_days):
        date = target_date - timedelta(days=i)
        date_str = date.strftime('%Y%m%d')
        for f in os.listdir(zettelkasten):
            if date_str in f and f.endswith('.md'):
                count += 1
    return count, target_date_str, date_str 

if __name__ == "__main__":
    yesterday = 1
    two_days_ago = 2
    # ten = '⬇︎' if trend(yesterday, 11) <= trend(two_days_ago, 10) else '⬆︎'
    # hundred = '⬇︎' if trend(yesterday, 100) <= trend(two_days_ago, 100) else '⬆︎'
    ten = '⬆︎' if trend(11, 10) >= trend(10, 10) else '⬇︎'
    hundred = '⬆︎' if trend(101, 100) >= trend(100, 100) else '⬇︎'
    print(ten, trend(yesterday, 11), trend(two_days_ago, 10))
    print(hundred, trend(yesterday, 100), trend(two_days_ago, 100))
    