import os
from app import app, db

def clean_database():
    print("Текущая директория:", os.getcwd())
    db_path = 'instance/recruiter.db'
    
    # Проверяем, существует ли файл
    if os.path.exists(db_path):
        print(f"Найдена база данных: {db_path}")
        try:
            # Удаляем файл
            os.remove(db_path)
            print("База данных успешно удалена")
        except Exception as e:
            print(f"Ошибка при удалении базы данных: {e}")
    else:
        print("База данных не найдена")
    
    # Создаем новую базу данных
    print("Создаем новую базу данных...")
    with app.app_context():
        db.drop_all()  # На всякий случай удаляем все таблицы
        db.create_all()  # Создаем новые таблицы
        print("Новая база данных успешно создана")

if __name__ == '__main__':
    clean_database() 