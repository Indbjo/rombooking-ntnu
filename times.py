# The purpose of this file is to create a simple, and flexible way to configure the bookings.
import pandas as pd
from dateutil.parser import parse
from datetime import timedelta
from datetime import datetime

df = pd.DataFrame()
df['weekday'] = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
df['start_time'] = ['08:15', '13:00', '08:15', '13:00', '08:15','13:00', '08:15', '13:00', '10:00', '13:00']
df['duration'] = ['04:00', '04:00', '01:45', '04:00', '04:00', '04:00', '04:00', '04:00', '02:30', '04:00']
LIMIT = 8

ROOM_PRIORITY_BY_ID = ['360E3-107'] # find the ID of rooms from tp.uio.no/ntnu/rombestilling
SEAT_PRIORITY = {'360E3-107': [7, 3]} # ordered list of seat number priorities, if all seats in the list are taken, random will be selected.


def compute_end_and_booking_times(df):
    df['end_time'] = df.apply(lambda row: (parse(f'{row.values[1]}') + timedelta(hours=parse(f'{row.values[2]}').hour, minutes=parse(f'{row.values[2]}').minute)).strftime('%H:%M'), axis=1)
    #df['booking_weekday'], df['booking_time'] = determine_booking_weekday(df)


def determine_booking_weekday(df):
    length = len(df)
    weekdays = []
    times = []
    for index, row in df.iterrows():
        weekday_index = (index - LIMIT) % length
        booking_weekday = df['weekday'][weekday_index]
        booking_time = (parse(df['end_time'][weekday_index]) + timedelta(minutes=1)).strftime('%H:%M')
        weekdays.append(booking_weekday)
        times.append(booking_time)
    return weekdays, times


def initialize_booking_dates(df):
    now = datetime.now()
    length = len(df)
    next_booking_datetimes = []
    for i in range(length):
        weekday_index = (i - LIMIT) % length
        booking_weekday = df['weekday'][weekday_index]
        booking_time = (parse(df.loc[weekday_index, 'end_time']) + timedelta(minutes=1))
        next_booking_datetime = now + timedelta(days=now.weekday() + 1 + int(booking_weekday))
        next_booking_datetime = datetime(
            year=next_booking_datetime.year,
            month=next_booking_datetime.month,
            day=next_booking_datetime.day,
            hour=booking_time.hour,
            minute=booking_time.minute
        )
        next_booking_datetimes.append(next_booking_datetime.strftime("%Y-%m-%d %H:%M"))
    return next_booking_datetimes


def book(df, index):
    df.loc[index, 'next_booking_datetime'] = (parse(df.loc[index, 'next_booking_datetime']) + timedelta(days=7)).strftime('%Y-%m-%d %H:%M')




print(df)
compute_end_and_booking_times(df)
print(df)
print(len(df))

df['next_booking_datetime'] = initialize_booking_dates(df)
book(df, 0)
print(df)


