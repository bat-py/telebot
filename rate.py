# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import json

URL = ['https://uzobmen.net/xchange_Uzcard_to_QWRUB/',  # uzcard to qiwi
       'https://uzobmen.net/xchange_QWRUB_to_Uzcard/',  # qiwi to uzcard
       ]
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0',
    'Accept': '*/*'
}


# Returns html page
def get_html(url, params=None):
    html = requests.get(url, headers=HEADERS, params=params)
    return html


def get_rate_1(html):
    soup = BeautifulSoup(html, 'html.parser')
    rate = soup.find('input', id='wsumm1').get('value')
    return rate


def get_rate_2(html):
    soup = BeautifulSoup(html, 'html.parser')
    rate = soup.find('input', id='wsumm2').get('value')
    return rate


def writer():
    html1 = get_html(URL[0])
    html2 = get_html(URL[1])
    if html1.status_code == 200 and html2.status_code == 200:
        uzcard_to_qiwi = get_rate_1(html1.text)
        qiwi_to_uzcard = get_rate_2(html2.text)
        rates = [uzcard_to_qiwi, qiwi_to_uzcard, time.asctime()]
        with open('/home/crow/PycharmProjects/telebot/rate.json', 'w', encoding='utf-8') as w:
            json.dump(rates, w, ensure_ascii=False)
    else:
        time.sleep(30)
        main()

def main():
    try:
        with open('/home/crow/PycharmProjects/telebot/rate.json', 'r', encoding='utf-8') as w:
            pass
    except:
        writer()
    else:
        writer()

if __name__ == '__main__':
    main()
