import logging
from commands import (
    start_command, unknown_command, help_command,
    calc_command, price_command, market_command)
from prettyconf import config
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
updater = Updater(config('TOKEN'))

updater.dispatcher.add_handler(CommandHandler('start', start_command))
updater.dispatcher.add_handler(CommandHandler('market', market_command))
updater.dispatcher.add_handler(CommandHandler('price', price_command, pass_args=True))
updater.dispatcher.add_handler(CommandHandler('calc', calc_command, pass_args=True))
updater.dispatcher.add_handler(CommandHandler('help', help_command, pass_args=True))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown_command))

prod = config('PRODUCTION', default=False, cast=config.boolean)
port = config('PORT', default="8001", cast=config.eval)

if __name__ == '__main__':
    if prod:
        updater.start_webhook(port=port, url_path=config('TOKEN'))
    else:
        updater.start_polling()
    updater.idle()
