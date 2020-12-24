from line import send_line
import os
from blackcat import get_requests, parse_table, read_table, write_table
from gmail import send_mail
import time
from pathlib import Path
import configparser


config = configparser.ConfigParser()
config.read('.conf.ini')
GMAIL_USER = config['MAIL']['GMAIL_USER']
GMAIL_PASSWORD = config['MAIL']['GMAIL_PASSWORD']
BILLID = config['BLACK_CAT']['BILLID']
RECIPIENT = config['MAIL']['RECIPIENT']
URL = 'https://www.t-cat.com.tw/Inquire/TraceDetail.aspx?BillID={BILLID}&ReturnUrl=Trace.aspx'.replace(
    '{BILLID}', BILLID)
CHANNEL_ACCESS_TOKEN = config['CHANNEL']['CHANNEL_ACCESS_TOKEN']
CHANNEL_ACCESS_TOKEN_2 = config['CHANNEL_2']['CHANNEL_ACCESS_TOKEN']


def get_color(code):
    return f'\033[{str(code)}m'


def log(msg):
    re = time.strftime("%Y-%m%d %H:%M:%S", time.localtime())
    fn = 'log.txt'
    with open(fn, mode='a+', encoding='utf8', errors='ignore') as f:
        t = re + msg+'\n'
        f.write(t)
    return re


def now(msg):
    re = time.strftime("%Y-%m%d %H:%M:%S", time.localtime())
    print(re, msg)
    log(msg)
    return re


def main():
    old_table = read_table()
    while 1:
        new_table = parse_table(billid=BILLID).prettify().replace('\r', '')
        if new_table != old_table:
            # print('不同')

            # t = f"{get_color('31;1')}{'狀態變動!'}{get_color(0)}"
            # now(t)

            send_mail(subject='黑貓狀態變動!', content=str(new_table), isHtml=True)
            send_line(text='黑貓狀態變動!'+' '+URL, token=CHANNEL_ACCESS_TOKEN)

            # t = f"{get_color('32;1')}{'寄信完成!'}{get_color(0)}"
            # now(t)

            write_table(new_table)
            old_table = new_table
        else:
            t = time.strftime("%H:%M:%S", time.localtime())
            if t[-2:] in ['00', '01']:
                send_line(text='alive', token=CHANNEL_ACCESS_TOKEN_2)

        time.sleep(1)


if __name__ == '__main__':
    main()
