import datetime
from calendar import monthrange

def iterate_metrics(df):
    metrics = ['AT', 'W', 'RH']
    means = {}
    for metric in metrics:
        means[metric] = df[metric].mean()
    return means

def format_climate(df, case_id, case_date, case_county):
    means = iterate_metrics(df)
    means['id'] = case_id
    means['date'] = case_date
    means['municipio'] = case_county
    return means

def format_date(date):
    date = str(date)
    if int(date) < 10 and len(date) != 2:
        return f"0{date}"
    else:
        return date

def max_date():
    today = datetime.date.today()
    if today.day < 10:
        day = f"0{today.day}"
    else:
        day = today.day
    return int(f"{today.year}{today.month}{day}")

def month_days(month, year=2020):
    month_num = int(month)
    month_range = monthrange(year, month_num)
    return month_range[1]
