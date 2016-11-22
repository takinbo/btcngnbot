from decimal import Decimal
import requests


class Exchange(object):
    name = ""
    symbol = ""

    def __init__(self):
        pass

    def exchange_rate(self):
        pass


class BitX(Exchange):
    name = "BitX"
    symbol = 'bitx'

    def exchange_rate(self):
        try:
            res = requests.get("https://api.mybitx.com/api/1/tickers").json()
            if res:
                tradepair = next(filter(lambda t: t['pair'] == 'XBTNGN', res['tickers']))
                return Decimal(tradepair['last_trade'])
        except:
            return Decimal('0')


class LBC(Exchange):
    name = 'LocalBitcoins'
    symbol = 'lb'

    def exchange_rate(self):
        try:
            res = requests.get("https://localbitcoins.com/bitcoinaverage/ticker-all-currencies/").json()
            if res:
                return Decimal(res['NGN']['rates']['last'])
        except:
            return Decimal('0')


__exchanges__ = [BitX, LBC]
