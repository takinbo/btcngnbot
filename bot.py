import logging
import exchanges as ex
import re
from decimal import Decimal, ROUND_UP, localcontext
from fuzzywuzzy import process
from mwt import MWT
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from prettyconf import config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
exchanges = {klass.symbol: klass for klass in ex.__exchanges__}
tickers = ['ngn', 'btc']

help_messages = {
    'general': '''
Commands:

*calc* - Converts amounts from one currency to the other
*price* - Displays the price of a ticker symbol

Each command has additional help. Type /help command (e.g. /help calc) for more help.
''',
    'price': '''
*/price* - Displays the price of a ticker symbol (currently only btc)

```
Syntax : /price [exchange]
Example: /price
         /price bitx
```
''',
    'calc': '''
*/calc* - Converts amounts from one currency to the other

```
Syntax : /calc amount [currency] [exchange]
Example: /calc 225,000
         /calc 15,000.23 ngn
         /calc 1 btc bitx
```
''',
}

@MWT(timeout=15)
def get_exchange_rate(exchange=None):
    if exchange:
        klass = exchanges[exchange]
        return klass().exchange_rate()
    else:
        rates = [get_exchange_rate(e) for e in exchanges.keys()]
        return sum(rates)/len(rates)

def start_command(bot, update):
    update.message.reply_text('''Hi *{}*!

I can provide bitcoin prices across a number of exchanges in Naira and can also help you calculate prices for different quantities of bitcoin.

How can I /help?'''.format(update.message.from_user.first_name), parse_mode=ParseMode.MARKDOWN)

def price_command(bot, update, args):
    if len(args) > 0:
        exchange = process.extractOne(args[0], exchanges.keys(), score_cutoff=60)
        if not exchange:
            update.message.reply_text(
                'Supported exchanges: {}'.format(', '.join(exchanges.keys())),
                parse_mode=ParseMode.MARKDOWN)
            return
    else:
        exchange = None

    if exchange:
        exchange_rate = get_exchange_rate(exchange[0])
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
    update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)

def calc_command(bot, update, args):
    if len(args) < 1:
        response = help_messages['calc']
        update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
        return

    exchange = None
    currency = None
    amount = re.sub('[^0-9\.]', '', args[0])
    if amount:
        amount = Decimal(amount)
    else:
        update.message.reply_text('`Invalid amount supplied.`', parse_mode=ParseMode.MARKDOWN)
        return

    if len(args) > 1:
        currency = process.extractOne(args[1], tickers, score_cutoff=60)

    if len(args) > 2:
        exchange = process.extractOne(args[2], exchanges.keys(), score_cutoff=60)
        if not exchange:
            update.message.reply_text('`Supported exchanges: {}`'.format(', '.join(exchanges.keys())), parse_mode=ParseMode.MARKDOWN)
            return

    if currency:
        currency = currency[0]

    if exchange:
        rate = get_exchange_rate(exchange[0])
    else:
        rate = get_exchange_rate()

    if currency == tickers[1]:
        target = amount * rate
        response = "`₦{:,.2f}`".format(target)
    else:
        target = amount / rate
        with localcontext() as ctx:
            ctx.prec = 8
            ctx.rounding = ROUND_UP
            response = "`฿{:.8g}`".format(target)

    update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)

def help_command(bot, update, args):
    topics = ['price', 'calc']
    topic = ''
    if args:
        choice = process.extractOne(args[0], topics, score_cutoff=60)
        if choice:
            topic = choice[0]

    response = help_messages.get(topic, help_messages['general'])

    update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)

def unknown_command(bot, update):
    update.message.reply_text("Sorry I didn't understand your command. Please respond with /help for help.", parse_mode=ParseMode.MARKDOWN)

if __name__ == '__main__':
    updater = Updater(config("TOKEN"))

    updater.dispatcher.add_handler(CommandHandler('start', start_command))
    updater.dispatcher.add_handler(CommandHandler('price', price_command, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('calc', calc_command, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('help', help_command, pass_args=True))
    updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown_command))

    updater.start_polling()
    updater.idle()
