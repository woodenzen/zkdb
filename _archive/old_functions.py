
# years

from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

notelist = ['20211202', '20201221', '20201221', '20191203', '20181203']


def zettel(x):
    ''' Returns the number of zettel created on this day 'x' years ago.'''
    note_uuid = datetime.now() - relativedelta(years=x)
    note_count = 0
    for uuid in notelist:
        if uuid == note_uuid.strftime('%Y%m%d'):
            note_count += 1
    return [x, note_count, note_uuid.strftime('%Y%m%d')]


# print(f'There was {zettel(1)[1]} notes {zettel(1)[0]} years ago.')
# print(f'There was {zettel(2)[1]} notes {zettel(2)[0]} years ago.')
# print(f'There was {zettel(3)[1]} notes {zettel(3)[0]} years ago.')
print(f'[{zettel(1)[1]} notes created on {zettel(1)[2]}](thearchive://match/›[[{zettel(1)[2]}).')
print(f'[{zettel(2)[1]} notes created on {zettel(2)[2]}](thearchive://match/›[[{zettel(2)[2]}).')
print(f'[{zettel(3)[1]} notes created on {zettel(3)[2]}](thearchive://match/›[[{zettel(3)[2]}).')


# _______________

# days


from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

notelist = ['20211202', '20201203', '20191203', '20181203']


def zettel(x):
    ''' Returns the number of zettel created on this day 'x' years ago.'''
    note_uuid = datetime.now() - relativedelta(days=x)
    note_count = 0
    for uuid in notelist:
        if uuid == note_uuid.strftime('%Y%m%d'):
            note_count += 1
    return [x, note_count, note_uuid.strftime('%Y%m%d')]


print(f'[{zettel(1)[1]} new zettel yesterday :: [{zettel(1)[2]}](thearchive://match/›[[{zettel(1)[2]}).')
