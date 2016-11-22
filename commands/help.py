from telegram import ParseMode
from utils import render_to_string, make_choice

def help_command(bot, update, args):
    topics = {'price': 'help/price.md', 'calc': 'help/calc.md', 'market': 'help/market.md'}
    topic = ''
    if args:
        topic = make_choice(args[0], topics.keys())

    template = topics.get(topic, 'help/general.md')

    update.message.reply_text(render_to_string(template), parse_mode=ParseMode.MARKDOWN, quote=False)

