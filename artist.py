import re

FB_REGEX = r".*facebook.com\/([\w,.]*)\/?"

class Artist(object):
  def __init__(self, name):
    self.name = name
    self.links = []

  def add_link(self, link):
    self.links.append(link)

  def fb_username(self):
    for link in self.links:
      if 'facebook.com' in link:
        find_username = re.match(FB_REGEX, link)
        if find_username:
          g = find_username.group(1)
          return g
    return None

