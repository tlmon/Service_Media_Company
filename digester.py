import importer
from keyworder import idf_precalc, tf_idf, keywords_sum, keywords_norm, keywords_mean, most_popular_keywords, keywords_diff
from tokenizer import keywords_groups_calc
from clusterizer import clusterize


import time
import datetime

def get_data_before(data, days):
    time_begin = time.time() - datetime.timedelta(days=days).total_seconds()
    # data_news = list(filter(lambda i: time_begin <= i["timestap"], data))
    data_news = list(filter(lambda i: time_begin <= i["timestamp"], data))
    return data_news



def get_popular_keywords(keyword_groups, idfs):
    # idfs = idf_precalc([keyword_groups])

    # keyword_groups = tf_idf(keyword_groups, idfs)
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

# person_type = ceo or buh
# days = digest days count
# count = articles count
def get_digest(data_from_parser, person_type, days, count, debug=False):
    data = get_data_for_person(data_from_parser, person_type)
    idfs = idf_precalc([ keywords_groups_calc(data) ])

    data = get_data_before(data, days=days)
    keyword_groups = keywords_groups_calc(data)
    popular_keywords = get_popular_keywords(keyword_groups, idfs)
    res = clusterize(data, keyword_groups, popular_keywords, ccount=count, debug=debug)
    return res


# person_type = ceo or buh
# days = digest days count
# count = articles count
def get_digest_words(data_from_parser, person_type, days, count, debug=False, use_titles=False):
    data = get_data_for_person(data_from_parser, person_type)
    idfs = idf_precalc([ keywords_groups_calc(data) ])

    data = get_data_before(data, days=days)
    keyword_groups = keywords_groups_calc(data)
    popular_keywords = get_popular_keywords(keyword_groups, idfs)
    res = clusterize(data, keyword_groups, popular_keywords, ccount=count, debug=debug, return_words=True, use_titles=use_titles)
    return res

def get_data_for_person(data_from_parser, person_type):
    if person_type == "ceo":
        return data_from_parser["cfo"] + data_from_parser["rbc"]
    elif person_type == "buh":
        return data_from_parser["cons"] + data_from_parser["klerk"]+ data_from_parser["rbc"]
    elif person_type == "all":
        return data_from_parser["cons"] + data_from_parser["klerk"]+ data_from_parser["rbc"] + data_from_parser["cfo"] 
    elif person_type == "all_without_rbc":
        return data_from_parser["cons"] + data_from_parser["klerk"]+ data_from_parser["cfo"] 
    elif person_type == "rbc":
        return data_from_parser["rbc"]
