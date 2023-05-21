from keyworder import idf_precalc, tf_idf, keywords_mean, most_popular_keywords, keywords_diff
from tokenizer import keywords_groups_calc
from clusterizer import clusterize

import time
import datetime

def get_data_before(data, days):
    time_begin = time.time() - datetime.timedelta(days=days).total_seconds()
    data_news = list(filter(lambda i: time_begin <= i["timestamp"], data))
    return data_news


def get_popular_keywords(keyword_groups, idfs):
    keyword_groups = tf_idf(keyword_groups, idfs)
    mmean = keywords_mean(keyword_groups)
    popular_keywords = []
    for document in keyword_groups:
        p = most_popular_keywords(keywords_diff(document, mmean), 30)
        popular_keywords.append({
            "short": set([i['short'] for i in p]), 
            "long": {
                i['short']: i for i in p
            }
        })
    return popular_keywords


def get_digest_words(data_from_parser, days, count, debug=False, use_titles=False):
    data = get_data_for_person(data_from_parser)
    idfs = idf_precalc([ keywords_groups_calc(data) ])
    data = get_data_before(data, days=days)
    keyword_groups = keywords_groups_calc(data)
    popular_keywords = get_popular_keywords(keyword_groups, idfs)
    res = clusterize(data, keyword_groups, popular_keywords, ccount=count, debug=debug, return_words=True, use_titles=use_titles)
    return res


def get_data_for_person(data_from_parser):
    return data_from_parser["cons"] + data_from_parser["klerk"]+ data_from_parser["rbc"] + data_from_parser["cfo"] 
