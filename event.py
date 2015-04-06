from datetime import datetime

from artist import Artist

class Event(object):
  def __init__(self, event):
    self.event = event

  def name(self):
    return self.event['title'].encode('utf-8').strip()

  def artists(self):
    artists = []
    if self.event['performers'] and 'performer' in self.event['performers']:
      performers = self.event['performers']['performer']
      if isinstance(performers, list):
        artists.extend([Artist(x['name']) for x in performers])
      else:
        artists.append(Artist(performers['name']))
    return artists

  def start_time(self):
    return datetime.strptime(self.event['start_time'], "%Y-%m-%d %H:%M:%S")

  def url(self):
    return self.event['url']

