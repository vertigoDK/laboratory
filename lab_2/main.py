# Установка библиотеки pydantic:
# pip install pydantic
import logging
import sqlite3
from pydantic import BaseModel, ValidationError, EmailStr, constr

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    logging.FileHandler('db_operations.log'),
    logging.StreamHandler()
])
logger = logging.getLogger(__name__)

class User(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr
    age: int

def connect_db():
    """Создает подключение к базе данных SQLite."""
    return sqlite3.connect('example.db')

def create_table(conn):
    """Создает таблицу 'users', если она не существует."""
    try:
        with conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL,
                    email TEXT NOT NULL,
                    age INTEGER NOT NULL
                )
            ''')
        logger.info('Таблица "users" создана или уже существует.')
    except Exception as e:
        logger.error(f'Ошибка при создании таблицы: {e}')

def insert_user(conn, user_data):
    """Вставляет нового пользователя в таблицу 'users'."""
    try:
        with conn:
            conn.execute('''
                INSERT INTO users (username, email, age) VALUES (?, ?, ?)
            ''', (user_data.username, user_data.email, user_data.age))
        logger.info(f'Пользователь добавлен: {user_data}')
    except Exception as e:
        logger.error(f'Ошибка при добавлении пользователя: {e}')

def validate_user_data(username, email, age):
    """Валидирует данные пользователя с использованием Pydantic."""
    try:
        user = User(username=username, email=email, age=age)
        return user
    except ValidationError as e:
        logger.error(f'Ошибка валидации данных: {e}')
        return None

def main():
    conn = connect_db()
    create_table(conn)

    while True:
        print('1. Добавить пользователя')
        print('2. Выход')
        choice = input('Введите ваш выбор: ')

        if choice == '1':
            username = input('Введите имя пользователя: ')
            email = input('Введите email: ')
            age = int(input('Введите возраст: '))

            user_data = validate_user_data(username, email, age)
            if user_data:
                insert_user(conn, user_data)
                print("Пользователь добавлен успешно.")
        elif choice == '2':
            conn.close()
            break
        else:
            print('Некорректный выбор. Пожалуйста, попробуйте снова.')

if __name__ == '__main__':
    main()
