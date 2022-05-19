import unittest
from TweetDatabase import TweetDB


class TestTweetDB(unittest.TestCase):
    def test_insert(self):
        my_tweet_db = TweetDB("tweets")
        for i in range(10):
            my_tweet_db.insert(i)  # Need to update this to include all six values

        my_tweet_db.commit()

        count = 0

        for row in my_tweet_db.select_all():
            self.assertEqual(count, row[0])
            count += 1
        print("SUCCESS: TweetDB insert and select all")


if __name__ == "__main__":
    unittest.main()
