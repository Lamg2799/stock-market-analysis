import requests
from dotenv import load_dotenv
import os
from urllib.parse import parse_qs, urlparse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# To use .env for hidden local user info
try:
    load_dotenv()
    QUESTRADE_APP_ID = os.getenv('QUESTRADE_APP_ID')
    QUESTRADE_GRANT_SERVER = os.getenv('QUESTRADE_GRANT_SERVER')
    QUESTRADE_ACCOUNT_ID = os.getenv('QUESTRADE_ACCOUNT_ID')
except Exception as e:
    print('Could not retrieve Questrade details from .env file.')
    exit()

REDIRECT_URL = 'https://www.example.com'
AUTH_URI = QUESTRADE_GRANT_SERVER + '?client_id=' + QUESTRADE_APP_ID + '&response_type=token&redirect_uri=' + REDIRECT_URL

def get_account_position_names(driver):
    """
    Retrieves the position names from a Questrade account using their api. https://www.questrade.com/api.

    Args:
        driver: An instance of Selenium webdriver for browser access.

    Returns:
        A list of position names as strings that are held by a questrade account.
    """
    driver.get(AUTH_URI)
    WebDriverWait(driver, 180).until(EC.url_contains(REDIRECT_URL + "/#"))
    parsed_url_data = parse_qs(urlparse(driver.current_url).fragment)

    try:
        user_auth = {
            'access_token': parsed_url_data['access_token'][0],
            'refresh_token': parsed_url_data['refresh_token'][0],
            'token_type': parsed_url_data['token_type'][0],
            'expires_in': parsed_url_data['expires_in'][0],
            'api_server': parsed_url_data['api_server'][0],
        }
    except:
        print('Error when parsing the Questrade verification url fragment.')
        quit()

    headers = {
        'Host': user_auth['api_server'],
        'Authorization': user_auth['token_type'] + ' ' + user_auth['access_token']
    }
    try:
        account_positions_info = requests.get(url=user_auth['api_server'] + 'v1/accounts/' + QUESTRADE_ACCOUNT_ID + '/positions', headers=headers)
        position_names = [position['symbol'] for position in account_positions_info.json()['positions']]
    except Exception as e: 
        print('An error has occurred while retrieving Questrade account positions: ', e)

    return position_names



