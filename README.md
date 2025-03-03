# Resume Parser Bot

Telegram бот для автоматической обработки резюме с использованием искусственного интеллекта.

## Возможности

- Автоматическое извлечение информации из резюме (PDF, DOCX)
- Распознавание имени кандидата с помощью NLP
- Извлечение контактной информации (email, телефон)
- Определение специализации с помощью AI
- Сохранение информации в базу данных
- Веб-интерфейс для управления кандидатами и вакансиями

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-username/resume-parser-bot.git
cd resume-parser-bot
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate     # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` и добавьте необходимые переменные окружения:
```
TELEGRAM_BOT_TOKEN=your_bot_token
ALLOWED_TELEGRAM_USERNAMES=username1,username2
```

## Использование

1. Запустите веб-приложение:
```bash
python app.py
```

2. Запустите Telegram бота:
```bash
python telegram_bot.py
```

## Структура проекта

- `app.py` - Flask веб-приложение
- `telegram_bot.py` - Telegram бот
- `advanced_resume_parser.py` - Парсер резюме
- `models.py` - Модели базы данных
- `templates/` - HTML шаблоны
- `static/` - Статические файлы (CSS, JS)
- `resumes/` - Папка для хранения загруженных резюме
