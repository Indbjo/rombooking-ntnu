import roombooking
import times
from datetime import datetime
from dateutil.parser import parse


SCHEDULE = times.df
ROOM_PRIO = times.ROOM_PRIORITY_BY_ID
SEAT_PRIO = times.SEAT_PRIORITY


def time_to_book(schedule):
    for i in range(len(schedule)):
        now = datetime.now()
        weekday = int(schedule['booking_weekday'][i]) == now.weekday
        time = parse(schedule['booking_time'][i]) == now.strftime('%H:%M')
        date = now.date() == schedule['last_booked'][i]
        if weekday and time and not date:
            schedule['last_booked'] = now.date()
            return True, i
    return False, -1, ''


while True:
    book, index = time_to_book(SCHEDULE)
    if book:
        row = SCHEDULE.iloc[index]
        start_time = row['start_time']
        duration = row['duration']
        weekday = row['weekday']
        date =

