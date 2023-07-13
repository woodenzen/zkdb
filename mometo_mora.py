from datetime import date, timedelta

def momento_mori():
    birth = date(1956, 9, 26)

    # Calculate the number of weeks between the birth date and today
    current = date.today()
    days = (current - birth).days
    weeks_since_birth = days / 7

    # Calculate the date for 80 years from now
    eighty_years_later = birth + timedelta(days=80*365.25)

    # Calculate the number of weeks between the birth date and 80 years later
    eighty_year_life = (eighty_years_later - birth).days / 7

    # Print the result
    print(f"Weeks since birth: {round(weeks_since_birth)} or {round(weeks_since_birth / eighty_year_life * 100, 1)}% of 80 years.")
    print(f'Weeks until 80: {round(eighty_year_life - weeks_since_birth)} or {round((eighty_year_life - weeks_since_birth) / round(eighty_year_life) *100, 1)}% of 80 years.')
    print(f'An 80 year life is {round(eighty_year_life)} weeks long.')
    print(f'I will be 80 on {eighty_years_later.strftime("%m/%d/%Y")}.')

if __name__ == "__main__":
    momento_mori()    