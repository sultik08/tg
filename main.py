from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
session_string = os.environ.get("SESSION_STRING")
owner_username = os.environ.get("OWNER_USERNAME")

client = TelegramClient(StringSession(session_string), api_id, api_hash)

KEYWORDS = ["ассистент", "съёмка", "работа в кино", "продюсер", "оплата", "дедлайн"]

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if event.is_group or event.is_channel:
        msg = event.message.message.lower()
        if any(keyword in msg for keyword in KEYWORDS):
            await client.send_message(owner_username, f"👀 Вакансия:\n\n{event.message.message}")

print("🚀 Бот запущен...")
client.start()
client.run_until_disconnected()
