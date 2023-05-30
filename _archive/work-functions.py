from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import re   

def zettel():
    n = 0
    for filename in "/Users/will/Dropbox/zettelkasten/":
        if re.match("20230504", filename):
            n+=1
        return n    
if __name__ == "__main__":    
    print(zettel())   
    
####
# Function for getting a trend in ZK production.
    
import pickle

def trending(zpd):
    """ The trend of my zettel productivity is either upward or downward.
    """
    pickle_out = open("/Users/will/Dropbox/Projects/zettelkasten/zkdb/zk_trend.pickle","rb")
    old_trend=pickle.load(pickle_out)
    pickle_out.close()
    
    pickle_in = open("/Users/will/Dropbox/Projects/zettelkasten/zkdb/zk_trend.pickle","wb")
    pickle.dump(zpd,pickle_in)
    pickle_in.close()

    result = '⬆︎' if old_trend <= zpd else '⬇︎'
    return result

if __name__ == "__main__":
    
    # print(trending(2))   
    print(pickle.load(open("/Users/will/Dropbox/Projects/zettelkasten/zkdb/zk_trend.pickle","rb")))    
    
#####
# Function for extracting days ago from last modified date
##### 

import os
from datetime import datetime, timedelta

zettelkasten = "/Users/will/Dropbox/zettelkasten/"

def trend(days_ago):
    target_date = datetime.now() - timedelta(days=days_ago)
    target_date_str = target_date.strftime('%Y%m%d')
    return sum(
        target_date_str in filename for filename in os.listdir(zettelkasten)
    ) 

if __name__ == "__main__":
    result = '⬇︎' if trend(10) <= trend(1) else '⬆︎'
    print(result)


import os
from datetime import datetime, timedelta

zettelkasten = "/Users/will/Dropbox/zettelkasten/"

def trend(days_ago, num_days):
    count = 0
    target_date = datetime.now() - timedelta(days=days_ago)
    target_date_str = target_date.strftime('%Y%m%d')
    for i in range(num_days):
        date = target_date - timedelta(days=i)
        date_str = date.strftime('%Y%m%d')
        for filename in os.listdir(zettelkasten):
            if date_str in filename:
                count += 1
    return count 

if __name__ == "__main__":
    ten = '⬇︎' if trend(20, 10) <= trend(10, 10) else '⬆︎'
    print(ten)
    hundred = '⬇︎' if trend(200, 100) <= trend(100, 100) else '⬆︎'
    print(hundred)