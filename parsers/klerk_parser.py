import requests as rq
from bs4 import BeautifulSoup as bs
import re
import datetime as dt
import json
import os

KLERK_NEWS_URL='https://www.klerk.ru/news/page/'


def parse_klerk_news(days=1):
    page_number = 1
    ress = []
    while (True):
        response = rq.get(KLERK_NEWS_URL + str(page_number))
        if (response.status_code == 200):
            page_number += 1
            news_urls = re.findall('klerk\.ru/buh/news/[\d]*/\"', response.text)[:-5]
            for news_url in news_urls:
                try:
                    res = {}
                    url = 'https://www.' + news_url[:-1]
                    res['url']= url
                    news = rq.get(url).text
                    soup = bs(news, 'html.parser')
                    res['site'] = 'klerk'
                    res['title'] = soup.body.find("h1")  .text.replace("\xa0", " ").replace("\t", " ")
                    res['text'] = soup.body.find(id="article-content").text.replace("\xa0", " ").replace("\t", " ")
                    try:
                        res['description'] = soup.body.find(class_="article__resume").text.replace("\xa0", " ").replace("\t", " ")
                    except:
                        if (len(res['text']) > 100):
                            res['description'] = res['text'][:100] + '...'
                        else:
                            res['description'] = res['text']
                    date_raw = re.findall('\d{4}-\d+-\d+ \d+:\d+:\d+', str(soup.body.time))[0]
                    date, time = date_raw.split()
                    date = date.split('-')
                    time = time.split(':')
                    res['timestamp'] = dt.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2])).timestamp()
                    if (days * 86400 + res['timestamp'] < dt.datetime.now().timestamp()):
                        return ress
                    ress.append(res)
                except Exception as e:
                    print(e, 'url:', url)
            
def main():   
    print('Start parsing klerk.ru')
    res = parse_klerk_news(2)
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    file_name = os.path.join(file_dir, '../data/kelrk_news.json')
    with open(file_name, 'w+') as outfile:
        json.dump(res, outfile)
    print('Finish parsing klerk.ru.')         

if __name__ == "__main__":
   main()
