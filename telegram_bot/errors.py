import os
import yaml
import requests

from Scraper.settings import BASE_DIR

with open(os.path.join(BASE_DIR, 'credentials.yaml'), 'r') as f:
    credentials = yaml.safe_load(f)
BOT_TOKEN = credentials['TELEGRAM_BOT_TOKEN']
BOT_CHAT_ID = credentials['TELEGRAM_BOT_CHAT_ID']


def report_error(user, error):
    message = f'ERROR [{user}] {error}'
    url = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage?chat_id=' + BOT_CHAT_ID + '&&text=' + message
    requests.get(url)
