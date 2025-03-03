from app import app, db, Candidate, Vacancy

def check_database():
    with app.app_context():
        # Получаем информацию о таблицах
        inspector = db.inspect(db.engine)
        
        print("Структура таблицы 'candidate':")
        for column in inspector.get_columns('candidate'):
            print(f"- {column['name']}: {column['type']}")
        
        print("\nСтруктура таблицы 'vacancy':")
        for column in inspector.get_columns('vacancy'):
            print(f"- {column['name']}: {column['type']}")

if __name__ == '__main__':
    check_database() 