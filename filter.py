import re
from config import FILTER_WORDS

pattern = re.compile('|'.join(map(re.escape, FILTER_WORDS)))


def is_relevant(message_text: str) -> bool:
    """
    Проверяет, содержит ли сообщение хотя бы одну подстроку из FILTER_WORDS.

    :param message_text: Текст сообщения для проверки.
    :return: True, если найдено хотя бы одно совпадение, иначе False.
    """
    message_text = message_text.lower()

    return bool(pattern.search(message_text))
