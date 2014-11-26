from utility import *

class TimelinePost(object):
  def __init__(self, post):
    self.post = post

  def id(self):
    return self.post['id']

  def name(self):
    return self.post['from']['name']

  def message(self):
    return clean_str(self.post['message'])

  def link(self):
    return (
        self.post['link']
        if 'link' in self.post
        else "Unknown Link")

  def created_time(self):
    raise RuntimeError("Not implemented yet")
