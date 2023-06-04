####
# Function for generating the first 8 numbers of a UUID based on the current date
####

from datetime import datetime
from dateutil.relativedelta import relativedelta

def UUID_date(years_ago=0):
    """Returns the first 8 numbers of a UUID based on the current date
    :param years_ago: number of years to subtract from the current date
    :return: first 8 numbers of a UUID based on the current date
    """
    return (datetime.now() - relativedelta(years=years_ago)).strftime('%Y%m%d')

if __name__ == '__main__':
    print(UUID_date(4))