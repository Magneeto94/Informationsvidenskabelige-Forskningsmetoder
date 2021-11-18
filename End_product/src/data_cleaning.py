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

import datetime
from datetime import datetime

#Adding spaCyTextBlob to spaCy pipline:
spacy_text_blob = SpacyTextBlob()
nlp.add_pipe(spacy_text_blob)


def main():


    #Saving the path to where the data is
    data_path = os.path.join("..", "data", "covidvaccine.csv")

    #reading data into a dataframe
    data = pd.read_csv(data_path)



    #Converting the text and date column to string type as some of them are in a float format.
    data = data.astype({"text": 'str', "date": 'str'})





    # Creating a container for the sentiment scores:
    output = []


    #The loop runs through the headlines in the csv-file.
    for doc in tqdm(nlp.pipe(data["text"], batch_size=200,
                       disable=["tagger", "parser", "ner"]), total = len(data)): #Disabeling to make the code run faster, since there is a lot of data and the processing time is long.
    
        output.append(doc._.sentiment.polarity) #appending the scores to our output container.



    # Creating a new dataframe
    sentiment_df = pd.DataFrame(data)

    # Appending a new series/column to the new df, with the scores
    sentiment_df["scores"] = output


    #Saving only the columns that is needed in the data set.
    sentiment_df = sentiment_df[["date", "text", "scores"]]



    #creating a container to hold formated time
    container = []

    #running through the date column
    for i in sentiment_df["date"]:
    
        #Appending a sliced time to the container
        container.append(i[:10])
    
    #over writing the date column with the values from the container.
    sentiment_df["date"] = container

    #Write new dataframe out, so it will not have to be processed again.
    sentiment_df.to_csv(os.path.join('..', 'data', 'sentiment_scores_twitter.csv'))

if __name__ =='__main__':
    main()