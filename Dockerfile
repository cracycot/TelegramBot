FROM python:3.11-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем все файлы проекта в контейнер
COPY . .

# Устанавливаем зависимости из requirements.txt
# Предполагается, что вы создадите файл requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Указываем переменные окружения для OpenAI и Telegram
ENV OPENAI_API_KEY="your-openai-api-key"
ENV API_ID="your-telegram-api-id"
ENV API_HASH="your-telegram-api-hash"
ENV TOKEN=""
ENV PHONE_NUMBER=""
ENV CHANNELS="archi_ru,ArchHunter,haltura_arhitetura,archivajno,urbanjob,wasa_job,nevolk_vacancies,elenpudova,ARCHITIME_RU,test1234590"
# Указываем, какой файл запускается по умолчанию
CMD ["python", "main.py"]