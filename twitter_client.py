from datetime import datetime

import tweepy
from timeline_post import TwitterTimelinePost

CONSUMER_KEY = "LqH2u9PuRERmvVoJy8eHMglue"
CONSUMER_SECRET = "SyCMuIPlmiWyWWLIemFFbfRe09AD4SL0wShKhzi8HzSqDpxkth"
APP_ACCESS_KEY = "2895514637-URHlOdL0M52H8FBxgMPY3o3kQiJgOGjENiXBkb3"
APP_ACCESS_SECRET = "vi48ehUNTtKWUWIvgiBFHAuVCh3LBGGDTRChCWPwQn13b"

FOLLOWERS_THRESHOLD = 500

class TwitterClient(object):
  auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
  auth.set_access_token(APP_ACCESS_KEY, APP_ACCESS_SECRET)
  api = tweepy.API(auth)

  def find_user(self, name):
    users = self.api.search_users(q=name)
    user = max(users, key=lambda x: x.followers_count)
    return user if user.followers_count > FOLLOWERS_THRESHOLD else None

  def get_set_times_posts(self, screen_name, date):
    set_time_posts = []

    timeline = self.api.user_timeline(screen_name)
    for post in [TwitterTimelinePost(x) for x in timeline]:
      if (self._is_set_time(post) and
          post.created_time().date() == date):
        set_time_posts.append(post)

    return set_time_posts

  def _is_set_time(self, post):
    message = post.message().lower()
    return (('set' in message and 'time' in message)
        or 'on at' in message)

if __name__ == "__main__":
  user = TwitterClient().find_user("Mat Zo")

  today = datetime.now().date()

  set_time_posts = TwitterClient().get_set_times_posts(user.screen_name, today)
  print set_time_posts

