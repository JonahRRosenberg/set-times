from artist import Artist

class Event(object):
  def __init__(self, event):
    self.__event = event

  def name(self):
    return self.__event['title']

  def artists(self):
    return [Artist(x['name']) for x in self.__event['performers']['performer']]

