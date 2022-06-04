from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import TimeoutException

YAHOO_BASE_URL = 'https://finance.yahoo.com'

"""
Disabled due to the unprectability of external news sites. Such as article limits, and difficulty parsing arbitrary html.
Would be cool to reintroduce one day though!

# non-yahoo finance
def parse_p_text_external(soup):
    article_text_list = soup.find_all('p')
    text_string = ''
    for text_block in article_text_list:
        text_string += text_block.get_text().strip()
    return text_string
"""

def parse_p_text_internal(soup):
    """
    Parses text for yahoo-finance native articles (articles that don't require one to click external links to read the full article).

    Args:
        soup: An instance of BeautifulSoup for a particular article

    Returns:
        The text for the article as a string.
    """
    article_text_body = soup.find('div', 'caas-body')
    article_text_list = article_text_body.find_all('p')
    text_string = ''
    for text_block in article_text_list:
        text_string += text_block.get_text().strip()
    return text_string

def parse_stock_news(driver, stocks):
    """
    Parses the text from multiple recent news articles from each stock provided (if the stock has news) from yahoo finance.

    Args:
        driver: An instance of Selenium webdriver for browser access.
        stocks: A list of stock symbols as strings.

    Returns:
        A dictionary with key as a stock symbol, and value as a list of parsed texts from articles associated with the symbol.
    """
    try:
        sentences = dict()
        for stock in stocks:
            sentences[stock] = []
            current_url = YAHOO_BASE_URL + '/quote/' + stock + '/news?p=' + stock
            driver.get(current_url)
            driver.execute_script("window.scrollTo(0,6000)")
            time.sleep(2)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            news_articles = soup.find_all('h3', 'Mb(5px)')
            news_article_hrefs = []
            for news_article in news_articles:
                link = news_article.a
                news_article_hrefs.append(YAHOO_BASE_URL + link['href'])
            for href in news_article_hrefs:
                driver.get(href)
                time.sleep(2)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                continue_reading_link = soup.find('a', 'link caas-button')
                if continue_reading_link:
                    """
                    Disabled due to the unprectability of external news sites. Such as article limits, and difficulty parsing arbitrary html.
                    Would be cool to reintroduce one day though!

                    href = continue_reading_link['href']
                    driver.get(href)
                    time.sleep(2)
                    text_string = parse_p_text_external(soup)
                    """
                else:
                    text_string = parse_p_text_internal(soup)
                    sentences[stock].append(text_string)
        return sentences
    except TimeoutException as e:
        print('The connection timed out while parsing yahoo finance news:', e)
        quit()
    except Exception as e:
        print('An error has occurred while scraping yahoo finance news: ', e)









