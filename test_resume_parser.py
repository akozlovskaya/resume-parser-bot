import sys
import os
from advanced_resume_parser import AdvancedResumeParser
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_extract_text(parser, file_path):
    """Тестирование извлечения текста из файла"""
    logger.info(f"Тестирование извлечения текста из файла: {file_path}")
    try:
        text = parser.extract_text(file_path)
        logger.info("Текст успешно извлечен")
        logger.info("Первые 500 символов текста:")
        logger.info("-" * 50)
        logger.info(text[:500])
        return text
    except Exception as e:
        logger.error(f"Ошибка при извлечении текста: {e}")
        return None

def test_extract_name(parser, text):
    """Тестирование извлечения имени"""
    logger.info("Тестирование извлечения имени")
    try:
        name = parser.extract_name(text)
        logger.info(f"Извлеченное имя: {name}")
        return name
    except Exception as e:
        logger.error(f"Ошибка при извлечении имени: {e}")
        return None

def test_extract_email(parser, text):
    """Тестирование извлечения email"""
    logger.info("Тестирование извлечения email")
    try:
        email = parser.extract_email(text)
        logger.info(f"Извлеченный email: {email}")
        return email
    except Exception as e:
        logger.error(f"Ошибка при извлечении email: {e}")
        return None

def test_extract_phone(parser, text):
    """Тестирование извлечения телефона"""
    logger.info("Тестирование извлечения телефона")
    try:
        phone = parser.extract_phone_numbers(text)
        logger.info(f"Извлеченный телефон: {phone}")
        return phone
    except Exception as e:
        logger.error(f"Ошибка при извлечении телефона: {e}")
        return None

def test_extract_specialization(parser, text):
    """Тестирование извлечения специализаций"""
    logger.info("Тестирование извлечения специализаций")
    try:
        specs = parser.extract_specialization(text)
        logger.info("Извлеченные специализации:")
        for spec in specs:
            logger.info(f"- {spec}")
        return specs
    except Exception as e:
        logger.error(f"Ошибка при извлечении специализаций: {e}")
        return None

def analyze_resume(file_path):
    """Полный анализ резюме"""
    logger.info(f"Начало анализа резюме: {file_path}")
    
    # Инициализация парсера
    parser = AdvancedResumeParser()
    
    # Извлекаем текст
    text = test_extract_text(parser, file_path)
    if not text:
        logger.error("Не удалось извлечь текст из резюме")
        return
    
    # Извлекаем данные
    name = test_extract_name(parser, text)
    email = test_extract_email(parser, text)
    phone = test_extract_phone(parser, text)
    specs = test_extract_specialization(parser, text)
    
    # Выводим итоговый результат
    logger.info("\nИтоговые результаты анализа резюме:")
    logger.info("-" * 50)
    logger.info(f"Имя: {name}")
    logger.info(f"Email: {email}")
    logger.info(f"Телефон: {phone}")
    logger.info("Специализации:")
    for spec in specs or []:
        logger.info(f"- {spec}")

def main():
    """Основная функция для запуска тестов"""
    if len(sys.argv) != 2:
        print("Использование: python test_resume_parser.py <путь_к_файлу_резюме>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        logger.error(f"Файл не найден: {file_path}")
        sys.exit(1)
    
    analyze_resume(file_path)

if __name__ == "__main__":
    main() 