"""
Utility functions for Secret Santa Bot
"""
from bot.database import Database

# Initialize database
db = Database()


def get_lang(chat_id: int) -> str:
    """Get language preference for a chat"""
    return db.get_language(chat_id)
