from telegram import ParseMode
from utils import render_to_string

def unknown_command(bot, update):
    update.message.reply_text(render_to_string('unknown.md'), parse_mode=ParseMode.MARKDOWN, quote=False)

