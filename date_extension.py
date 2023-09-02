from datetime import date
from datetime import datetime

def days_since(start_date, event):
    today = date.today()
    start_date = datetime.strptime(start_date, '%m%d%Y').date()
    days_since = (today - start_date).days
    print(f"It has been {days_since} days since {event} on {start_date.strftime('%m/%d/%Y')}")

if __name__ == "__main__":
    days_since("08072023", "Right Eye Surgery")