
import os, pathlib, re
from datetime import datetime
from datetime import timedelta

# path to zettelkasten
zettelkasten = pathlib.Path("/Users/will/Dropbox/zettelkasten/")

def trend(current, previous, length):
    """
    Count and compare the number of files modified during the current and previous time periods.

    Args:
        current (int): The number of days ago to start the current time period.
        previous (int): The number of days ago to start the previous time period.
        length (int): The length of the time period to count files for.

    Returns:
        A tuple containing the number of files modified during the current and previous time periods,
        and a trend indicator ('⎯' for no change, '⬆︎' for an increase, '⬇︎' for a decrease).
    """
    current_timestamp = datetime.now() - timedelta(days=current)
    previous_timestamp = datetime.now() - timedelta(days=(current + length))
    current_count = 0
    previous_count = 0
    for f in os.listdir(zettelkasten):
        if f.endswith('.md'):
            file_date_str = re.findall(r'\d{8}', f)[0]
            file_date = datetime.strptime(file_date_str, '%Y%m%d')
            if (current_timestamp - file_date).days <= length:
                current_count += 1
            elif (previous_timestamp - file_date).days <= length and (current_timestamp - file_date).days > length:
                previous_count += 1
    trend = '⎯'
    if current_count > previous_count:
        trend = '⬆︎'
    elif current_count < previous_count :
        trend = '⬇︎'
    return current_count, previous_count, trend

if __name__ == "__main__":
    # print(trend(0, 11, 10))
    # print(trend(0, 101, 100))
    tenday_trend_result = trend(0, 1, 10)
    # tenday_previous_count = tenday_trend_result[1]
    hundredday_trend_result = trend(0, 1, 100)  
    # hundredday_count = hundredday_trend_result[0]  
    print(f'10-day trend: {tenday_trend_result[0]} {tenday_trend_result[1]} {tenday_trend_result[2]}')
    print(f'100-day trend: {hundredday_trend_result[0]} {hundredday_trend_result[1]} {hundredday_trend_result[2]}')