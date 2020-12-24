import configparser
from pathlib import Path
import requests
import os
from bs4 import BeautifulSoup


config = configparser.ConfigParser()
config.read('.conf.ini')
BILLID = config['BLACK_CAT']['BILLID']
fn = 'table.html'


HEADERS = '''Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-TW,zh-CN;q=0.9,zh;q=0.8,en;q=0.7
Cache-Control: no-cache
Connection: keep-alive
Cookie: ASP.NET_SessionId=2hcxexcmyytlvkdk0w2ej3wq; __utma=8454064.1894533047.1608737248.1608737248.1608737248.1; __utmc=8454064; __utmz=8454064.1608737248.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); citrix_ns_id=usZEq9om5LyedqMwlhgMeTVvGmE0003; home_Alert=true; __utmt=1; ASPSESSIONIDCCTBQSDA=CNHLLNKBNNKDGDPCGDKGBNEL; citrix_ns_id=q6x9lSB/tSWwhyBY3FDZQUE4Tw80003; __utmb=8454064.11.10.1608737248
DNT: 1
Host: www.t-cat.com.tw
Pragma: no-cache
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'''


def get_requests(billid):
    headers = dict(l.split(': ') for l in HEADERS.split('\n'))
    url = 'https://www.t-cat.com.tw/Inquire/TraceDetail.aspx?BillID={BILLID}&ReturnUrl=Trace.aspx'
    url = url.replace('{BILLID}', billid)
    r = requests.get(url, headers=headers)
    return r.text


def parse_table(billid):
    html = get_requests(billid)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find('table')
    return table


def read_table():
    if Path(fn).exists():
        with open(fn, mode='r', encoding='utf8', errors='ignore') as f:
            table = f.read()
        return table
    return ''


def write_table(html):
    with open(fn, mode='w', encoding='utf8', errors='ignore') as f:
        f.write(html)


if __name__ == '__main__':

    table = parse_table(billid=BILLID)

    with open(fn, mode='w', encoding='utf8', errors='ignore') as f:
        f.write(table)
