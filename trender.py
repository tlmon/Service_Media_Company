import time
import datetime

from tokenizer import keywords_groups_calc
from keyworder import idf_precalc, tf_idf, keywords_sum, keywords_norm, keywords_mean, most_popular_keywords, keywords_diff
from tokenizer import keywords_groups_calc
from clusterizer import clusterize

def get_trends(data_from_parser, days):
    data = data_from_parser["cfo"] + data_from_parser["cons"] + data_from_parser["klerk"] + data_from_parser["rbc"] 
    def filt(normal):
        if normal.tag._POS in ["NUMB", "UNKN"] or normal.tag.POS in ["COMP", "PRTS", "PRTF"]:
            return True
        if normal.normal_form in ["октябрь", "сентябрь", 'август']:
            return True
        return False

    idfs = idf_precalc([ keywords_groups_calc(data, filt=filt) ])

    time_begin = time.time() - datetime.timedelta(days=days).total_seconds()
    data_before = list(filter(lambda i: time_begin <= i["timestamp"], data))
    data_after = list(filter(lambda i: time_begin > i["timestamp"], data))

    keyword_groups_before = keywords_groups_calc(data_before, filt=filt)
    keyword_groups_after = keywords_groups_calc(data_after, filt=filt)

    keyword_groups_before = tf_idf(keyword_groups_before, idfs)
    keyword_groups_after = tf_idf(keyword_groups_after, idfs)

    keywords = most_popular_keywords(keywords_diff(keywords_mean(keyword_groups_before),
                                        keywords_mean(keyword_groups_after)), 20)

    import pymorphy2
    import string

    res = []
    morph = pymorphy2.MorphAnalyzer()

    for i in keywords:
        normal = morph.parse(i['word'])
        normal = normal[0]
        res.append(normal.normal_form)

    return res

# calc_trends2(data_from_parser, days=180, count=3, use_titles=False)
def calc_trends2(data_from_parser, days, count, use_titles=False):
    from tokenizer import snowball
    from digester import get_digest_words
    import pymorphy2

    morph = pymorphy2.MorphAnalyzer()
    digest_words = get_digest_words(data_from_parser, person_type="all", days=days, count=count, debug=False, use_titles=use_titles)

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
            if normal.normal_form in ["октябрь", "сентябрь", 'август', 'ноябрь', 'июнь', 'вебинар']:
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
                    # print(word[0], i['title'])

            articles_rres.append(articles_rrres)
            rres.append(form)
            if len(rres) == 3:
                break
        articles_res.append(articles_rres)

        res.append(rres)
    return res, articles_res
