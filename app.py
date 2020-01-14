import tweepy
import markovify
import requests, json
# from time import sleep
from credentials import consumer_key, consumer_secret, access_token, access_token_secret

class TroikaBackgroundsBot:
  def __init__(self, backgrounds):
    self.generate_backgrounds(backgrounds)

    #initialize Twitter authorization with Tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    self.api = tweepy.API(auth)

  def generate_backgrounds(self, backgrounds):
    url = 'https://raw.githubusercontent.com/DavidSchirduan/davidschirduan.github.io/master/_pages/troika.json'
    response = json.loads(requests.get(url).text)

    with open('corpus.txt', 'w') as corpus:
      for i in response['Backgrounds']:
        background = i['Text']
        corpus.write(background + '\n')

    corpus.close()

    self.load_backgrounds(backgrounds)

  def load_backgrounds(self, backgrounds):
    with open("corpus.txt") as backgrounds_file:
      backgrounds_entries = backgrounds_file.read()
    self.model = markovify.Text(backgrounds_entries)

  def tweet(self):
    message = self.model.make_short_sentence(280)
    try:
      # self.api.update_status(message)
      print(message)
    except tweepy.TweepError as error:
      print(message)
      print(error.reason)

  def tweeter(self):
    self.tweet()

  # IF YOU WANT THIS SCRIPT TO BE A LONG RUNNING TASK UNCOMMENT AND RUN THIS INSTEAD OF TWEETER()
  # def automate(self, delay):
  #   while True:
  #     self.tweet()
  #     sleep(delay)

# def main():

if __name__ == "__main__":
  # main()
  troika = TroikaBackgroundsBot("corpus.txt")
  troika.tweeter()