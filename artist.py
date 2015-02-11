import re

from fb_client import FBClient
from twitter_client import TwitterClient
import utility

FB_REGEX = r".*facebook.com\/([\w,.]*)\/?"

class Artist(object):
  def __init__(self, name):
    self.name = utility.clean_str(name)

  def fb_user(self):
    return self._find_user(FBClient())

  def twitter_user(self):
    return self._find_user(TwitterClient())

  def _find_user(self, client):
    try:
      user = client.find_user(self.name)
      if (user):
        return user
    except Exception as ex:
      print "Exception finding user: {0} Client: {1} Ex: {2}".format(
          self.name, type(client), ex)
    return None

