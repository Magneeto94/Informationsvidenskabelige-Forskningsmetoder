# Running the scripts

In order to run the scrip you will first have to set up a virtual inviorement (venv).
  - The venv can be set up by navigating in the terminal to the End_product folder and running the the bash script "create_venv_twitter_sentiment-sh" the following way:
    - bash create_venv_twitter_sentiment.sh
    - All packages that is needed to run the scripts will be installed from the file called requirements.txt, also placed in the End_product folder.
    - the bash script will also unzip a folder in the data-folder, that is needed to run the script.
  - When the venv has been set up you can now run the python scripts.
    - Via the terminal navigate to the src folder where you will find 2 python scripts:
      - data_cleaning.py
      - twitter_sentiment.py
    - run: "python data_cleaning.py" to create a dataset that is nessesary to run the next that creates the sentiment analysis.
    - now you can run "python twitter_sentiment.py
 - the graphs of that shows the dewellopment in the sentiment can be found in the output folder.
