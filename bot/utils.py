"""
Utility functions for Secret Santa Bot
"""
import os
from bot.database import Database

# Initialize database with path from environment or default
db_path = os.getenv("DB_PATH", "secret_santa.db")
db = Database(db_path)


def get_lang(chat_id: int) -> str:
    """Get language preference for a chat"""
    return db.get_language(chat_id)
