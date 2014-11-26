import base64

import twitter
import twitter_oauth

CONSUMER_KEY = "cwqdnO7gN13OhiyABJ9wkiJ9L"
CONSUMER_KEY = base64.b64encode(CONSUMER_KEY)
CONSUMER_SECRET = "NV4WJuq1VcAm6u16XUIvHfF8qpFrYjTpxfjno37axxPbZgDkFA"
CONSUMER_SECRET = base64.b64encode(CONSUMER_SECRET)

print CONSUMER_KEY
print CONSUMER_SECRET

class Twitter(object):
  def get_posts(self):
    pass

if __name__ == "__main__":
  get_oauth_obj = twitter_oauth.GetOauth(CONSUMER_KEY, CONSUMER_SECRET)
  print get_oauth_obj
  key_dict = get_oauth_obj.get_oauth()
  print key_dict
  exit()

  api = twitter.Api(
      consumer_key=CONSUMER_KEY,
      consumer_secret=CONSUMER_SECRET)
      #access_token_key='288108997-ODHTR4znfrfq2I3Ljruwg4CzGqGMYj9BpLdYMVUb',
      #access_token_secret='z7m3luv7UxQHEvhBehve67Px2LJNfVHBS0s3ZBVDukS3w')

  print api.VerifyCredentials()


