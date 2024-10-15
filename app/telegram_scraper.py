from telethon import TelegramClient
import logging
import os
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    filename='logs/api_telegram_scraping.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load environment variables once
load_dotenv('.env')
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

client = TelegramClient('session_name', api_id, api_hash)

async def scrape_telegram_channel(channel):
    messages = []
    async with client:
        async for message in client.iter_messages(channel):
            messages.append({
                'channel': channel,
                'message_content': message.text
            })
    return messages
