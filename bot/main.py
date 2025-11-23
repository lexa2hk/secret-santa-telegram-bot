"""
Secret Santa Telegram Bot
Main application entry point
"""
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

from bot.config import get_bot_token
from bot.handlers.base_handlers import start, help_command
from bot.handlers.admin_handlers import (
    setup,
    set_date,
    set_price,
    assign,
    button_callback,
    lang_command,
)
from bot.handlers.participant_handlers import (
    join,
    participants,
    info,
    my_assignment,
    chat_command,
    wish,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Suppress verbose httpx logs (only show warnings and errors)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by updates."""
    logger.error("Exception while handling an update:", exc_info=context.error)

    # Try to notify the user about the error
    if isinstance(update, Update) and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "❌ An error occurred while processing your request. Please try again later."
            )
        except Exception:
            # If we can't send a message, just log it
            logger.error("Could not send error message to user")


def main():
    """Start the bot."""
    try:
        token = get_bot_token()
    except ValueError as e:
        logger.error(str(e))
        return

    # Create the Application
    application = Application.builder().token(token).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("setup", setup))
    application.add_handler(CommandHandler("setdate", set_date))
    application.add_handler(CommandHandler("setprice", set_price))
    application.add_handler(CommandHandler("join", join))
    application.add_handler(CommandHandler("participants", participants))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("assign", assign))
    application.add_handler(CommandHandler("myassignment", my_assignment))
    application.add_handler(CommandHandler("lang", lang_command))
    application.add_handler(CommandHandler("wish", wish))
    application.add_handler(CommandHandler("chat", chat_command))
    application.add_handler(CallbackQueryHandler(button_callback))

    # Register error handler
    application.add_error_handler(error_handler)

    # Run the bot
    logger.info("Starting Secret Santa bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
