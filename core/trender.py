from tokenizer import snowball
from digester import get_digest_words
import pymorphy2
from importer import load
import time

def get_trends(days, count):
    trends_raw = calc_trends(load(), days, count)
    response = []
    keywords = trends_raw[0]
    trends = trends_raw[1]
    for n in range(len(keywords)):
        parsed_trends = []
        for group in trends[n]:
            for trend in group:
                if trend not in parsed_trends:
                    parsed_trends.append(trend)
        response.append({
            'keyword': keywords[n],
            'trends': parsed_trends
        })
    return response


def get_insights(days, count):
    def get_body(val):
        if (type(val) == list):
            ans = set()
            for i in val:
                ans.update(get_body(i))
            return list(ans)
        else:
            return [val]
    insights_raw = calc_trends(load(), days, count)
    keywords = insights_raw[0]
    response = []
    for i in get_body(insights_raw[1]):
        response.append({
            'insight': i
        })
    return response


# calc_trends(data_from_parser, days=180, count=3, use_titles=False)
def calc_trends(data_from_parser, days, count, use_titles=False):
    morph = pymorphy2.MorphAnalyzer()
    digest_words = get_digest_words(data_from_parser, days=days, count=count, debug=False, use_titles=use_titles)
    res = []
    articles_res = []
    for words in digest_words:
        rres = []
        articles_rres = []
        for word in words:
            normal = morph.parse(word[0])
            normal = normal[0]
            if normal.tag._POS in ["NUMB", "UNKN"]:
                continue
            if normal.tag.POS in ["COMP", "PRTS", "PRTF"]:
                continue
            if normal.normal_form in ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 
            'июль', 'август', "сентябрь", "октябрь", 'ноябрь', 'декабрь', 'вебинар']:
                continue
            form = word[0]
            if word[0].upper() == word[0]:
                form = word[0]
            elif normal.score > 0.7:
                form = normal.normal_form
            short = snowball.stem(word[0])
            articles_rrres = []
            for i in word[2]:
                if short in i['title'] or word[0] in i['title'] or form in i['title']:
                    articles_rrres.append(i['title'])
            articles_rres.append(articles_rrres)
            rres.append(form)
            if len(rres) == 3:
                break
        articles_res.append(articles_rres)
        res.append(rres)
    return res, articles_res
