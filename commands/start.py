from telegram import ParseMode
from utils import render_to_string

def start_command(bot, update):
    update.message.reply_text(render_to_string('start.md', {'first_name': update.message.from_user.first_name}), parse_mode=ParseMode.MARKDOWN, quote=False)
