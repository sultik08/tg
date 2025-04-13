import os
import re
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from dotenv import load_dotenv
import logging  # Для логирования

# Загружаем переменные окружения из файла .env
load_dotenv()

# Настройки логирования
logging.basicConfig(level=logging.DEBUG)  # Устанавливаем уровень логирования

# Получаем переменные окружения через os.getenv
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")
OWNER_USERNAME = os.getenv("OWNER_USERNAME")

# Настройки клиента
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# Список регулярных выражений для фильтрации вакансий
KEY_PATTERNS = [
    r"(ищу|нужен|нужна|нужны|ищем|требуется).{0,40}(админ|в админку|в администрацию)",  # для админов
    r"(ищу|нужен|нужна|нужны|ищем|требуется).{0,40}(ассистент|ассистента|помощник|помощника|хелпер)",  # для ассистентов и помощников
    r"(ищу|нужен|нужна|нужны|ищем|требуется).{0,40}(на площадку|на съёмку|в команду|на проект)",  # для людей на проект
    r"(продюсер|продюсеру).{0,40}(ассистент|помощник|админ)",  # для продюсерских ассистентов
]

# Функция фильтрации сообщений
def message_matches(message_text: str) -> bool:
    message_text = message_text.lower()
    for pattern in KEY_PATTERNS:
        if re.search(pattern, message_text):
            return True
    return False

# Обработчик новых сообщений
@client.on(events.NewMessage(incoming=True))
async def handler(event):
    try:
        message_text = event.message.message
        if message_matches(message_text):
            await client.send_message(OWNER_USERNAME, f"🔎 Найдена вакансия:\n\n{message_text}")
    except Exception as e:
        logging.error(f"Ошибка при обработке сообщения: {e}")

# Запуск бота
print("🚀 Бот запущен...")
client.start()
client.run_until_disconnected()
