from TweetDatabase import TweetDB
from TwitterClient import TwitterClient
from datetime import date
import os


class TweetScraper(object):
    def __init__(self, query_words):
        """
        Initializes this TweetScraper object
        :param query_words: list of words for this TweetScraper object to query twitter for
        """
        self.query_words = query_words
        self.client = TwitterClient()

        # path for which to insert daily tweet data
        self.tweet_dir_path = "/Users/ariyaredddyy/Documents/Projects/sentiment-analysis/tweets"
        self.today_date = str(date.today())

    def create_dir(self):
        """
        Creates a directory in tweet_dir_path named to today's date
        """
        parent_path = self.tweet_dir_path
        path = os.path.join(parent_path, self.today_date)  # path to make directory

        try:  # makes directory
            os.mkdir(path)

        except FileExistsError:
            print("Directory with date already exists.")
            print("Using existing directory (" + self.tweet_dir_path + "/" + self.today_date + ")")

    def query(self, query_word: str, count: int = 10000, to_filter: bool = False):
        """
        Queries for a specific word on twitter for "count" amount of tweets.
        Creates a SQLite database in tweet_dir_path/today_date/query_word for this word
        and includes data about sentiment, data, tweet id, username, and the tweet's content

        :param query_word: Word to query for
        :param count: Number of tweets to query for
        :param to_filter: determines whether to filter tweets depending. Filtering depends
                   self.filter_tweets
        """
        path = os.path.join(self.tweet_dir_path, self.today_date, query_word + ".db")  # creates db path
        db = TweetDB(path)
        fetched_tweets = self.client.fetch_tweets(query_word, count)  # fetches tweets

        if to_filter:
            fetched_tweets = TweetScraper.filter_tweets(fetched_tweets)

        for tweet in fetched_tweets:  # insert fetched tweets into the db
            db.insert(tweet)

        db.commit()

    @staticmethod
    def filter_tweets(fetched_tweets: list) -> list:
        """
        Filters list of tweets so that both russia AND ukraine may
        not be in in the tweet's text. For example, "Russia
        beats Ukraine" will be filtered out of the resultant list
        while "Russia wins!" or "Ukraine wins"! will be kept in.

        :param fetched_tweets: unparsed tweets for which to filter

        :return filtered list of tweets
        """
        filtered_tweets = []

        for tweet in fetched_tweets:  # parses fetched_tweets
            text = TwitterClient.clean_tweet(tweet.text)  # cleans each tweet
            if "russia" not in text or "ukraine" not in text:
                filtered_tweets.append(tweet)  # if passes filter, add it to filtered_tweets

        return filtered_tweets

    def query_words_on_twitter(self):
        """
        Queries self.query_words, as defined upon initialize, on Twitter,
        creating separate databases for each query word.

        Each database will be stored under a directory in self.tweet_dir_path.
        The directory will be named  based on the day of which the program is being run.
        """
        self.create_dir()  # creates a directory based on the date
        for word in self.query_words:  # queries each query word
            self.query(word)
            print("Finished Querying: " + word)

        print("Finished.")


def main():
    """
    Creates a TweetScraper object that scrapes based on tweets "ukraine" and "russia"
    """
    words = ["ukraine", "russia"]  # query words
    scraper = TweetScraper(words)
    scraper.query_words_on_twitter()


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    main()

