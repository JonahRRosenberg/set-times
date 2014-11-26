import twitter

class Twitter(object):
  def get_posts(self):
    pass

if __name__ == "__main__":
  api = twitter.Api(
      consumer_key='cwqdnO7gN13OhiyABJ9wkiJ9L',
      consumer_secret='NV4WJuq1VcAm6u16XUIvHfF8qpFrYjTpxfjno37axxPbZgDkFA')
      #access_token_key='288108997-ODHTR4znfrfq2I3Ljruwg4CzGqGMYj9BpLdYMVUb',
      #access_token_secret='z7m3luv7UxQHEvhBehve67Px2LJNfVHBS0s3ZBVDukS3w')

  print api.VerifyCredentials()


