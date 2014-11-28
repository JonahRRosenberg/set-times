import re

from fb_client import FBClient
import utility

FB_REGEX = r".*facebook.com\/([\w,.]*)\/?"

class Artist(object):
  def __init__(self, name):
    self.name = utility.clean_str(name)
    self.links = []

  def add_link(self, link):
    self.links.append(link)

  def fb_username(self):
    try:
      user = FBClient().find_user(self.name)
      if (user):
        return user
    except Exception as ex:
      print "Exception finding user: {0} Ex: {1}".format(
          self.name, ex)
    return None

  def _fb_username_link(self):
    for link in self.links:
      if 'facebook.com' in link:
        find_username = re.match(FB_REGEX, link)
        if find_username:
          g = find_username.group(1)
          return g
    return None

