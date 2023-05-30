
import os, pathlib, re
from datetime import datetime, date
from datetime import timedelta

# path to zettelkasten
zettelkasten = pathlib.Path("/Users/will/Dropbox/zettelkasten/")
timestamp_file = 'timestamp.txt'

def previous_run():
    timestamp = datetime.now()-timedelta(days=10)
    previous_timestamp_str=timestamp.strftime('%Y%m%d')
    # print(timestamp_str)
    with open(timestamp_file, 'r') as f:
        timestamp_str = f.read().strip()
        print(f'Current run: {timestamp_str}')
        print(f'Previous run: {previous_timestamp_str}')
        # print(timestamp_str)
    if timestamp_str:
        return previous_run, datetime.strptime(timestamp_str, '%Y%m%d'),  datetime.strptime(previous_timestamp_str, '%Y%m%d')   
    else:
        return None, None
    

def trend(days_ago, num_days, previous_days_ago):
    timestamp = datetime.now()
    timestamp_str = timestamp.strftime('%Y%m%d')
    with open(timestamp_file, 'r') as f:
        previous_run_str = f.read().strip()
        # f.seek(0)
        # f.write(timestamp_str)
    
    previous_timestamp = datetime.strptime(previous_run_str, '%Y%m%d')
    

    if previous_run is None:
        return 0, 0, '⎯'
    
    current_files = []
    previous_files = []
    for f in os.listdir(zettelkasten):
        if f.endswith('.md'):
            file_date_str = re.findall(r'\d{8}', f)[0]
            file_date = datetime.strptime(file_date_str, '%Y%m%d')
            if previous_timestamp <= file_date < timestamp:
                previous_files.append(f)
            elif timestamp_str <= file_date_str < previous_run:
                current_files.append(f)
    
    current_count = len(current_files)
    previous_count = len(previous_files)
    
    if current_count == previous_count:
        return current_count, previous_count, '⎯'
    elif current_count > previous_count:
        return current_count, previous_count, '⬆︎'
    else:
        return current_count, previous_count, '⬇︎'

if __name__ == "__main__":
    current_count, previous_count, trend_ten = trend(10, 10, 11)
    ten = '⎯' if trend_ten == '⎯' else ('⬆︎' if current_count > previous_count else '⬇︎')
    print(f'## {current_count} notes in the past 10 days. Trend = {ten}')
    print(f'## {previous_count} notes in the 10 days before that.')
    current_count, previous_count, trend_hundred = trend(100, 100, 101)
    hundred = '⎯' if trend_hundred == '⎯' else ('⬆︎' if current_count > previous_count else '⬇︎')
    print(f'## {current_count} notes in the past 100 days. Trend = {hundred}')
    print(f'## {previous_count} notes in the 100 days before that.')
    print(current_count)
    print(previous_count)
    previous_run()