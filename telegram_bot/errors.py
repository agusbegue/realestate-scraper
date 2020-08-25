from telegram_bot.auth import BOT_TOKEN, BOT_CHAT_ID

import requests


def report_error(user, error):
    message = f'ERROR [{user}] {error}'
    url = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage?chat_id=' + BOT_CHAT_ID + '&&text=' + message
    requests.get(url)
