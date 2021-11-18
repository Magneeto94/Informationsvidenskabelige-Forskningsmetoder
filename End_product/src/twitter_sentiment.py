#Loading packages:

import os
import sys
sys.path.append(os.path.join(".."))
from pathlib import Path #Importing Path that we are going to acces our files with.
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
#Initialise spacy
nlp = spacy.load("en_core_web_sm") #nlp = natural language processing.
import numpy as np
from tqdm import tqdm
from datetime import datetime

#Adding spaCyTextBlob to spaCy pipline:
spacy_text_blob = SpacyTextBlob()
nlp.add_pipe(spacy_text_blob)

import datetime
#Defining a function to guess how the dates should look.
def guess_date(string):
    
    #Running through the different formats
    for fmt in ["%Y-%m-%d", "%d-%m-%Y", "%Y%m%d"]:
        try:
            return datetime.datetime.strptime(string, fmt).date()
        except ValueError:
            continue
    raise ValueError(string)
    

#Defining plotting function to be used later in main function
def plot_figure(date, score, dataframe):
    # set figure size
    plt.figure( figsize = ( 20, 15))

    # plot a simple time series plot
    # using seaborn.lineplot()
    sns.lineplot(x = date,
                 y = score,
                 data = dataframe,
                 label = 'Sentiment score for'+score)


    plt.xlabel( 'Months of the year August 2020', fontsize=25)

    # setting labels for x axis
    pos = ['2020-08-01', '2020-09-01', '2020-10-01', '2020-11-01', '2020-12-01',
           '2021-01-01', '2021-02-01', '2021-03-01', '2021-04-01', '2021-05-01',
           '2021-06-01', '2021-07-01', '2021-08-01', '2021-09-01', '2021-10-01',
           '2021-11-01']

    # setting labels for x axis
    lab = [ 'Aug', 'Sept', 'Oct', 'Nov', 'Dec','Jan',
            'Feb', 'Mar', 'Apr', 'May', 'June', 'July',
            'Aug', 'Sept', 'Oct', 'Nov']

    #plotting
    plt.xticks(pos, lab)

    #plotting
    plt.ylabel('Sentiment Score', fontsize=25)

    plt.savefig(os.path.join("..", "output", score+".png"))
    
    
    


def main():
    
   #Saving the path to where the data is
    data_path = os.path.join("..", "data", "sentiment_scores_twitter.csv")

    #reading data into a dataframe
    sentiment_df = pd.read_csv(data_path) 
    
    #Dropping all nan's
    sentiment_df = sentiment_df.dropna()
    #resetting indexes
    sentiment_df = sentiment_df.reset_index(drop=True)
    
    
    #transforming the "date" column from float to string format, to be able to work with the column.
    sentiment_df = sentiment_df.astype({"date": 'str'})
    
    
    
    #Container to contain errors, that should be deleted later
    errors = []

    #Container to check what the errors are.
    indexes_to_be_dropped =[]

    #itterating through the length of sentiment_df.
    for i in range (len(sentiment_df)):

        current_date = sentiment_df["date"][i]

        #If values in this column does not contain "20", I will remove it from det date column.
        if "20" not in current_date:
            errors.append(current_date)
            indexes_to_be_dropped.append(i)

    print(f"Errors in the date columns: {errors}")
    print(f"The indexes they are ordered by: {indexes_to_be_dropped}")
    
    
    
    #Dropping the errors found above.
    sentiment_df = sentiment_df.drop(labels=indexes_to_be_dropped, axis=0).reset_index(drop=True)

    #Deleting column.
    sentiment_df = sentiment_df.drop('Unnamed: 0', 1)
    
    
    
    
    #container for new time
    new_time = []

    
    
    for time in sentiment_df["date"]:
        #changeing the data format for dates to stand in the same way.
        formated_time = guess_date(time)

        # appending the formated_time to the new_time
        new_time.append(formated_time.strftime("%Y%m%d"))

    #Overwriting date again with the new_time
    sentiment_df["date"] = new_time
    
    #creating a container for new date formats
    date_formats = []

    
    from datetime import datetime
    
    for date in sentiment_df["date"]:
        #Using the package datetime to transform dates from strings into date format.
        date_time_obj = datetime.strptime(date, '%Y%m%d')
        date_formats.append(date_time_obj)
        
        
    #over writing the date column with the new list
    sentiment_df["date"] = date_formats

    #creating the data frame avg_sentiment, grouped by date to make a rolling mean.
    avg_sentiment = sentiment_df.groupby("date").mean()
    
    #calculating rolling mean for weeks.
    avg_sentiment['week_rolling_avg'] = avg_sentiment.rolling(7).mean()
    #calculating rolling mean for months.
    avg_sentiment['month_rolling_avg'] = avg_sentiment['scores'].rolling(30).mean()
    
    
    #Calling plotfunction on the different scores.
    plot_figure('date','scores', avg_sentiment)
    plot_figure('date','week_rolling_avg', avg_sentiment)
    plot_figure('date','month_rolling_avg', avg_sentiment)
    
    
    
if __name__ =='__main__':
    main()