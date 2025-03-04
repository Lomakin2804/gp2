from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

class Coinmk:
    def __init__(self, api_key):
        self.api_key = api_key

    def finding_explorers(self, ticker, target):
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/info"
        parameters = {
            'symbol': ticker
        }
        headers= {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.api_key,
        }

        session = Session()
        session.headers.update(headers)

        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data['data'][ticker]['urls'][target]

    def add_metrics(self, ticker):
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        parameters = {
            'symbol': ticker,
            'convert': 'USD'
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.api_key,
        }

        session = Session()
        session.headers.update(headers)

        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return (data['data'][ticker]['quote']['USD'])









