import eventful

from event import Event

APP_KEY = "ZWLRPpZNFbSRG7KS"
QUERY = 'tag:Music tag:Electronic'
LOCATION = 'Chicago'
DATE = 'Today'

class EventClient(object):
  api = eventful.API(APP_KEY)

  def get_events(self):
    events = []
    api_events = self.api.call('/events/search', q=QUERY, l=LOCATION, date=DATE)
    api_events = api_events['events']
    if api_events and 'event' in api_events:
      api_events = api_events['event']
      if isinstance(api_events, list):
        for event in api_events:
          self._add_event(event, events)
      else:
        self._add_event(api_events, events)
    return events

  def _add_event(self, event, events):
    e = Event(event)
    if e.artists():
      events.append(e)

if __name__ == '__main__':
  events =EventClient().get_events()
  for event in events:
    print "event:", event.name(), "artists:", [a.name for a in event.artists()]


