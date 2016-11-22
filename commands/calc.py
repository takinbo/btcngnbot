from decimal import Decimal, ROUND_UP, localcontext
from telegram import ParseMode
from utils import render_to_string, exchanges, get_exchange_rate, make_choice
import re

def calc_command(bot, update, args):
    tickers = ['ngn', 'btc']

    if len(args) < 1:
        update.message.reply_text(render_to_string('help/calc.md'), parse_mode=ParseMode.MARKDOWN, quote=False)
        return

    exchange = None
    currency = None
    amount = re.sub('[^0-9\.]', '', args[0])
    if amount:
        amount = Decimal(amount)
    else:
        update.message.reply_text('`Invalid amount supplied.`', parse_mode=ParseMode.MARKDOWN, quote=False)
        return

    if len(args) > 1:
        currency = make_choice(args[1], tickers)

    if len(args) > 2:
        exchange = make_choice(args[2], exchanges.keys()) 
        if not exchange:
            update.message.reply_text('`Supported exchanges: {}`'.format(', '.join(exchanges.keys())), parse_mode=ParseMode.MARKDOWN, quote=False)
            return

    if exchange:
        rate = get_exchange_rate(exchange)
    else:
        rate = get_exchange_rate()

    if currency == tickers[1]:
        target = amount * rate
        response = render_to_string('ngn.md', {'amount': target })
    else:
        target = amount / rate
        with localcontext() as ctx:
            ctx.prec = 8
            ctx.rounding = ROUND_UP
            response = render_to_string('btc.md', {'amount': target })

    update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN, quote=False)
