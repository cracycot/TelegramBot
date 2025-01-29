import json
import logging
import os
from pyrogram import Client, filters
from config import API_ID, API_HASH, PHONE_NUMBER, TARGET_CHAT, CHANNELS
from filter import is_relevant
from OpenAI_handler import check_with_openai

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Client("session_name", api_id=API_ID, api_hash=API_HASH, phone_number=PHONE_NUMBER)

PROCESSED_MESSAGES_FILE = 'processed_messages.json'


def load_processed_messages():
    if not os.path.exists(PROCESSED_MESSAGES_FILE):
        return set()
    with open(PROCESSED_MESSAGES_FILE, 'r', encoding='utf-8') as f:
        try:
            return set(json.load(f))
        except json.JSONDecodeError:
            return set()


def save_processed_messages(processed_messages):
    with open(PROCESSED_MESSAGES_FILE, 'w', encoding='utf-8') as f:
        json.dump(list(processed_messages), f, ensure_ascii=False, indent=4)


processed_messages = load_processed_messages()


@app.on_message(filters.chat(CHANNELS))
async def handle_new_message(client, message):
    try:
        print("Ok")
        message_id = message.id
        chat_id = message.chat.username or message.chat.title

        if message_id in processed_messages:
            logger.info(f"Сообщение {message_id} из канала {chat_id} уже обработано.")
            return

        message_text = message.text or ""
        if not message_text.strip():
            logger.info(f"Сообщение {message_id} в канале {chat_id} пусто.")
            processed_messages.add(message_id)
            save_processed_messages(processed_messages)
            return

        if not is_relevant(message_text):
            logger.info(f"Сообщение {message_id} в канале {chat_id} не соответствует критериям фильтрации.")
            processed_messages.add(message_id)
            save_processed_messages(processed_messages)
            return

        if not check_with_openai(message_text):
            logger.info(f"Сообщение {message_id} в канале {chat_id} не прошло проверку через OpenAI.")
            processed_messages.add(message_id)
            save_processed_messages(processed_messages)
            return

        target_channel = TARGET_CHAT if TARGET_CHAT.startswith('@') else f"@{TARGET_CHAT}"
        await client.send_message(target_channel, message_text)
        logger.info(f"Сообщение {message_id} из канала {chat_id} переслано в {target_channel}.")

        processed_messages.add(message_id)
        save_processed_messages(processed_messages)

    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения: {e}")


if __name__ == "__main__":
    app.run()

