import requests
from dotenv import load_dotenv
import os
from urllib.parse import parse_qs, urlparse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# To use .env for hidden local user info
load_dotenv()

QUESTRADE_APP_ID = os.getenv('QUESTRADE_APP_ID')
QUESTRADE_GRANT_SERVER = os.getenv('QUESTRADE_GRANT_SERVER')
QUESTRADE_ACCOUNT_ID = os.getenv('QUESTRADE_ACCOUNT_ID')
redirect_url = 'https://www.example.com'
auth_uri = QUESTRADE_GRANT_SERVER + '?client_id=' + QUESTRADE_APP_ID + '&response_type=token&redirect_uri=' + redirect_url


driver = webdriver.Firefox()

auth_response = driver.get(auth_uri)
WebDriverWait(driver, 180).until(EC.url_contains(redirect_url + "/#"))
parsed_url_data = parse_qs(urlparse(driver.current_url).fragment)

user_auth = {
    'access_token': parsed_url_data['access_token'][0],
    'refresh_token': parsed_url_data['refresh_token'][0],
    'token_type': parsed_url_data['token_type'][0],
    'expires_in': parsed_url_data['expires_in'][0],
    'api_server': parsed_url_data['api_server'][0],
}

headers = {
    'Host': user_auth['api_server'],
    'Authorization': user_auth['token_type'] + ' ' + user_auth['access_token']
}
get_account = requests.get(url=user_auth['api_server'] + 'v1/accounts/' + QUESTRADE_ACCOUNT_ID + '/positions', headers=headers)

print(get_account.json())



