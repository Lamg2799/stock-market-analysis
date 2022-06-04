from selenium import webdriver
import questrade_api as api
import yahoo_finance_webscraper as scraper
import sentiment_analysis as analysis
from enum import Enum
import itertools
import threading
import time
import sys

done_scraping = False

class Sentiment(str, Enum):
    """
    Contains members which represent different sentiments from very positive to very negative.
    """
    good = 'This stock has good market sentiment currently.'
    average = 'This stock has mixed opinions about it currently.'
    great = 'This stock has been receiving great feedback from the market and has great news, there is no need to worry about this stock right now.'
    bad = 'The stock has had bad market sentiment recently, you should review your position when you get the chance.'
    terrible = 'The market sentiment is terrible for this stock recently, you should review this stock position closely ASAP.'

def print_sentiment_message(symbol, positive_sentiment_percentage):
    """
    Prints a message based on a symbols sentiment

    Args:
        symbol: stock symbol as a string.
        positive_sentiment_percentage: An integer between 0 and 100 representing the percentage of positive sentiment.
    """
    if positive_sentiment_percentage < 20:
        print(symbol, Sentiment.terrible.value)
    elif positive_sentiment_percentage < 40:
        print(symbol, Sentiment.bad.value)
    elif positive_sentiment_percentage < 60:
        print(symbol, Sentiment.average.value)
    elif positive_sentiment_percentage < 80:
        print(symbol, Sentiment.good.value)
    else:
        print(symbol, Sentiment.great.value)

def animate_scraping():
    """
    Prints an animation to show that execution is continuing while webscraping occurs (as it may take a while).
    """
    global done_scraping
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done_scraping:
            break
        sys.stdout.write('\rWebscraping news data ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone webscraping.     ')


def main():
    """
    Provides recommendations for further analysis of stocks based on market sentiment.
    """
    driver = webdriver.Firefox()
    position_names = api.get_account_position_names(driver)
    print('\nRetrieved Questrade positions\n')

    # Animation while webscraping occurs
    t = threading.Thread(target=animate_scraping, daemon=True)
    t.start()
    stock_news_dict = scraper.parse_stock_news(driver, position_names)
    driver.close()
    global done_scraping
    done_scraping = True
    print('Market sentiment for positions in your Questrade account:\n')
    for stock in stock_news_dict:
        predictions = analysis.predict_sentences(stock_news_dict[stock])
        positive_sentiment_count = 0
        for article_sentiment in predictions:
            if article_sentiment == 'positive':
                positive_sentiment_count += 1
        positive_sentiment_percentage = (positive_sentiment_count/len(predictions)) * 100
        print_sentiment_message(stock, positive_sentiment_percentage + '(Recommendation based on ' + str(len(predictions)) + ' news articles)')
    

if __name__ == "__main__":
    main()

"""
- Add a moving terminal graphic to show the code is still executing (takes a while)

"""



