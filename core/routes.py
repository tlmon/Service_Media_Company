from flask import Flask
import json
from trender import get_trends, get_insights

app = Flask(__name__)

@app.route('/api/v0/trends', methods=['GET'])
def trends():
    trends =  get_trends(days=180, count=3)
    trends_dumped = json.dumps(trends, ensure_ascii=False).encode('utf8')
    return trends_dumped


@app.route('/api/v0/insights', methods=['GET'])
def insights():
    insights = get_insights(days=3, count=3)
    insights_dupmed = json.dumps(insights, ensure_ascii=False).encode('utf8')
    return insights_dupmed


if __name__ == '__main__':
    app.run(debug=False, port=8080)
