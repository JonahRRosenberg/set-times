from datetime import datetime
from dateutil import tz
import facebook

APP_ID = 339774799528645
APP_SECRET = "0993650e78e2f8a64f096963c601e77b"
FB_DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S+0000'
LIKE_THRESHOLD = 2000
MAX_USER_REQUEST = 50
MUSICIAN_CATEGORY = 'Musician/band'

class FBClient(object):
  def __init__(self):
    oauth_access_token = facebook.get_app_access_token(APP_ID, APP_SECRET)
    self.graph = facebook.GraphAPI(oauth_access_token)

  def find_user(self, name):
    pages = self.graph.request('search', args={'q': name, 'type': 'page'})
    ids = [x['id'] for x in pages['data'] if x['category'] == MUSICIAN_CATEGORY][:MAX_USER_REQUEST]
    if ids:
      users = self.graph.get_objects(ids)
      user = max(users.values(), key=lambda x: x['likes'])
      if int(user['likes']) > LIKE_THRESHOLD:
        return user
    return None

  def get_set_time_posts(self, username, date):
    set_time_posts = []

    user = self.graph.get_object(username)
    posts = self.graph.get_connections(user['id'], 'posts')
    for post in self._valid_posts(posts):
      if 'comments' in post:
        for comment in self._valid_posts(post['comments']):
          self._add_set_times(comment, date, user['id'], set_time_posts)
      self._add_set_times(post, date, user['id'], set_time_posts)
    return set_time_posts

  def _valid_posts(self, posts):
    return [x for x in posts['data']
             if 'message' in x
             and 'created_time' in x
             and 'from' in x
             and 'id' in x['from']
           ]

  def _is_set_time(self, message):
    message = message.lower()
    return (('set' in message and 'time' in message)
        or 'on at' in message)

  def _get_local_time(self, time):
    utc_time = datetime.strptime(time, FB_DATE_TIME_FORMAT).replace(
        tzinfo=tz.tzutc())
    return utc_time.astimezone(tz.tzlocal())

  def _add_set_times(self, post, date, user_id, set_time_posts):
    created_time = self._get_local_time(post['created_time'])
    if (post['from']['id'] == user_id and
        self._is_set_time(post['message'])# and
        #created_time.date() == date
        ):
      set_time_posts.append(post)

if __name__ == '__main__':
  fb = FBClient()

  #TEST searching
  pages = fb.graph.request('search', args={'q': 'dillon francis', 'type': 'page'})
  ids = [x['id'] for x in pages['data'] if x['category'] == MUSICIAN_CATEGORY][:MAX_USER_REQUEST]
  users = fb.graph.get_objects(ids)
  user = max(users.values(), key=lambda x: x['likes'])
  print user.keys()
  exit()

  #TEST Posts
  for post in fb.get_set_time_posts('iamtchami', None):
    print post['message']

