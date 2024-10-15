from telethon import TelegramClient
import logging

api_id = ''
api_hash = ''


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
