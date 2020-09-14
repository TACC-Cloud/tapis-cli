import datetime
import time

__all__ = ['key_values']


def key_values():
    '''Return a dictonary of handy date and time values'''
    # Lifted from ansible/module_utils/facts/system/date_time.py
    date_time_facts = dict()

    now = datetime.datetime.now()
    date_time_facts['year'] = now.strftime('%Y')
    date_time_facts['month'] = now.strftime('%m')
    date_time_facts['weekday'] = now.strftime('%A')
    date_time_facts['weekday_number'] = now.strftime('%w')
    date_time_facts['weeknumber'] = now.strftime('%W')
    date_time_facts['day'] = now.strftime('%d')
    date_time_facts['hour'] = now.strftime('%H')
    date_time_facts['minute'] = now.strftime('%M')
    date_time_facts['second'] = now.strftime('%S')
    date_time_facts['epoch'] = str(int(time.time()))
    date_time_facts['date'] = now.strftime('%Y-%m-%d')
    date_time_facts['time'] = now.strftime('%H:%M:%S')
    date_time_facts['iso8601_micro'] = now.utcnow().strftime(
        "%Y-%m-%dT%H:%M:%S.%fZ")
    date_time_facts['iso8601'] = now.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    date_time_facts['iso8601_basic'] = now.strftime("%Y%m%dT%H%M%S%f")
    date_time_facts['iso8601_basic_short'] = now.strftime("%Y%m%dT%H%M%S")
    date_time_facts['tz'] = time.strftime("%Z")
    date_time_facts['tz_offset'] = time.strftime("%z")

    return {'date_time': date_time_facts}
