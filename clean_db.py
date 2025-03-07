import os
from app import app, db

def clean_database():
    print("Текущая директория:", os.getcwd())
    db_path = 'instance/recruiter.db'
    
    # Создаем новую базу данных
    print("Создаем новую базу данных...")
    with app.app_context():
        # Удаляем все таблицы
        db.drop_all()
        # Создаем новые таблицы
        db.create_all()
        print("Новая база данных успешно создана")

if __name__ == '__main__':
    clean_database() 