import requests
from bs4 import BeautifulSoup
import time
import datetime
import json
import os

headers = requests.utils.default_headers()
headers.update(
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    }
)


#"https://www.cfo-russia.ru/novosti/?article=73485"
def get_cfo_article(url):
    text = requests.get(url, headers=headers).text
    soup = BeautifulSoup(text, 'html.parser')
    import re
    CLEANR = re.compile('<.*?>') 

    def cleanhtml(raw_html):
        return re.sub(CLEANR, '', raw_html)


    html = str(soup.find("div", "news-detail").find("span", itemprop="description"))
    return cleanhtml(html).replace("\t", " ").replace("\xa0", " ")

# "https://www.cfo-russia.ru/novosti/?PAGEN_1=4"
def get_cfo_page(url):
    text = requests.get(url, headers=headers).text
    soup = BeautifulSoup(text, 'html.parser')

    res = []
    for i in soup.body.find(id="content").find("ul", "item-list").find_all("li"):
        title_a = i.find("div", "title").a
        url = "https://www.cfo-russia.ru" + str(title_a.get("href"))
        title = str(title_a.string).strip()
        description = str(i.find("div", "description").string).strip()
        date = str(i.find("div", "date-box").string).strip()
        timestamp = time.mktime(datetime.datetime.strptime(date, "%d.%m.%Y").timetuple())
        text = get_cfo_article(url)
        res.append({
            "url":url,
            "title": title,
            "description": description,
            "text": text,
            "timestamp": timestamp
        })
    return res

# get_cfo(0, 10)
def get_cfo(offset, count):
    res = []
    while len(res) < count:
        url = "https://www.cfo-russia.ru/novosti/?PAGEN_1=" + str(offset + 1)
        offset += 1
        res += get_cfo_page(url)
        
    return res[:count]


# get_cfo_days(10)
def get_cfo_days(days):
    res = []
    time_begin = time.time() - datetime.timedelta(days=days).total_seconds()
    offset = 0 # datetime.date.today()
    while len(res) == 0 or time_begin <= res[-1]["timestamp"]:
        url = "https://www.cfo-russia.ru/novosti/?PAGEN_1=" + str(offset + 1)
        offset += 1
        res += get_cfo_page(url)
    return list(filter(lambda i : time_begin <= i["timestamp"], res))


def main():
    print('Start parsing cfo-russia.ru.')
    res = get_cfo_days(2)
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    file_name = os.path.join(file_dir, '../data/cfo_news.json')
    with open(file_name, 'w+') as outfile:
        json.dump(res, outfile)
    print('Finish parsing cfo-russia.ru.')


if __name__ == "__main__":
    main()
    