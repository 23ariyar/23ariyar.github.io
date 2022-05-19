import matplotlib.pyplot as plt
from TweetDatabase import get_database_data
import os

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


    file_name: file name for which to look for in every "day" directory
    return: a compilation of the data of the files. it will look something like
        [
        {"day": "5-18-2020", "positive": 41, "negative": 10, "neutral": 49}
        {"day": "5-19-2020", "positive": 10, "negative": 13, "neutral": 77}
        {"day": "5-20-2020", "positive": 1, "negative": 1, "neutral": 98}
    ]
    """
    file_name = file_name
    data = []
    tweet_directories = os.listdir(tweet_dir_path)  # gets list of directories in tweet_dir_path

    for directory in tweet_directories:  # iterates through each directory
        path_of_db = os.path.join(tweet_dir_path, directory, file_name)  # gets absolute path of each file name

        if not os.path.exists(path_of_db):
            print("No " + file_name + ".db file exists in " + path_of_db)
            print("Excluding date " + directory + " from result")

        else:  # if the file does exist in the "day" directory, add it to the data list
            directory_data = get_database_data(path_of_db)
            directory_data["day"] = repr(directory)  # add day information to the database dict
            data.insert(0, directory_data)

    return data


def plot_russia_ukraine_over_time():
    """
    Plots the percentage of Russia and Ukraine positive tweet percentage
    over time
    """
    ukraine_data = compile_data("ukraine.db")
    russia_data = compile_data("russia.db")

    russia_y_axis_values = []
    russia_x_axis_values = []
    for day in russia_data:  # gets russia data
        russia_x_axis_values.append(day["day"])
        russia_y_axis_values.append(day["positive"])

    ukraine_y_axis_values = []
    ukraine_x_axis_values = []
    for day in ukraine_data:  # gets ukraine data
        ukraine_x_axis_values.append(day["day"])
        ukraine_y_axis_values.append(day["positive"])


    #  creates plot
    plt.plot(russia_x_axis_values, russia_y_axis_values, label="Russia")
    plt.plot(ukraine_x_axis_values, ukraine_y_axis_values, label="Ukraine")
    plt.xlabel("Date")
    plt.ylabel("Percentage of Positive Sentiment Tweets")
    plt.legend()  # turns on plot legend
    plt.show()  # shows plot


if __name__ == "__main__":
    plot_russia_ukraine_over_time()
