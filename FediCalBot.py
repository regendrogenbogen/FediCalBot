import requests
import icalendar
import datetime
import sys
from mastodon import Mastodon

try:
    mode = sys.argv[1]
except IndexError:
    print('Called without mode. Pass either soon or today as argument.')
    sys.exit(1)

if mode not in ('soon', 'today'):
    print('Called with wrong mode. Pass either soon or today as argument.')
    sys.exit(1)

def read_ical_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        ical_data = response.text
        calendar = icalendar.Calendar.from_ical(ical_data)
        return calendar
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

url = "https://metalab.at/calendar/export/ical/"
calendar = read_ical_from_url(url)
now = datetime.datetime.now()

mastodon = Mastodon(access_token = 'pytooter_usercred.secret')

if calendar:
    for event in calendar.walk("VEVENT"):
        summary = event.get("summary")
        start = event.get("dtstart").dt
        url = event.get("url")
        location = event.get("location")
        desc = event.get("description")
        if desc is None:
            desc = ""

        if start < now:
            continue
        time_to_event = start.date() - now.date()
        if time_to_event.days == 0 and mode == 'today':
            mastodon.status_post(f'Heute um {start.hour}:{start.minute:02d} im @metalab@chaos.social: {summary}\n{desc}\n\nMehr Informationen: {url}', visibility='unlisted')
        if time_to_event.days == 7 and mode == 'soon':
            mastodon.status_post(f'Am {start.date()} um {start.hour}:{start.minute:02d} im @metalab@chaos.social: {summary}\n{desc}\n\nMehr Informationen: {url}', visibility='unlisted')
