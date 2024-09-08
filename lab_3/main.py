from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Теоретическая часть:
# SQLAlchemy - это библиотека для работы с базами данных в Python, предоставляющая ORM (объектно-реляционное отображение).
# Основные компоненты SQLAlchemy:
# 1. Engine: соединение с базой данных.
# 2. Session: "сессия" для взаимодействия с базой данных.
# 3. Model (класс): описание таблицы базы данных в виде Python-класса.
# 4. Query: способ выполнения запросов к базе данных.

# Инициализация базы данных и модели
Base = declarative_base()

class User(Base):
    """Модель для таблицы пользователей в базе данных."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

# Подключение к базе данных SQLite
engine = create_engine('sqlite:///users.db')
Base.metadata.create_all(engine)

# Создание сессии для взаимодействия с базой данных
Session = sessionmaker(bind=engine)
session = Session()

def create_user(username, email, age):
    """Создает нового пользователя и добавляет его в базу данных."""
    new_user = User(username=username, email=email, age=age)
    session.add(new_user)
    session.commit()
    print(f'Пользователь {username} добавлен в базу данных.')

def get_all_users():
    """Получает всех пользователей из базы данных."""
    users = session.query(User).all()
    for user in users:
        print(f'ID: {user.id}, Имя: {user.username}, Email: {user.email}, Возраст: {user.age}')

def update_user(user_id, new_username=None, new_email=None, new_age=None):
    """Обновляет данные пользователя."""
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        if new_username:
            user.username = new_username
        if new_email:
            user.email = new_email
        if new_age is not None:
            user.age = new_age
        session.commit()
        print(f'Данные пользователя с ID {user_id} обновлены.')
    else:
        print(f'Пользователь с ID {user_id} не найден.')

def delete_user(user_id):
    """Удаляет пользователя из базы данных по его ID."""
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        session.delete(user)
        session.commit()
        print(f'Пользователь с ID {user_id} удален.')
    else:
        print(f'Пользователь с ID {user_id} не найден.')

def main():
    """Основное меню для работы с приложением."""
    while True:
        print('1. Добавить пользователя')
        print('2. Посмотреть всех пользователей')
        print('3. Обновить пользователя')
        print('4. Удалить пользователя')
        print('5. Выход')

        choice = input('Выберите действие: ')
        if choice == '1':
            username = input('Введите имя пользователя: ')
            email = input('Введите email пользователя: ')
            age = int(input('Введите возраст пользователя: '))
            create_user(username, email, age)
        elif choice == '2':
            get_all_users()
        elif choice == '3':
            user_id = int(input('Введите ID пользователя для обновления: '))
            new_username = input('Введите новое имя (оставьте пустым, если не хотите менять): ')
            new_email = input('Введите новый email (оставьте пустым, если не хотите менять): ')
            new_age = input('Введите новый возраст (оставьте пустым, если не хотите менять): ')
            update_user(user_id, new_username or None, new_email or None, int(new_age) if new_age else None)
        elif choice == '4':
            user_id = int(input('Введите ID пользователя для удаления: '))
            delete_user(user_id)
        elif choice == '5':
            break
        else:
            print('Неверный выбор. Попробуйте снова.')

if __name__ == '__main__':
    main()
