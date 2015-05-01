import re
from collections import defaultdict
from datetime import datetime
from datetime import date
from time import sleep

from constants import *
from event_client import EventClient
from fb_client import FBClient
from twitter_client import TwitterClient
from mail_client import MailClient

MESSAGE_POST = """
    We found a possible Set Time posting for your show:\n
    <br><br>
    {0}\n
    <br><br>
    From: {1}\n
    <br><br>
    Message: {2}\n
    <br><br>
    Link: {3}\n
    """
MAX_ARTIST_LEN = 45

TIMEOUT_IN_SECONDS = 30

MY_EMAIL = "JonahRRosenberg@gmail.com"

processed_posts = set()

def get_username(user):
  return user['username'] if 'username' in user else user['id']

def process_post(post, event_name):
  if post.id() not in processed_posts:
    message = MESSAGE_POST.format(
        event_name, post.name(), post.message(), post.link())
    try:
      MailClient().send(MY_EMAIL, event_name, message)
    except Exception as ex:
      print "Exception sending email:", ex
      return
    processed_posts.add(post.id())
  else:
    print "post already processed. id:", post.id()

def process_posts(set_time_posts, event_name):
  print "Found set times. count: {0} sets: {1}".format(
      len(set_time_posts), [x.message() for x in set_time_posts])
  for post in set_time_posts:
    process_post(post, event_name)

def process_event(event, today):
  print "Procesing event: {0} date: {1}".format(event.name(), event.start_time())

  for artist in event.artists():
    "Processing artist:", artist.name
    fb_user = artist.fb_user()
    if fb_user:
      print "Artist:", artist.name, "fb username:", get_username(fb_user)
      try:
        set_time_posts = FBClient().get_set_time_posts(fb_user['id'], today)
        if set_time_posts:
          process_posts(set_time_posts, event.name())
      except Exception as ex:
        print "Exception querying FB. fb_user: {0} ex: {1}".format(get_username(fb_user), ex)
    else:
      print "Unable to find fb_user. artist:", artist.name

    twitter_user = artist.twitter_user()
    if twitter_user:
      print "Artist:", artist.name, "twitter username:", twitter_user.screen_name
      try:
        set_time_posts = TwitterClient().get_set_time_posts(
            twitter_user.screen_name, today)
        if set_time_posts:
          process_posts(set_time_posts, event.name())
      except Exception as ex:
        print "Exception querying twitter. twitter_user: {0} ex: {1}".format(
            twitter_user.screen_name, ex)
    else:
      print "Unable to find twitter_user. artist:", artist.name

if __name__ == '__main__':
  try:
    while (True):
      print "==============================="
      local_time = datetime.now(CHICAGO_TZ)
      print "Local time:", local_time

      for event in EventClient().get_events():
        process_event(event, local_time.date())

      sleep(TIMEOUT_IN_SECONDS)
  except KeyboardInterrupt:
    pass


