from config import keys
import requests
import json

class ConvertionException(Exception):
    pass
class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str ):

        if quote == base:
            raise ConvertionException(f'Не возможно конвертировать одинаковые валюты {base}.')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту{quote}.')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту{base}.')
        try:
            amount = float(amount)
        except KeyError:
            raise ConvertionException(f'Не удалось обработать колличество {amount}.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        return total_base
