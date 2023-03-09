import requests
import json
from TOKEN import keys


# Классы, ошибоки
class ConvertionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Не возможно перевести одинаковые валюты {base}')

        try:
            quote_ticket = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалоь обрюотать валюту {quote}')

        try:
            base_ticket = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')


        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticket}&tsyms={base_ticket}')
        total_base = json.loads(r.content)[keys[base]] * amount


        return total_base


