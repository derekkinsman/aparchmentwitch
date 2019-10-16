import tweepy
import markovify
from time import sleep
from credentials import consumer_key, consumer_secret, access_token, access_token_secret

class TroikaBackgroundsBot:
  def __init__(self, corpus):
    self.load_corpus(corpus)

    #initialize Twitter authorization with Tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    self.api = tweepy.API(auth)

  def load_corpus(self, corpus):
    with open("corpus.txt") as corpus_file:
      corpus_entires = corpus_file.read()
    self.model = markovify.Text(corpus_entires)

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
  troika = TroikaBackgroundsBot("corpus.txt")
  # Generate background text once a week
  troika.automate(604800)

if __name__ == "__main__":
  main()