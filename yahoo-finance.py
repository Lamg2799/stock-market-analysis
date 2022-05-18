import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

yahoo_base_url = 'https://finance.yahoo.com'
stocks = [
    ['AAPL', ['Apple', 'AAPL']]
]

driver = webdriver.Firefox()
driver.maximize_window()

for stock in stocks:
    current_url = yahoo_base_url + '/quote/' + stock[0] + '/news?p=' + stock[0]
    driver.get(current_url)
    news_feed = driver.find_element(By.ID, 'latestQuoteNewsStream-0-Stream')
    news_feed_list = news_feed.find_element(By.TAG_NAME, 'ul')
    news_feed_list_elements = news_feed_list.find_elements(By.TAG_NAME, 'li')
    news_feed_list_elements_hrefs = []
    for current_element in news_feed_list_elements:
        valid = False
        link = current_element.find_element(By.TAG_NAME, 'a')
        for name in stock[1]:
            if name.lower() in link.text.lower():
                valid = True
                news_feed_list_elements_hrefs.append(link.get_attribute('href'))

    for href in news_feed_list_elements_hrefs:
        driver.get(href)
        WebDriverWait(driver, 15).until(EC.url_changes(current_url))
        article_text_list = driver.find_elements(By.TAG_NAME, 'p')
        text_string = ''
        for text_block in article_text_list:
            text_string += text_block.text.strip()
        print(stock , ': ' + text_string)
driver.quit()








