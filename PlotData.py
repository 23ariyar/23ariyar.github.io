import matplotlib.pyplot as plt
from TweetDatabase import get_database_data
import os
import glob

tweet_dir_path = "/Users/ariyaredddyy/Documents/Projects/sentiment-analysis/tweets"


def compile_data(file_name: str):
    """
    Goes through every single "day" directory in tweet_dir_path
    to get the file_name.

    For example, the tweet_dir_path will have the directories:

    5-18-2020,
    5-19-2020,
    5-20-2020,

    and compile data will look for the "file_name" file in each, which must be
    created as TweetDatabase is created. This function will return a compilation of
    the data in each file.


    :param file_name: file name for which to look for in every "day" directory
    :return a compilation of the data of the files. it will look something like
        [
        {"day": "5-18-2020", "positive": 41, "negative": 10, "neutral": 49}
        {"day": "5-19-2020", "positive": 10, "negative": 13, "neutral": 77}
        {"day": "5-20-2020", "positive": 1, "negative": 1, "neutral": 98}
    ]
    """
    file_name = file_name
    data = []

    # get all directories in tweet_dir_path
    tweet_directories = filter(os.path.isdir, glob.glob(tweet_dir_path + '/*'))

    # sort directories by date created
    tweet_directories = sorted(tweet_directories, key=os.path.getmtime, reverse=True)

    for directory in tweet_directories:  # iterates through each directory
        path_of_db = os.path.join(tweet_dir_path, directory, file_name)  # gets absolute path of each file name
        if not os.path.exists(path_of_db):
            print("No " + file_name + ". file exists in " + path_of_db)
            print("Excluding date " + directory + " from result")

        else:  # if the file does exist in the "day" directory, add it to the data list
            directory_data = get_database_data(path_of_db)
            directory_data["day"] = directory[-10:]  # add day information to the database dict
            data.insert(0, directory_data)

    return data


def plot_russia_ukraine_over_time(sentiment_to_plot_for="positive"):
    """
    Plots the percentage of Russia and Ukraine positive tweet percentage
    over time
    """
    if sentiment_to_plot_for not in ["positive", "negative", "neutral"]:
        raise TypeError('Only "positive", "negative", and "neutral" are valid arguments for '
                        'plot_russia_ukraine_over_time')
    ukraine_data = compile_data("ukraine.db")
    russia_data = compile_data("russia.db")

    russia_y_axis_values = []
    russia_x_axis_values = []
    for day in russia_data:  # gets russia data
        russia_x_axis_values.append(day["day"])
        russia_y_axis_values.append(day[sentiment_to_plot_for])

    ukraine_y_axis_values = []
    ukraine_x_axis_values = []
    for day in ukraine_data:  # gets ukraine data
        ukraine_x_axis_values.append(day["day"])
        ukraine_y_axis_values.append(day[sentiment_to_plot_for])

    #  creates plot
    plt.plot(russia_x_axis_values, russia_y_axis_values, label="Russia")
    plt.plot(ukraine_x_axis_values, ukraine_y_axis_values, label="Ukraine")
    plt.xlabel("Date")
    plt.ylabel("Percentage of " + sentiment_to_plot_for.capitalize()  + " Sentiment Tweets")
    plt.legend()  # turns on plot legend
    plt.show()  # shows plot


if __name__ == "__main__":
    plot_russia_ukraine_over_time()
