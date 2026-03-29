import os
import logging
import asyncio
from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError

# --- Configuration ---
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# --- Logging ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def verify_connection():
    """Verify that the bot token is valid and can send messages."""
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.warning("TELEGRAM_BOT_TOKEN is not set or using placeholder.")
        return False

    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        bot_info = await bot.get_me()
        logger.info(f"Bot '@{bot_info.username}' is connected and authorized.")
        return True
    except TelegramError as e:
        logger.error(f"Failed to connect to Telegram: {e}")
        return False


async def main():
    logger.info("Dawn Dash Bot Starting...")

    # Verify environment
    is_authorized = await verify_connection()
    if not is_authorized:
        logger.warning("Running in limited mode. Please check your .env file.")

    logger.info("Heartbeat: Bot is alive. Use 'docker compose down' to stop.")

    # Stay alive loop
    while True:
        await asyncio.sleep(60)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
