import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import os


# Code adapted from https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/

class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''

    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console

        keys_file = open("/Users/ariyaredddyy/Documents/Projects/sentiment-analysis/APIKeys.txt", "r")


        #Reads API keys from a separate file
        consumer_key = keys_file.readline().rstrip()
        consumer_secret = keys_file.readline().rstrip()
        access_token = keys_file.readline().rstrip()
        access_token_secret = keys_file.readline().rstrip()

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    @staticmethod
    def clean_tweet(tweet_text: str):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.

        :param  tweet_text: text of tweet to clean
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])", " ", tweet_text).split()).lower()

    @staticmethod
    def get_tweet_sentiment(tweet_text: str):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method

        :param tweet_text: text of tweet from which to determine sentiment

        :return "+" if the sentiment of the text is positive,
                "-" if the sentiment of the text is negative,
                "±" if the sentiment of the text is neutral
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(TwitterClient.clean_tweet(tweet_text))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return '+'
        elif analysis.sentiment.polarity == 0:
            return '-'
        else:
            return '±'

    def fetch_tweets(self, query, count=10):
        '''
        fetches unparsed tweets

        :param query: word for which to query for
        :param count: number of tweets to fetch, defaults to 10

        :return fetched tweets
        '''
        fetched_tweets = self.api.search_tweets(q=query, count=count)
        return fetched_tweets


if __name__ == "__main__":
    # calling main function
    os.system('cls' if os.name == 'nt' else 'clear')  # clears terminal screan
    print("TwitterClient has compiled without issues")
