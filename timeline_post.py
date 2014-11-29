from datetime import datetime

from constants import *
import utility

FB_DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S+0000'
TWEET_URL = "http://www.twitter.com/{0}/status/{1}"

def tweet_url(screen_name, status_id):
  return TWEET_URL.format(screen_name, status_id)

class FacebookTimelinePost(object):
  def __init__(self, post):
    self.post = post

  def id(self):
    return self.post['id']

  def user_id(self):
    return self.post['from']['id']

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
    utc_time = datetime.strptime(self.post['created_time'], FB_DATE_TIME_FORMAT)
    return utility.to_local_tz(utc_time)

  def __str__(self):
    return "Id: '{}' User Id: {} Name: '{}' Message: '{}' Link: '{}' Created Time: '{}'".format(
        self.id(), self.user_id(), self.name(), self.message(), self.link(), self.created_time())

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

  def __str__(self):
    return "Id: '{}' Name: '{}' Message: '{}' Link: '{}' Created Time: '{}'".format(
        self.id(), self.name(), self.message(), self.link(), self.created_time())
