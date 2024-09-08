# Установка библиотеки pydantic:
# pip install pydantic

from pydantic import BaseModel, ValidationError, EmailStr, constr
import sqlite3

# Определение модели данных для пользователя
class User(BaseModel):
    username: constr(min_length=3, max_length=50)  # Имя пользователя должно быть от 3 до 50 символов
    email: EmailStr  # Электронная почта должна быть в корректном формате
    age: int  # Возраст пользователя (целое число)

def connect_db():
    """Создает подключение к базе данных SQLite."""
    return sqlite3.connect('example.db')

def create_table(conn):
    """Создает таблицу 'users', если она не существует."""
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,         -- Уникальный идентификатор пользователя
                username TEXT NOT NULL,        -- Имя пользователя (не может быть пустым)
                email TEXT NOT NULL,           -- Электронная почта (не может быть пустым)
                age INTEGER NOT NULL           -- Возраст (не может быть пустым)
            )
        ''')

def insert_user(conn, user_data):
    """Вставляет нового пользователя в таблицу 'users'."""
    with conn:
        conn.execute('''
            INSERT INTO users (username, email, age) VALUES (?, ?, ?)
        ''', (user_data.username, user_data.email, user_data.age))

def validate_user_data(username, email, age):
    """Валидирует данные пользователя с использованием Pydantic."""
    try:
        user = User(username=username, email=email, age=age)
        return user
    except ValidationError as e:
        print(f"Validation error: {e}")
        return None

def main():
    conn = connect_db()  # Создаем подключение к базе данных
    create_table(conn)   # Создаем таблицу, если её нет

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
            conn.close()  # Закрываем подключение к базе данных
            break
        else:
            print('Некорректный выбор. Пожалуйста, попробуйте снова.')

if __name__ == '__main__':
    main()
