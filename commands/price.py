from telegram import ParseMode
from utils import render_to_string, make_choice, exchanges, get_exchange_rate

def price_command(bot, update, args):
    if len(args) > 0:
        exchange = make_choice(args[0], exchanges.keys())
        if not exchange:
            update.message.reply_text(
                'Supported exchanges: {}'.format(', '.join(exchanges.keys())),
                parse_mode=ParseMode.MARKDOWN, quote=False)
            return
    else:
        exchange = None

    if exchange:
        exchange_rate = get_exchange_rate(exchange)
        response = "`฿1 = ₦{:,.2f}`".format(exchange_rate)
    else:
        response = '''*XBT/NGN Spot Prices*
```
'''
        for exchange in exchanges:
            rate = get_exchange_rate(exchange)
            response += "{:<15}: ₦{:,.2f}\n".format(exchanges[exchange].name, rate)

        response = response.strip()
        response += '''```
`Avg. Price     : ₦{:,.2f}`
'''.format(get_exchange_rate())
    update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN, quote=False)
