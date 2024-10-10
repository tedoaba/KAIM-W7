import pandas as pd
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel
import asyncio

# Step 1: Define Telegram API credentials
API_ID = ''
API_HASH = ''
PHONE_NUMBER = ''
# Step 2: Create a function to connect to the Telegram client
client = TelegramClient('session_name', API_ID, API_HASH)

async def connect_telegram():
    await client.start(PHONE_NUMBER)
    if not await client.is_user_authorized():
        try:
            await client.send_code_request(PHONE_NUMBER)
            await client.sign_in(PHONE_NUMBER, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Enter your 2FA password: '))

# Step 3: Scraping messages from specific Telegram channels
async def scrape_channel_messages(channel_username, limit=10000):
    """
    Scrapes messages from a specific Telegram channel.

    Args:
        channel_username (str): The username or URL of the Telegram channel.
        limit (int): The maximum number of messages to scrape.
    
    Returns:
        DataFrame: A pandas DataFrame containing the scraped messages.
    """
    try:
        channel = await client.get_entity(PeerChannel(int(channel_username)) if channel_username.isdigit() else channel_username)
    except Exception as e:
        print(f"Could not access channel {channel_username}: {e}")
        return pd.DataFrame()

    messages = []
    async for message in client.iter_messages(channel, limit=limit):
        messages.append({
            'message_id': message.id,
            'date': message.date,
            'text': message.message,
            'sender_id': message.sender_id
        })
    
    return pd.DataFrame(messages)

# Step 4: Scraping data from multiple channels
async def scrape_multiple_channels(channel_list, message_limit=1000):
    """
    Scrapes data from a list of Telegram channels and aggregates it into a single DataFrame.

    Args:
        channel_list (list): List of Telegram channel usernames or URLs.
        message_limit (int): The number of messages to scrape per channel.

    Returns:
        DataFrame: A pandas DataFrame containing all the scraped messages.
    """
    all_data = pd.DataFrame()

    for channel in channel_list:
        print(f"Scraping messages from {channel}...")
        channel_data = await scrape_channel_messages(channel, limit=message_limit)
        all_data = pd.concat([all_data, channel_data], ignore_index=True)

    return all_data

# Step 5: Define the main function to run the pipeline
async def main():
    # List of Telegram channels
    channel_list = [
        '@DoctorsET',
        '@CheMed123',
        '@lobelia4cosmetics',
        '@yetenaweg',
        '@EAHCI'
    ]

    # Connect to Telegram
    await connect_telegram()

    # Scrape messages from the channels
    scraped_data = await scrape_multiple_channels(channel_list)

    # Save scraped data to CSV for later processing
    scraped_data.to_csv('../data/telegram_medical_businesses_data.csv', index=False)
    print("Data scraping complete. Data saved to 'telegram_medical_businesses_data.csv'.")

# Step 6: Start the script
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
