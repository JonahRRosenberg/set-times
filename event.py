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
    return self.event['start_time']

  def url(self):
    return self.event['url']

