# The purpose of this file is to create a simple, and flexible way to configure the bookings.
import pandas as pd
from dateutil.parser import parse
from datetime import timedelta
from datetime import datetime


def load_schedule(filename='schedule.csv'):
    try:
        return pd.read_csv(filename)
    except FileNotFoundError as e:
        print(f'Could not find the file, initializing a new schedule\n'
              f'Error: {e}')
        return initialize_schedule(filename)


class Schedule:
    adjusted = False

    def __init__(self, filename):
        self.filename = filename
        self.schedule = set_schedule(filename)

    def set_schedule(self, filename):
        schedule = load_schedule(filename)

        if schedule['active_day'].any() and not self.adjusted:
            self.adjusted = True
            return adjust_schedule(schedule)
        return schedule

    def save(self):
        self.schedule.to_csv(self.filename)

    def book(self, weekday, booking_index):
        expected_booking_datetime = parse(self.schedule.loc[weekday, 'next_booking_datetime'][booking_index])
        if datetime.now() > expected_booking_datetime:
            self.schedule.loc[weekday, 'next_booking_datetime'][booking_index] = self.next_booking_datetime(weekday, booking_index)
            return True
        return False

    def next_booking_datetime(self, weekday, booking_index):
        now = datetime.now()

        return ''


def initialize_schedule(filename):
    data = {
        'weekday': [i for i in range(7)],
        'start_time': [],
        'duration': [],
        'end_time': [],
        'next_booking_datetime': [],
        'active_day': False,
    }
    schedule = pd.DataFrame(data).set_index('weekday')
    schedule.to_csv('schedule.csv')
    print(f'Initialized a new schedule with the filename {filename}, please enter the desired booking times.')
    return schedule


def adjust_schedule(schedule):
    compute_end_and_booking_times(schedule)
    return schedule


def set_schedule(filename='schedule.csv'):
    schedule = load_schedule(filename)

    if schedule['active_day'].any() and not schedule['adjusted'].all():
        return adjust_schedule(schedule)



df = pd.DataFrame()
df['weekday'] = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
df['start_time'] = ['08:15', '13:00', '08:15', '13:00', '08:15','13:00', '08:15', '13:00', '10:00', '13:00']
df['duration'] = ['04:00', '04:00', '01:45', '04:00', '04:00', '04:00', '04:00', '04:00', '02:30', '04:00']
LIMIT = 8

ROOM_PRIORITY_BY_ID = ['360E3-107'] # find the ID of rooms from tp.uio.no/ntnu/rombestilling
SEAT_PRIORITY = {'360E3-107': [7, 3]} # ordered list of seat number priorities, if all seats in the list are taken, random will be selected.


def compute_end_and_booking_times(df):
    df['end_time'] = df.apply(
        lambda row: (parse(f'{row.values[1]}') + timedelta(
            hours=parse(f'{row.values[2]}').hour,
            minutes=parse(f'{row.values[2]}').minute
        )).strftime('%H:%M'),
        axis=1
    )


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


compute_end_and_booking_times(df)

df['next_booking_datetime'] = initialize_booking_dates(df)
book(df, 0)
