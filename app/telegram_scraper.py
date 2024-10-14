from telethon import TelegramClient
import logging

api_id = '22245208'
api_hash = '97e00dd8cc0c9e215c5226c2f6d34be2'

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
