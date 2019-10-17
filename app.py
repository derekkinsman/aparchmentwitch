import tweepy
import markovify
from time import sleep
from credentials import consumer_key, consumer_secret, access_token, access_token_secret

class TroikaBackgroundsBot:
  def __init__(self, backgrounds):
    self.load_backgrounds(backgrounds)

    #initialize Twitter authorization with Tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    self.api = tweepy.API(auth)

  def load_backgrounds(self, backgrounds):
    with open("backgrounds.txt") as backgrounds_file:
      backgrounds_entries = backgrounds_file.read()
    self.model = markovify.Text(backgrounds_entries)

  def tweet(self):
    message = self.model.make_short_sentence(280)
    print(message)
    try:
      self.api.update_status(message)
    except tweepy.TweepError as error:
      print(error.reason)

  def automate(self, delay):
    while True:
      self.tweet()
      sleep(delay)

def main():
  troika = TroikaBackgroundsBot("backgrounds.txt")
  # Generate background text once a week
  troika.automate(604800)

if __name__ == "__main__":
  main()