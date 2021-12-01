from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

notelist = ['20201130', '20191130']


def zettel(x):
    yr_ago = datetime.now() - relativedelta(years=x)
    yr_ago_count = 0
    for uuid in notelist:
        if uuid == yr_ago.strftime('%Y%m%d'):
            yr_ago_count += 1
    return [x, yr_ago_count, yr_ago.strftime('%Y%m%d')]


print(f'There was {zettel(1)[1]} notes {zettel(1)[0]} years ago.')
print(f'There was {zettel(2)[1]} notes {zettel(2)[0]} years ago.')
print(f'There was {zettel(3)[1]} notes {zettel(3)[0]} years ago.')
