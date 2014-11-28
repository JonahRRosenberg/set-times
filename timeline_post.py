from constants import *
import utility

TWEET_URL = "http://www.twitter.com/{0}/status/{1}"

def tweet_url(screen_name, status_id):
  return TWEET_URL.format(screen_name, status_id)

class FacebookTimelinePost(object):
  def __init__(self, post):
    self.post = post

  def id(self):
    return self.post['id']

  def name(self):
    return self.post['from']['name']

  def message(self):
    return utility.clean_str(self.post['message'])

  def link(self):
    return (
        self.post['link']
        if 'link' in self.post
        else "Unknown Link")

  def created_time(self):
    raise RuntimeError("Not implemented yet")

class TwitterTimelinePost(object):
  def __init__(self, post):
    self.post = post

  def id(self):
    return self.post.id_str

  def name(self):
    return self.post.author.screen_name

  def message(self):
    return utility.clean_str(self.post.text)

  def link(self):
    return tweet_url(self.name(), self.id())

  def created_time(self):
    return utility.to_local_tz(self.post.created_at)
