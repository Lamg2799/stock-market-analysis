from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# non-yahoo finance
def parse_p_text_external(soup):
    print('external')
    article_text_list = soup.find_all('p')
    text_string = ''
    for text_block in article_text_list:
        text_string += text_block.get_text().strip()
    return text_string

# yahoo-finance
def parse_p_text_internal(soup):
    print('internal')
    article_text_body = soup.find('div', 'caas-body')
    article_text_list = article_text_body.find_all('p')
    text_string = ''
    for text_block in article_text_list:
        text_string += text_block.get_text().strip()
    return text_string

yahoo_base_url = 'https://finance.yahoo.com'
stocks = [
    ['AAPL', ['Apple', 'AAPL']]
]

driver = webdriver.Firefox()

start = time.time()
for stock in stocks:
    current_url = yahoo_base_url + '/quote/' + stock[0] + '/news?p=' + stock[0]
    driver.get(current_url)
    driver.execute_script("window.scrollTo(0,6000)")
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    news_articles = soup.find_all('h3', 'Mb(5px)')
    news_article_hrefs = []
    for news_article in news_articles:
        valid = False
        link = news_article.a
        for name in stock[1]:
            if link['href'] in news_article_hrefs:
                break
            else:
                if name.lower() in link.get_text().lower():
                    valid = True
                    news_article_hrefs.append(yahoo_base_url + link['href'])
    for href in news_article_hrefs:
        driver.get(href)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        continue_reading_link = soup.find('a', 'link caas-button')
        if continue_reading_link:
            href = continue_reading_link['href']
            driver.get(href)
            time.sleep(2)
            text_string = parse_p_text_external(soup)
        else:
            text_string = parse_p_text_internal(soup)
        print(text_string, '\n\n')
end = time.time()
print(end-start)




'''
    news_stream = soup.find(id='latestQuoteNewsStream-0-Stream')
    news_stream_list = news_stream.ul
    news_stream_list_hrefs = []
    for news_source in news_stream_list.children:
        print(news_source,'\n\n\n\n\n\n')
        valid = False
        link = news_source.a
        print(link.prettify())
        for name in stock[1]:
            if name.lower() in link.get_text().lower():
                valid = True
                news_stream_list_hrefs.append(link.href)
    print(news_stream_list_hrefs)

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
'''










