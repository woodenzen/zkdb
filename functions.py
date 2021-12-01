from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

uuid = '20191130'


def zettel(x):
    yr_ago = datetime.now() - relativedelta(years=x)
    yr_ago_count = 0
    if uuid == yr_ago.strftime('%Y%m%d'):
        yr_ago_count += 1
    return [x, yr_ago_count, yr_ago.strftime('%Y%m%d')]


print(zettel(2))
print(f'There was {zettel(2)[1]} notes {zettel(2)[0]} years ago.')
print(uuid)

print(zettel(3))
print(f'There was {zettel(3)[1]} notes {zettel(3)[0]} years ago.')
print(uuid)


# Here, f() returns a list that can be indexed or sliced:

# def f():
#     return ['foo', 'bar', 'baz', 'qux']


# print(f())
# # ['foo', 'bar', 'baz', 'qux']
# print(f()[2])  # Return expressions called individually
# # 'baz'
# print(f()[::-1])
#['qux', 'baz', 'bar', 'foo']

# # Formatting strings, with multiple integer variables:
# stringVariable = 'I am {0} years old and I have {1} dollars in my pocket'
# age = 19
# cash = 65
# print(stringVariable.format(age, cash))
# Output: I am 19 years old and I have 65 dollars in my pocket
