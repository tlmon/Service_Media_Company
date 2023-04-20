import requests as rq
from bs4 import BeautifulSoup as bs
import re
import datetime as dt
import json
import os

CONSULTANT_NEWS_URL='https://www.consultant.ru/legalnews/buh/'

headers = rq.utils.default_headers()
headers.update( 
    {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0',
    }
)

month_enum = {'янв': 1, 'фев': 2, 'мар': 3, 'апр': 4, 'мая': 5, 'июн': 6,
    'июл': 7, 'авг': 8, 'сен': 9, 'окт': 10, 'ноя': 11, 'дек': 12} 


def parse_consultant_news():
    ress = []
    response = rq.get(CONSULTANT_NEWS_URL, headers=headers)
    
    if (response.status_code == 200):
        news_urls = re.findall('legalnews/[\d]*/', response.text)
        news_urls = list(set(news_urls))
        for news_url in news_urls:
            res = {}
            url = 'https://www.consultant.ru/' + news_url
            res['url']= url
            news = rq.get(url).text
            soup = bs(news, 'html.parser')
            res['site'] = 'consultant'
            res['title'] = soup.body.find(class_="news-page__title").text.replace("\xa0", " ").replace("\t", " ")
            res['text'] = soup.body.find(class_="news-page__text").text.replace("\xa0", " ").replace("\t", " ")
            try:
                res['description'] = soup.body.find(class_="news-page__intro").text.replace("\xa0", " ").replace("\t", " ")
            except:
                if (len(res['text']) > 100):
                    res['description'] = res['text'][:100] + '...'
                else:
                    res['description'] = res['text']
            

            date_raw = soup.body.find(class_="news-page__date").text
            date = date_raw.split()
            date[1] = month_enum[date[1][:3]]
            res['timestamp'] = dt.datetime(int(date[2]), int(date[1]), int(date[0])).timestamp()
            ress.append(res)
    return sorted(ress, key=lambda d: -d['timestamp'])
            

def main():
    print('Start parsing consultant.')
    res = parse_consultant_news()
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    file_name = os.path.join(file_dir, '../data/consultant_news.json')
    with open(file_name, 'w+') as outfile: 
        json.dump(res, outfile)
    print('Finish parsing consultant.')


if __name__ == "__main__":
    main()
