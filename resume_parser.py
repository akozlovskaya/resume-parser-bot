import re
import spacy
import phonenumbers
import docx
import PyPDF2
import magic
import os

class ResumeParser:
    def __init__(self):
        # Загружаем модель русского языка для NLP
        self.nlp = spacy.load("ru_core_news_sm")
        
        # Регулярные выражения для поиска email и специализаций
        self.email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        
        # Словарь специализаций и ключевых слов
        self.specializations = {
            'QA': ['qa', 'quality assurance', 'тестировщик', 'тестирование', 'qc', 'quality control'],
            'Python': ['python', 'django', 'flask', 'fastapi', 'pytest'],
            'Java': ['java', 'spring', 'hibernate', 'maven'],
            'Frontend': ['javascript', 'react', 'vue', 'angular', 'frontend', 'фронтенд'],
            'Backend': ['backend', 'бэкенд', 'node.js', 'php', 'ruby'],
            'DevOps': ['devops', 'docker', 'kubernetes', 'ci/cd', 'jenkins'],
            'Android': ['android', 'kotlin', 'mobile'],
            'iOS': ['ios', 'swift', 'objective-c'],
        }

    def extract_text_from_pdf(self, file_path):
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        except Exception as e:
            print(f"Ошибка при чтении PDF: {e}")
        return text

    def extract_text_from_docx(self, file_path):
        text = ""
        try:
            doc = docx.Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            print(f"Ошибка при чтении DOCX: {e}")
        return text

    def extract_text(self, file_path):
        # Определяем тип файла по расширению
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif file_extension in ['.doc', '.docx']:
            return self.extract_text_from_docx(file_path)
        return ""

    def extract_phone_numbers(self, text):
        phones = []
        # Ищем телефонные номера в тексте
        for match in phonenumbers.PhoneNumberMatcher(text, "RU"):
            phone = phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            phones.append(phone)
        return phones[0] if phones else None

    def extract_email(self, text):
        emails = re.findall(self.email_pattern, text)
        return emails[0] if emails else None

    def extract_name(self, text):
        # Берем первые два слова из текста, которые похожи на имя и фамилию
        doc = self.nlp(text[:1000])  # Ограничиваем анализ первой 1000 символов
        for ent in doc.ents:
            if ent.label_ == "PER":  # Если найдено имя персоны
                return ent.text
        # Если не нашли через NER, берем первые слова из документа
        words = text.split()
        if len(words) >= 2:
            return " ".join(words[:2])
        return None

    def extract_specialization(self, text):
        text_lower = text.lower()
        found_specs = []
        
        for spec, keywords in self.specializations.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    found_specs.append(spec)
                    break
        
        return list(set(found_specs))  # Убираем дубликаты

    def parse_resume(self, file_path):
        text = self.extract_text(file_path)
        if not text:
            return None

        return {
            'name': self.extract_name(text),
            'email': self.extract_email(text),
            'phone': self.extract_phone_numbers(text),
            'specializations': self.extract_specialization(text)
        } 