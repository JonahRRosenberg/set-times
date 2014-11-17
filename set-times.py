import re
from datetime import datetime
from datetime import date

from bs4 import BeautifulSoup
import urllib2

from artist import Artist
from fb_client import FBClient

EVENTS_URL = "http://www.clubtix.com/latest_events"
CLUBTIX_REGEX = r".*::(.*)::.*"

def html_request(url):
  html = urllib2.urlopen(url).read()
  return BeautifulSoup(html)

def get_username(user):
  return user['username'] if 'username' in user else user['id']

def parse_b_artists(soup, artists):
  b = soup.find("b", text=re.compile(CLUBTIX_REGEX))
  if b:
    artists_p = b.parent

    curArtist = None
    looking_for_links = False
    for child in artists_p.contents:
      if looking_for_links and curArtist and child.name == "a":
        curArtist.add_link(child.get('href'))
      else:
        if child.name == "b":
          artist_match = re.match(CLUBTIX_REGEX, child.text)
          if artist_match:
            artist = artist_match.group(1).strip().lower()
            curArtist = Artist(artist)
            artists.append(curArtist)
        elif child == "[ ":
          looking_for_links = True
        elif child == " ]":
          looking_for_links = False

def parse_p_artists(soup, artists):
  artists_p = [p for p in soup.find_all("p") if re.match(CLUBTIX_REGEX, p.text) is not None]
  if len(artists_p) > 0:
    artists_p = artists_p[0]
    looking_for_artists = False

    bs = artists_p.find_all("b")
    for b in bs:
      if (b.previous_sibling and
          b.next_sibling and
          "::" in b.previous_sibling and
          "::" in b.next_sibling):
        link = b.find_next("a")
        if link:
          name = b.text.strip().lower()
          artist = Artist(name)
          artist.add_link(link.get('href'))
          artists.append(artist)

if __name__ == '__main__':
  events_soup = html_request(EVENTS_URL)
  #pages = events_soup.find_all(class_="events_page")
  this_month = events_soup.find(text=re.compile(r"This Month"))
  if not this_month:
    raise RuntimeError("Could not find \"This Month\". Soup: " + str(events_soup))

  table = this_month.find_parent("table")

  urls = set([x.get('href') for x in table.find_all('a')])

  fb = FBClient()
  today = datetime.now().date()
  today = date(2014, 11, 1) #TODO: REMOVE

  for url in urls:
    print "=========================================="
    print "url:", url
    #url = "http://www.clubtix.com/freaky-deaky-nervo-ktn-tchami-tickets-332007"
    #url = "http://www.clubtix.com/morgan-page-elle-morgan-chris-v-tickets-327445"
    soup = html_request(url)

    artists = []

    parse_b_artists(soup, artists)
    parse_p_artists(soup, artists)

    for artist in artists:
      user = artist.fb_username(fb)

      if user:
        print "artist:", artist.name, "fb username:", get_username(user)
        try:
          set_time_posts = fb.get_set_time_posts(user['id'], today)
          if set_time_posts:
            print "found set times. count: {0} sets: {1}".format(
                len(set_time_posts), [x['message'] for x in set_time_posts])
        except Exception as ex:
          print "Unable to query fb. user: {0} ex: {1}".format(get_username(user), ex)
      else:
        print "Unable to find user. artist:", artist.name

