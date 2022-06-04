# Stock Analysis App

## Description

- Retrieves stock positions for a Questrade clients account, webscrapes news related to these positions and 
provides recommendations for further analysis using machine learning.

## Features and Information

- Authenticates users and accesses data for their account using the Questrade REST api (https://www.questrade.com/api) and requests.
- Webscrapes news from Yahoo Finance (https://ca.finance.yahoo.com/) using Selenium and BeautifulSoup.
- Predicts the sentiment of an article (positive or negative) using a Naive Bayes machine learning algorithm (Code located in ./sentiment_analysis.ipynb).
    - I used datasets specific to the stock market as I thought this would provide a unique and applicable dataset to this problem. Due to this, the data
    was not of the highest quality, but sufficed for this personal project. I would love to use better data to help improve the algorithm.
    - The model was trained using the datasets in ./datasets (Contained about 10,500 entries after filtering): 
        - https://www.kaggle.com/datasets/sbhatti/financial-sentiment-analysis
        - https://www.kaggle.com/datasets/ankurzing/sentiment-analysis-for-financial-news
        - https://www.kaggle.com/datasets/yash612/stockmarket-sentiment-dataset
    - Model.pkl currently has the following scores:
        
        Recall:

        Positive:  0.828
        Negative:  0.757703081232493


        Precision:

        Positive:  0.8271728271728271
        Negative:  0.758765778401122


        F score:

        Positive:  0.8275862068965518
        Negative:  0.7582340574632095

# Requirements

- python3
- pip3
- The rest are located within the ./requirements.txt file.

# Instructions

- Clone the repository (git clone).
- Fill in the provided .env template file with the private information required.
    - QUESTRADE_APP_ID: Log in, click on your profile, access the "App Hub" and register the app under your 
    Questrade account (https://www.questrade.com/api/documentation/getting-started) and retrieve the APP_ID by clicking on the app.
    - QUESTRADE_ACCOUNT_ID: Log in, and view your account number under 'Account Management' and provide the prefix before "-".
- Install requirements.txt (pip3 install -r requirements.txt).
- Run (python3 ./src/main.py).
- Provide the application access to your Questrade account through the webbrowser that the application invokes.
- Check the terminal for your recommendations!

# Future Improvements

- Create more sophisticated algorithms selecting relevant articles, parsing valid text, etc.
- Automatic Questrade login.
- Improve machine learning model and potentially include neutral sentiment (data did not permit this with appropriate scores).
- Add more testcases and error handling.