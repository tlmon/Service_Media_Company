import requests as rq
import json

def get_trends_message():
    response = rq.get('http://127.0.0.1:8080/api/v0/trends')
    if response.status_code != 200:
        return "Произошла ошибка. Попробуйте позже..."
    result = "Тренды:\n"
    number = 1     
    for trend in json.loads(response.text):
        result += str(number) + '. Теги:' 
        for keyword in trend['keyword']:
            result += ' #' + keyword
        result += '\n'
        for trend in trend['trends'][:3]:
            result +=  '• ' + trend + '\n'
        number += 1
    return result


def get_insights_message():
    response = rq.get('http://127.0.0.1:8080/api/v0/insights')
    if response.status_code != 200:
        return "Произошла ошибка. Попробуйте позже..."
    result = "Инсайты:\n"
    number = 1     
    for insight in json.loads(response.text)[:10]:
        result += str(number) + '. ' + str.replace(insight['insight'], '\n', '') + '\n'
        number += 1
    return result