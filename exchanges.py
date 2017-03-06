from decimal import Decimal
import requests


class Exchange(object):
    name = ""
    symbol = ""

    def __init__(self):
        pass

    def exchange_rate(self):
        return Decimal('0')

    def ticker(self):
        return {'bid': Decimal('0'), 'ask': Decimal('0')}


class BitSSA(Exchange):
    name = "BitSSA"
    symbol = 'bitssa'

    def exchange_rate(self):
        try:
            res = requests.get("https://bitssa.com/api/v2/trades.json?market=btcngn&limit=1").json()
            if res:
                return Decimal(res[0]['price'])
        except:
            return Decimal('0')

    def ticker(self):
        try:
            res = requests.get("https://bitssa.com/api/v2/tickers.json").json()
            if res:
                return {'bid': Decimal(res['btcngn']['ticker']['buy']), 'ask': Decimal(res['btcngn']['ticker']['sell'])}
        except:
            return {'bid': Decimal('0'), 'ask': Decimal('0')}


class LBC(Exchange):
    name = 'LB'
    symbol = 'lb'

    def exchange_rate(self):
        try:
            res = requests.get("https://localbitcoins.com/bitcoinaverage/ticker-all-currencies/").json()
            if res:
                return Decimal(res['NGN']['rates']['last'])
        except:
            return Decimal('0')

    def ticker(self):
        t = {'bid': Decimal('0'), 'ask': Decimal('0')}
        try:
            bids = requests.get("https://localbitcoins.com/sell-bitcoins-online/NGN/national-bank-transfer/.json").json()
            if bids:
                bid = bids['data']['ad_list'][0]['data']['temp_price']
                t['bid'] = Decimal(bid)
        except:
            pass

        try:
            asks = requests.get("https://localbitcoins.com/buy-bitcoins-online/NGN/national-bank-transfer/.json").json()
            if asks:
                ask = asks['data']['ad_list'][0]['data']['temp_price']
                t['ask'] = Decimal(ask)
        except:
            pass

        return t


class Luno(Exchange):
    name = "Luno"
    symbol = 'luno'

    def exchange_rate(self):
        try:
            res = requests.get("https://api.mybitx.com/api/1/ticker?pair=XBTNGN").json()
            if res:
                return Decimal(res['last_trade'])
        except:
            return Decimal('0')

    def ticker(self):
        try:
            res = requests.get("https://api.mybitx.com/api/1/ticker?pair=XBTNGN").json()
            if res:
                return {'bid': Decimal(res['bid']), 'ask': Decimal(res['ask'])}
        except:
            return {'bid': Decimal('0'), 'ask': Decimal('0')}


__exchanges__ = [BitSSA, LBC, Luno]
