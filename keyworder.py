import math


def idf_precalc(keyword_groups_list):
    from collections import defaultdict
    df_counts = defaultdict(lambda: 0)
    documents_count = 0
    for documents in keyword_groups_list:
        for document in documents:
            documents_count += 1
            for key in document:
                df_counts[key] += 1
    
    idf_counts = {}
    for word in df_counts:
        idf_counts[word] = math.log2(documents_count / df_counts[word])
        # idf_counts[word] = math.log2(math.log2(documents_count / df_counts[word]))
            
    return idf_counts

def tf_idf(documents, idfs):
    res = []
    for document in documents:
        total_words_count = 0
        for key in document:
            total_words_count += document[key]["count"]
        
        rres = {}
        for key in document:
            rres[key] = document[key].copy()
            rres[key]["count"] = 1 * idfs[key]
            # rres[key]["count"] = rres[key]["count"] / total_words_count * idfs[key]
            
        res.append(rres)
    return res

def keywords_sum(documents):
    res = {}
    for document in documents:
        for key in document:
            if key not in res:
                res[key] = document[key].copy()
            else:
                res[key]["count"] += document[key]["count"]
    return res


def keywords_norm(documents):
    rres = []
    for document in documents:
        res = {}
        for key in document:
            res[key] = document[key].copy()
            res[key]["count"] = 1
        rres.append(res)
        
    return rres

def keywords_mean(documents):
    res = keywords_sum(documents)
    for key in res:
        res[key]["count"] /= len(documents)
    return res

def most_popular_keywords(document, count):
    res = []
    for key in document:
        res.append(document[key])
    res.sort(key=lambda k: -k["count"])
    return res[:count]


# left - right
def keywords_diff(left, right):
    res = left.copy()
    for key in right:
        if key not in res:
            res[key] = right[key] 
            res[key]["count"] = -res[key]["count"]
        else:
            res[key]["count"] -= right[key]["count"]
    return res


# idfs = idf_precalc([keyword_groups_before, keyword_groups_after])
# most_popular_keywords(keywords_sum(tf_idf(keyword_groups_before, idfs)), 10)
