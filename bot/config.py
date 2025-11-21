"""
Configuration module for Secret Santa Bot
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_bot_token() -> str:
    """Get bot token from environment variables"""
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN not found in environment variables!")
    return token
