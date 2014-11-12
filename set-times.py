import re

from bs4 import BeautifulSoup
import urllib2

from fb_client import FBClient

EVENTS_URL = "http://www.clubtix.com/latest_events"

def html_request(url):
  html = urllib2.urlopen(url).read()
  return BeautifulSoup(html)

#TODO: Move to other file
class Artist(object):
  def __init__(self, name):
    self.name = name
    self.links = []

  def add_link(self, link):
    self.links.append(link)

def parse_b_artists(soup, artists):
  b = soup.find("b", text=re.compile(".*::.*::.*"))
  if b:
    artists_p = b.parent

    curArtist = None
    looking_for_links = False
    for child in artists_p.contents:
      if looking_for_links and curArtist and child.name == "a":
        curArtist.add_link(child.get('href'))
      else:
        if child.name == "b":
          artist_match = re.match(r".*::(.*)::.*", child.text)
          if artist_match:
            artist = artist_match.group(1).strip().lower()
            curArtist = Artist(artist)
            artists.append(curArtist)
        elif child == "[ ":
          looking_for_links = True
        elif child == " ]":
          looking_for_links = False
  
def parse_p_artists(soup, artists):
  #p = soup.find("p", text=re.compile(".*::.*"))
  p = soup.find_all("p", text=re.compile(r".*:.*"))
  print p
  #ps = soup.find_all("p")
  #for p in ps:
  #  t = re.match(r".*::.*", p.text)
  #  if t:
  #    print t.group(0)
  #  if '::' in p.text:
  #    print "=================="
  #    print
  #    print p.text
  #    print
  #    print "=================="

if __name__ == '__main__':
  #events_soup = html_request(EVENTS_URL)
  #urls = [x.get('href') for x in events_soup.find_all('a')]

  test_url = "http://www.clubtix.com/freaky-deaky-nervo-ktn-tchami-tickets-332007"
  #test_url = "http://www.clubtix.com/morgan-page-elle-morgan-chris-v-tickets-327445"
  test_soup = html_request(test_url)
  #urls = [x.get('href') for x in test_soup.find_all('a') if 'facebook' in x.get('href')]

  artists = []

  #parse_b_artists(test_soup, artists)
  parse_p_artists(test_soup, artists)
  #print [x.links for x in artists]

  #fb = FBClient()
  #fb.test()
