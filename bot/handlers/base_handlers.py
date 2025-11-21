"""
Base command handlers for Secret Santa Bot
"""
from telegram import Update
from telegram.ext import ContextTypes

from bot.utils import get_lang
from bot.translations import get_text


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    chat = update.effective_chat
    lang = get_lang(chat.id)

    if chat.type == "private":
        await update.message.reply_text(
            get_text(lang, "start_private", name=user.first_name)
        )
    else:
        await update.message.reply_text(
            get_text(lang, "start_group")
        )
