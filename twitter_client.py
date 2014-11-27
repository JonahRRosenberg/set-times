import tweepy

CONSUMER_KEY = "LqH2u9PuRERmvVoJy8eHMglue"
CONSUMER_SECRET = "SyCMuIPlmiWyWWLIemFFbfRe09AD4SL0wShKhzi8HzSqDpxkth"

class Twitter(object):
  def get_posts(self):
    pass

if __name__ == "__main__":
  auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
  api = tweepy.API(auth)
  timeline = api.user_timeline('Axwell')
  print timeline

