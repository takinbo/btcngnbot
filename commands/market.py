from telegram import ParseMode
from utils import render_to_string, exchanges, get_exchange_ticker

def market_command(bot, update):
    ctx = {'exchanges': []}
    for exchange in exchanges:
        ticker = get_exchange_ticker(exchange)
        ctx['exchanges'].append({'name': exchanges[exchange].name, 'bid': ticker['bid'], 'ask': ticker['ask']})

    update.message.reply_text(render_to_string('market.md', ctx), parse_mode=ParseMode.MARKDOWN, quote=False)
