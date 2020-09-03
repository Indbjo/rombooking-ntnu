import roombooking
import times
from datetime import datetime
from dateutil.parser import parse
from datetime import timedelta


SCHEDULE = times.df
ROOM_PRIO = times.ROOM_PRIORITY_BY_ID
SEAT_PRIO = times.SEAT_PRIORITY


def time_to_book(schedule):
    for i in range(len(schedule)):
        now = datetime.now().strftime('%Y-%m-%d %H:%M')
        next_booking_datetime = schedule.loc[i, 'next_booking_datetime']
        if now == next_booking_datetime:
            return True, i
    return False, -1


SCHEDULE.loc[0, 'next_booking_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M")

print(SCHEDULE)

while True:
    book, index = time_to_book(SCHEDULE)
    if book:
        row = SCHEDULE.iloc[index]
        start_time = row['start_time']
        duration = row['duration']
        weekday = row['weekday']
        current_datetime = parse(SCHEDULE.loc[index, 'next_booking_datetime'])
        booking_weekday = current_datetime.weekday()
        booking_day = current_datetime + timedelta(days=7 - int(abs(weekday - booking_weekday)), minutes=-1)
        last_booked_datetime = datetime(year=booking_day.year, month=booking_day.month, day=booking_day.day, hour=parse(start_time).hour, minute=parse(start_time).minute)
        date = last_booked_datetime.strftime("%d.%m.%Y")
        SCHEDULE.loc[index, 'last_booked_datetime'] = last_booked_datetime

        success = roombooking.book_room(start_time=start_time, duration=duration, date=date, area='Gløshaugen', building='Realfagbygget', roomtype='Lesesal', room=['360E3-107'], seat=[7])
        times.book(SCHEDULE, index) if success else None
        print(f"Booked room for {last_booked_datetime}") if success else print('something went wrong.')
        break

print(SCHEDULE)
