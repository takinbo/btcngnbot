from decimal import Decimal, ROUND_UP, localcontext
from functools import partial
from telegram import ParseMode
from utils import render_to_string, exchanges, get_exchange_rate, make_choice
import re

def from_btc(amount, rate, multiplier=Decimal('1')):
    target = amount * rate * multiplier
    return render_to_string('ngn.md', {'amount': target })

def to_btc(amount, rate):
    target = amount / rate
    with localcontext() as ctx:
        ctx.prec = 8
        ctx.rounding = ROUND_UP
        return render_to_string('btc.md', {'amount': target })

def calc_command(bot, update, args):
    tickers = {
        'ngn':       to_btc,
        'btc':       from_btc,
        'mbtc':      partial(from_btc, multiplier=Decimal('0.001')),
        'millibit': partial(from_btc, multiplier=Decimal('0.001')),
        'bit':      partial(from_btc, multiplier=Decimal('0.000001')),
        'satoshi':  partial(from_btc, multiplier=Decimal('0.00000001')),
    }

    if len(args) < 1:
        update.message.reply_text(render_to_string('help/calc.md'), parse_mode=ParseMode.MARKDOWN, quote=False)
        return

    exchange = None
    ticker   = None
    amount = re.sub('[^0-9\.]', '', args[0])
    if amount:
        amount = Decimal(amount)
    else:
        update.message.reply_text('`Invalid amount supplied.`', parse_mode=ParseMode.MARKDOWN, quote=False)
        return

    if len(args) > 1:
        ticker = make_choice(args[1], tickers.keys())

    if len(args) > 2:
        exchange = make_choice(args[2], exchanges.keys()) 
        if not exchange:
            update.message.reply_text('`Supported exchanges: {}`'.format(', '.join(exchanges.keys())), parse_mode=ParseMode.MARKDOWN, quote=False)
            return

    if exchange:
        rate = get_exchange_rate(exchange)
    else:
        rate = get_exchange_rate()

    if ticker:
        response = tickers[ticker](amount, rate)
    else:
        response = tickers['ngn'](amount, rate)

    update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN, quote=False)
