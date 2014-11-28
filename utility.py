
from constants import *

def clean_str(val):
  return val.encode('ascii', 'ignore')

def to_local_tz(utc_time):
  return utc_time.replace(tzinfo=tz.tzutc()).astimezone(CHICAGO_TZ)

