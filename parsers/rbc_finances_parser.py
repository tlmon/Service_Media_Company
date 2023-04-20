import requests as rq
from bs4 import BeautifulSoup as bs
import datetime as dt
import json
import re
import os

RBC_FINANCE_URL = 'https://rbc.ru/v10/ajax/get-news-by-filters/?category=finances&limit=20&offset='
CLEANR = re.compile('<.*?>') 


def parse_rbc_news(days=1):
    offset = 0
    ress = []
    while (True):
        response = rq.get(RBC_FINANCE_URL + str(offset))
        offset += 20
        if (response.status_code == 200):
            news_urls = re.findall('https://www.rbc.ru/finances/\d+/\d+/\d+/\w+', response.text)
            for url in news_urls:
                try:
                    res = {}
                    res['url']= url
                    news = rq.get(url).text
                    soup = bs(news, 'html.parser')
                    res['site'] = 'rbc_finances'
                    res['title'] = soup.body.find(class_="article__header__title-in js-slide-title").text.replace("\xa0", " ").replace("\t", " ").strip()
                    
                    def cleanhtml(raw_html):
                        return re.sub(CLEANR, '', raw_html)

                    raw = soup.body.find('div', class_="article__text article__text_free").find_all('p')
                    res['text'] = ''
                    for i in raw:
                        if (str(i).find('span') == -1):
                            res['text'] += cleanhtml(str(i))
                    try:
                        res['description'] = soup.body.find(class_="article__text__overview").text.replace("\xa0", " ").replace("\t", " ")
                    except:
                        if (len(res['text']) > 100):
                            res['description'] = res['text'][:100] + '...'
                        else:
                            res['description'] = res['text']
                    date_raw =re.findall('\d{4}-\d+-\d+T\d+:\d+:\d+' ,str(soup.body.find(class_="article__header__date")))[0]
                    date, time = date_raw.split('T')
                    date = date.split('-')
                    time = time.split(':')
                    res['timestamp'] = dt.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2])).timestamp()
                    if (days * 86400 + res['timestamp'] < dt.datetime.now().timestamp()):
                        return ress
                    ress.append(res)
                except Exception as e:
                    print(e, url)
        else:
            return ress


def main():
    print('Start parsing rbc finances.')
    res = parse_rbc_news(365)
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    file_name = os.path.join(file_dir, '../data/rbc_finances_news.json')
    with open(file_name, 'w+') as outfile:
        json.dump(res, outfile)
    print('Finish parsing rbc finances.')
            

if __name__ == "__main__":
    main()
    