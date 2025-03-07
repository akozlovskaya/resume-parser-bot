# Pharos Recruiter

Telegram бот для автоматической обработки резюме с использованием искусственного интеллекта. Pharos помогает рекрутерам автоматизировать процесс обработки резюме, извлекая ключевую информацию и структурируя данные для удобного анализа.

## Требования

- Python 3.10 или 3.11 (рекомендуется Python 3.10.13)
- pip (менеджер пакетов Python)

> ⚠️ **Важно**: Python 3.13 и выше не поддерживается из-за несовместимости с некоторыми зависимостями проекта.

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
git clone https://github.com/akozlovskaya/resume-parser-bot.git
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

4. Установите языковую модель для spaCy:
```bash
python -m spacy download ru_core_news_sm
```

5. Создайте файл `.env` в корневой директории проекта и добавьте в него необходимые переменные окружения:
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
