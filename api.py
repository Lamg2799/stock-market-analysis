import requests
from dotenv import load_dotenv
import os

# To use .env
load_dotenv()

QUESTRADE_ACCESS_TOKEN = os.getenv('QUESTRADE_ACCESS_TOKEN')
QUESTRADE_REFRESH_SERVER = os.getenv('QUESTRADE_REFRESH_SERVER')
QUESTRADE_REFRESH_TOKEN = os.getenv('QUESTRADE_REFRESH_TOKEN')
QUESTRADE_REFRESH_GRANT_TYPE = os.getenv('QUESTRADE_REFRESH_GRANT_TYPE') + QUESTRADE_REFRESH_TOKEN
QUESTRADE_API_SERVER = os.getenv('QUESTRADE_API_SERVER')
QUESTRADE_TOKEN_TYPE = os.getenv('QUESTRADE_TOKEN_TYPE')
headers = {
    'Host':QUESTRADE_API_SERVER, 
    'Authorization':QUESTRADE_TOKEN_TYPE + " " + QUESTRADE_ACCESS_TOKEN
}

get_account = requests.get(url=QUESTRADE_API_SERVER + "v1/accounts", headers=headers)

print(get_account.json())


