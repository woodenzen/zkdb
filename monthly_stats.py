import os
import prettytable as pt
from datetime import datetime, timedelta


'''
I've discovered that the date string could be in the last 6 digits of the UID, or in the first 6 digits of the UID.
I have to correct that in the script.
Consider switching to pandas instead of prettytable
'''

def count_files_zettelkasten(year_month_str):
    directory = "/Users/will/Dropbox/zettelkasten"
    count = 0
    for filename in os.listdir(directory):
        if year_month_str in filename:
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                count += 1
    return count

# Generate year and month strings for the past 5 years
today = datetime.today()
year_month_strs = []
for y in range(today.year-5, today.year+1):
    for m in range(1, 13):
        year_month_strs.append(f"{y}{m:02d}")

# Create a list of lists to store the counts for each year
counts_by_year = []
for i in range(6):
    year_counts = [count_files_zettelkasten(year_month_strs[j]) for j in range(i*12, (i+1)*12)]
    counts_by_year.append(year_counts)

# Convert month numbers to month names
month_names = [datetime(2000, i, 1).strftime('%b') for i in range(1, 13)]

# Create a table with the month names as the first column
table = pt.PrettyTable()
table.field_names = ['Month'] + [str(y) for y in range(today.year-5, today.year+1)]
for i in range(12):
    table.add_row([month_names[i]] + [str(counts_by_year[j][i]) for j in range(6)])

# Print the table
print(table)
# if __name__ == "__main__":
#     # count = count_files_zettelkasten("202305")
#     # print(count)

#     # today = datetime.today()
#     # year_month_str = today.strftime("%Y%m")
#     # count = count_files_zettelkasten(year_month_str)
#     # print(f"Number of files in {year_month_str}: {count}")

#     today = datetime.today()-timedelta(days=365)
#     for month in range(1, 13):
#         year_month_str = today.strftime(f"%Y{month:02d}")
#         count = count_files_zettelkasten(year_month_str)
#         print(f"Number of files in {year_month_str}: {count}")

# table = pt.PrettyTable()
# table.field_names = ["Monthly Stats 2023", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
# table.add_row(["Number of notes", "50", "49", "48", "40", "80", "16", "0", "0", "0", "0", "0", "0"])

# print(table)    