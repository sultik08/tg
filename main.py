import os
import re
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from dotenv import load_dotenv
import logging

from pathlib import Path
load_dotenv(dotenv_path=Path('.') / '.env')  # Явно указываем путь

# Смотрим, что реально загружается
print("🔍 DEBUG:")
print("API_ID:", repr(os.getenv("API_ID")))
print("API_HASH:", repr(os.getenv("API_HASH")))
print("SESSION_STRING:", repr(os.getenv("SESSION_STRING")))

# Настройки логирования
logging.basicConfig(level=logging.DEBUG)

# Получаем переменные окружения через os.getenv
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")

# Преобразуем API_ID в int, если он не пустой
if API_ID:
    API_ID = int(API_ID)

# Выводим переменные для проверки
print(f"API_ID: {API_ID}")
print(f"API_HASH: {API_HASH}")
print(f"SESSION_STRING: {SESSION_STRING}")

# Проверка на пустоту
if not API_ID or not API_HASH or not SESSION_STRING:
    raise ValueError("API_ID, API_HASH или SESSION_STRING пустые. Проверь файл .env")

GROUP_ID = "@bknmoi"  # Используем ссылку на группу вместо ID

# Настройки клиента
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# Список регулярных выражений для фильтрации вакансий
KEY_PATTERNS = [
    r"(ищу|нужен|нужна|нужны|ищем|требуется).{0,40}(админ|в админку|в администрацию)",
    r"(ищу|нужен|нужна|нужны|ищем|требуется).{0,40}(ассистент|ассистента|помощник|помощника|хелпер)",
    r"(ищу|нужен|нужна|нужны|ищем|требуется).{0,40}(на площадку|на съёмку|в команду|на проект)",
    r"(продюсер|продюсеру).{0,40}(ассистент|помощник|админ)",
]

# Функция фильтрации сообщений
def message_matches(message_text: str) -> bool:
    message_text = message_text.lower()
    for pattern in KEY_PATTERNS:
        if re.search(pattern, message_text, re.IGNORECASE):
            return True
    return False

# Обработчик новых сообщений
@client.on(events.NewMessage(incoming=True))
async def handler(event):
    try:
        message_text = event.message.message
        if message_matches(message_text):
            await client.send_message(GROUP_ID, f"🔎 Найдена вакансия:\n\n{message_text}")
    except Exception as e:
        logging.error(f"Ошибка при обработке сообщения: {e}")

# Запуск бота
print("🚀 Бот запущен...")
client.start()
client.run_until_disconnected()
