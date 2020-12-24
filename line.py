import json
import configparser
import requests


config = configparser.ConfigParser()
config.read('.conf.ini')
CHANNEL_ACCESS_TOKEN = config['CHANNEL']['CHANNEL_ACCESS_TOKEN']
# CHANNEL_SECRET = config['CHANNEL']['CHANNEL_SECRET']


# from linebot import LineBotApi, WebhookHandler
# line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
# handler = WebhookHandler(CHANNEL_SECRET)


def send_line(text, token):
    url = "https://api.line.me/v2/bot/message/broadcast"  # broadcast
    headers = {'Content-Type': 'application/json'}
    headers['Authorization'] = f'Bearer {token}'
    data = {'messages': []}
    # data['messages'] += [{'type': 'text', 'text': '111'}]
    data['messages'] += [{'type': 'text', 'text': text}]
    data = json.dumps(data)
    response = requests.request(
        method="POST", url=url, headers=headers, data=data)


if __name__ == '__main__':
    send_line(text='123', token=CHANNEL_ACCESS_TOKEN)
