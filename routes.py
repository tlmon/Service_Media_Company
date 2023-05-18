from flask import Flask,render_template,jsonify
import json
from datetime import datetime
from digester import get_digest
from importer import load
import random
from trender import calc_trends2

app = Flask(__name__)

@app.route('/api/v0/digest/accounter', methods=['GET'])
def get_digest_accounter():
    digest = get_digest(load(), 'buh', 30, 3)
    response = []
    for news in digest:
        tmp = {
            'url': news['url'],
            'publication_date': datetime.fromtimestamp(news['timestamp']).strftime('%Y-%m-%d %H:%M:%S'),
            'title': news['title'],
            'description': news['description']
        }
        response.append(tmp)
    return json.dumps(response, ensure_ascii=False).encode('utf8')

@app.route('/api/v0/digest/ceo', methods=['GET'])
def get_digest_ceo():
    digest = get_digest(load(), 'ceo', 30, 3)
    response = []
    for news in digest:
        tmp = {
            'url': news['url'],
            'publication_date': datetime.fromtimestamp(news['timestamp']).strftime('%Y-%m-%d %H:%M:%S'),
            'title': news['title'],
            'description': news['description']
        }
        response.append(tmp)
    return json.dumps(response, ensure_ascii=False).encode('utf8')

@app.route('/api/v0/trends', methods=['GET'])
def get_digest_trends():
    trends_raw = calc_trends2(load(), 180, 3)
    response = []
    keywords = trends_raw[0]
    trends = trends_raw[1]
    response = []
    for n in range(len(keywords)):
        parsed_trends = []
        for group in trends[n]:
            for trend in group:
                if trend not in parsed_trends:
                    parsed_trends.append(trend)
        random.shuffle(parsed_trends)
        response.append({
            'keyword': keywords[n],
            'trends': parsed_trends
        })        
    return json.dumps(response, ensure_ascii=False).encode('utf8')

@app.route('/api/v0/insights', methods=['GET'])
def get_digest_insights():
    def get_body(val):
        if (type(val) == list):
            ans = set()
            for i in val:
                ans.update(get_body(i))
            return list(ans)
        else:
            return [val]
    insights_raw = calc_trends2(load(), 3, 3)
    keywords = insights_raw[0]
    response = []
    for i in get_body(insights_raw[1]):
        response.append({
            'insight': i
        })
    return json.dumps(response, ensure_ascii=False).encode('utf8')


if __name__ == '__main__':
    app.run(debug=False, port=8080)
