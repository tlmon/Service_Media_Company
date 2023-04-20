from flask import Flask,render_template,jsonify
import json
from datetime import datetime
from digester import get_digest
from importer import load
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
    def get_body(val):
        if (type(val) == list):
            ans = []
            for i in val:
                ans += get_body(i)
            return ans
        else:
            return [val]
    trend = calc_trends2(load(), 180, 3)
    response = []
    for i in get_body(trend[1]):
        response.append({
            'trend': i
        })
    return json.dumps(response[3:], ensure_ascii=False).encode('utf8')

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
    insight = calc_trends2(load(), 3, 3)
    response = []
    for i in get_body(insight[1]):
        response.append({
            'insight': i
        })
    return json.dumps(response, ensure_ascii=False).encode('utf8')


if __name__ == '__main__':
    app.run(debug=False, port=8080)
