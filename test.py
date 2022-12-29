from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta



three_years_ago = datetime.now() - relativedelta(years=3)
print(three_years_ago.strftime('%Y%m%d'))