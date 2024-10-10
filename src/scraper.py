from telethon import TelegramClient, sync
import os

# Your API ID and API Hash (from my.telegram.org)

api_id = ''
api_hash = ''

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
