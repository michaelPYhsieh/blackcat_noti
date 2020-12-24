import configparser
import smtplib
import email.message
import os


config = configparser.ConfigParser()
config.read('.conf.ini')
GMAIL_USER = config['MAIL']['GMAIL_USER']
GMAIL_PASSWORD = config['MAIL']['GMAIL_PASSWORD']
RECIPIENT = config['MAIL']['RECIPIENT']


def send_mail(subject=None, content=None, isHtml=False):
    gmail = {'host': 'smtp.gmail.com',
             'port': 465,
             'user': GMAIL_USER,
             'password': GMAIL_PASSWORD}
    conn_gmail = smtplib.SMTP_SSL(gmail['host'], gmail['port'])
    conn_gmail.login(gmail['user'], gmail['password'])

    msg = email.message.EmailMessage()
    msg['From'] = GMAIL_USER
    msg['To'] = RECIPIENT
    msg['Subject'] = subject  # opt
    if isHtml:
        msg.add_alternative(content, subtype='html')  # html信件
    else:
        msg.set_content(content)  # 純文字信件
    conn_gmail.send_message(msg)
    conn_gmail.close()


if __name__ == '__main__':
    subject = '主旨'
    content = '<h3>測試一</h3>測試二'
    send_mail(subject=subject, content=content, isHtml=True)
