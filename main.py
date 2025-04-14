import os
import re
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from dotenv import load_dotenv
import logging

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Получаем переменные окружения
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")
OWNER_USERNAME = os.getenv("OWNER_USERNAME")  # Куда бот будет отправлять найденные сообщения

# Проверка, что все переменные есть
if not API_ID or not API_HASH or not SESSION_STRING:
    raise ValueError("API_ID, API_HASH или SESSION_STRING пустые. Проверь файл .env")

# Инициализация клиента
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# Ключевые паттерны для поиска вакансий
KEY_PATTERNS = [
    r"(ищу|нужен|нужна|нужны|ищем|требуется).{0,40}(админ|в админку|в администрацию)",
    r"(ищу|нужен|нужна|нужны|ищем|требуется).{0,40}(ассистент|ассистента|помощник|помощника|хелпер)",
    r"(ищу|нужен|нужна|нужны|ищем|требуется).{0,40}(на площадку|на съёмку|в команду|на проект)",
    r"(продюсер|продюсеру).{0,40}(ассистент|помощник|админ)",
]

# Функция фильтрации текста
def message_matches(text):
    text = text.lower()
    for pattern in KEY_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

# Проверка подключения
async def whoami():
    me = await client.get_me()
    print(f"✅ Бот успешно запущен от имени: {me.first_name} (@{me.username})")

# Основной обработчик новых сообщений
@client.on(events.NewMessage(incoming=True))
async def handle_new_message(event):
    try:
        message_text = event.message.message
        if message_matches(message_text):
            await client.send_message(OWNER_USERNAME, f"🔎 Найдена вакансия:\n\n{message_text}")
            logging.info("✅ Найдено и отправлено сообщение.")
    except Exception as e:
        logging.error(f"❌ Ошибка при обработке сообщения: {e}")

# Запуск
if __name__ == "__main__":
    print("🚀 Бот запускается...")
    with client:
        client.loop.run_until_complete(whoami())
        client.run_until_disconnected()
