import sqlite3
import os
from TwitterClient import TwitterClient


class TweetDB(object):
    """
    The TweetDB class is the base-point for creating SQLite databases in this module.
    Any methods involved in creating and inserting data into an SQLite database should
    most likely be added to this class
    """
    def __init__(self, filename: str):
        """
        Initializes a TweetDB object.

        :param filename: filename for which to create a database path.
                  can be absolute path or relative path
        """
        self.filename = filename
        self.conn = sqlite3.connect(filename)  # creates connection
        self.conn.execute("\n"
                          "        CREATE TABLE IF NOT EXISTS tweets (\n"
                          "          tweet_id integer UNIQUE,\n"
                          "          sentiment text,\n"
                          "          text text,\n"
                          "          created_at text,\n"
                          "          username text,\n"
                          "          favorite_count integer\n"
                          "          )")
        self.conn.commit()
        self.cur = self.conn.cursor()
        self.pending = 0  # Counter for when to commit
        self.column_names = 'tweetID, text, sentiment, created_at, username, favorite_count'

    def maybe_commit(self):
        """
        Each time a tweet is inserted, maybe_commit is called.
        The database will only fully commit every 100 tweets to improve time efficiency.
        """
        self.pending += 1
        if self.pending > 100:
            self.commit()

    def commit(self):
        """
        Called every 100 self.maybe_commits() and
        MUST be called at the end of the parsing in order
        to save data
        """
        self.conn.commit()
        self.pending = 0

    def insert(self, tweet):
        """
        Gets a tweet's id, text, sentiment, timestamp, username, and like count and
        inserts it into the database.
        :param tweet: Status object from tweepy
        """
        tweet_id = tweet.id
        text = TwitterClient.clean_tweet(tweet.text)
        sentiment = TwitterClient.get_tweet_sentiment(tweet.text)
        timestamp = str(tweet.created_at)
        username = tweet.user.screen_name
        favorite_count = tweet.favorite_count # like count

        self.conn.execute("""
                  INSERT or IGNORE INTO tweets VALUES (?, ?, ?, ?, ?, ?);
                """, [tweet_id, sentiment, text, timestamp, username, favorite_count])
        self.maybe_commit()

    def select_all(self, filename):
        """
        Returns all values in this sqlite database
        """
        return self.cur.execute('SELECT * FROM ' + filename + ' ORDER BY tweet_id')

    def __repr__(self):
        """
        Returns a string representation of this SQLite database object
        """
        return '<SQLite DB (' + self.filename + '): ' + ', '.join(self.column_names) + '>'


def get_database_data(absolute_file_path):
    """
    Given a SQLite database file, such as those created by
    TweetDatabase, will collect and return the percentages
    of positive, negative, and neutral tweets

    :param absolute_file_path: absolute file path of SQLite database
    :return: return the positive, negative, neutral percentages in a
             dictionary as such
            {
             "positive": 0
             "negative": 0
             "neutral": 0
            }
    """
    conn = sqlite3.connect(absolute_file_path)  # creates connection
    cursor = conn.cursor()  # gets cursor
    cursor.execute('SELECT * FROM tweets')

    positive_tweets = 0
    neutral_tweets = 0
    negative_tweets = 0
    for row in cursor:  # iterates over each row

        sentiment = row[1]  # gets sentiment
        if sentiment == "+":
            positive_tweets += 1

        elif sentiment == "-":
            negative_tweets += 1

        else:
            neutral_tweets += 1

    total = positive_tweets+neutral_tweets+negative_tweets  # total amount of tweets
    return {
        "positive": positive_tweets/total * 100,
        "neutral": neutral_tweets/total * 100,
        "negative": negative_tweets/total * 100
    }


if __name__ == "__main__":
    # calling main function
    os.system('cls' if os.name == 'nt' else 'clear')
    database = TweetDB("tweets")

    api = TwitterClient()  # creates twitter client
    fetched_tweets = api.fetch_tweets("War", 200)
    for tweet in fetched_tweets:
        database.insert(tweet)

    database.commit()
