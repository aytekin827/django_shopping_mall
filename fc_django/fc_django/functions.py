import requests
import datetime

def get_exchange():
    today = datetime.datetime.now()
    if today.weekday() >= 5:
        diff = today.weekday() - 4
        today = datetime.timedelta(days=diff)
    today = today.strftime('%Y%m%d')

    auth = 'L8BZPjweTRiGu6K3bL3IU7NfqaPo0BGV'
    url = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={}&searchdate={}&data=AP01'.format(auth, today)
    res = requests.get(url)
    data = res.json()

    for d in data:
        if d['cur_unit'] == "USD":
            return d['tts']