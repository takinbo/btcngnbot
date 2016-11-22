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
        response = render_to_string('quote.md', {'rate': exchange_rate})
    else:
        ctx = {'exchanges': []}
        for exchange in exchanges:
            rate = get_exchange_rate(exchange)
            ctx['exchanges'].append({'name': exchanges[exchange].name, 'rate': rate})

        ctx['average_rate'] = get_exchange_rate()
        response = render_to_string('price.md', ctx)
    update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN, quote=False)
