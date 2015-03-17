import re
from collections import defaultdict
from datetime import datetime
from datetime import date
from time import sleep

from bs4 import BeautifulSoup
import urllib2

from artist import Artist
from constants import *
from fb_client import FBClient
from twitter_client import TwitterClient
from mail_client import MailClient

EVENTS_URL = "http://www.clubtix.com/latest_events"
EVENT_DATE_FORMAT = "%a, %b %d %Y"
CLUBTIX_REGEX = r".*:: (.*) ::(?!::).*"
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

TIMEOUT_IN_SECONDS = 15

MY_EMAIL = "JonahRRosenberg@gmail.com"

processed_posts = set()

def html_request(url):
  html = urllib2.urlopen(url).read()
  return BeautifulSoup(html)

def get_event_date(url):
  event_meta = url.find_next('p', class_='event_meta')
  event_date = event_meta.text.split('|')[0].strip()
  return datetime.strptime(event_date, EVENT_DATE_FORMAT).date()

def get_username(user):
  return user['username'] if 'username' in user else user['id']

def check_matches(text, artists):
  artist_match = re.match(CLUBTIX_REGEX, text)
  if artist_match:
    artist = artist_match.group(1).strip().lower()
    if len(artist) <= MAX_ARTIST_LEN:
      artists.append(Artist(artist))
    else:
      print "Ignoring artist, name is too long. artist:", \
          artist, "len:", len(artist)

def parse_artist_tag_matches(soup, artists):
  tags = soup.find_all(text=re.compile(CLUBTIX_REGEX))
  for tag in tags:
    check_matches(str(tag), artists)

def parse_artist_text_matches(soup, artists):
  artists_p = [p for p in soup.find_all("p") if re.match(CLUBTIX_REGEX, p.text) is not None]
  if len(artists_p) > 0:
    artists_p = artists_p[0]

    bs = artists_p.find_all("b")
    for b in bs:
      if (b.previous_sibling and
          b.next_sibling and
          "::" in b.previous_sibling and
          "::" in b.next_sibling):
        name = b.text.strip().lower()
        artist = Artist(name)
        artists.append(artist)

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
  print "found set times. count: {0} sets: {1}".format(
      len(set_time_posts), [x.message() for x in set_time_posts])
  for post in set_time_posts:
    process_post(post, event_name)

def process_event(event_date, url):
  print "Procesing event url: {0} date: {1}".format(url, event_date)
  soup = html_request(url)

  artists = []

  parse_artist_tag_matches(soup, artists)
  parse_artist_text_matches(soup, artists)

  for artist in artists:
    fb_user = artist.fb_user()
    if fb_user:
      print "artist:", artist.name, "fb username:", get_username(fb_user)
      try:
        set_time_posts = FBClient().get_set_time_posts(fb_user['id'], today)
        if set_time_posts:
          #TODO: url should be event name
          process_posts(set_time_posts, url)
      except Exception as ex:
        print "Exception querying FB. fb_user: {0} ex: {1}".format(get_username(fb_user), ex)
    else:
      print "Unable to find fb_user. artist:", artist.name

    twitter_user = artist.twitter_user()
    if twitter_user:
      print "artist:", artist.name, "twitter username:", twitter_user.screen_name
      try:
        set_time_posts = TwitterClient().get_set_time_posts(
            twitter_user.screen_name, today)
        if set_time_posts:
          process_posts(set_time_posts, url)
      except Exception as ex:
        print "Exception querying twitter. twitter_user: {0} ex: {1}".format(
            twitter_user.screen_name, ex)
    else:
      print "Unable to find twitter_user. artist:", artist.name

if __name__ == '__main__':
  #TODO: Timeout testing
  # Assign QuotaGuard to your environment's http_proxy variable
  #import os
  #print "url:", os.environ['QUOTAGUARDSTATIC_URL']
  #os.environ['http_proxy'] = os.environ['QUOTAGUARDSTATIC_URL']

  #events_soup = html_request(EVENTS_URL)
  #print events_soup

  #exit()


  try:
    events_by_date = defaultdict(set)

    while (True):
      print "==============================="
      local_time = datetime.now(CHICAGO_TZ)
      print "Local time:", local_time
      events_soup = html_request(EVENTS_URL)

      urls = events_soup.find_all('a', class_="eventNameLink")
      urls = [(x.get('href'), get_event_date(x)) for x in urls]

      today = local_time.date()

      for url, event_date in urls:
        events_by_date[event_date].add(url)

      for event_date, urls in events_by_date.iteritems():
        for url in urls:
          if event_date == today:
            process_event(event_date, url)

      sleep(TIMEOUT_IN_SECONDS)
  except KeyboardInterrupt:
    pass


