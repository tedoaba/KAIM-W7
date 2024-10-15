from telethon import TelegramClient, sync
from dotenv import load_dotenv
import logging
import os
import json

load_dotenv('.env')

# Set up logging
logging.basicConfig(
    filename='../logs/image_scraping.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load environment variables once
load_dotenv('.env')
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone = os.getenv('PHONE_NUMBER')

# Define the client (replace 'session_name' with any name)
client = TelegramClient('session_name', api_id, api_hash)

# Connect to Telegram
client.start()

# Define the channel username or ID (You can use ID or '@channelusername')
channel = '@CheMed123'

# Folder to save the images
image_save_path = '../images/'
os.makedirs(image_save_path, exist_ok=True)

# Fetch messages from the channel
async def scrape_channel():
    async for message in client.iter_messages(channel):
        # Check if the message contains media (image)
        if message.photo:
            # Download the photo
            file_path = await message.download_media(file=image_save_path)
            print(f"Image saved to {file_path}")
            
# Run the scraping
with client:
    client.loop.run_until_complete(scrape_channel())
