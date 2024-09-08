# Шифрование данных в базе данных

**Цель работы:** Реализовать хранение чувствительных данных (например, паролей) в зашифрованном виде в базе данных с использованием библиотеки `cryptography`.

### Теоретическая часть

Хранение чувствительных данных, таких как пароли, в зашифрованном виде необходимо для обеспечения безопасности. Вместо хранения пароля в открытом виде, применяется хеширование и шифрование данных.

**Основные методы защиты данных:**

- **Хеширование:** Это односторонняя операция, которая преобразует данные в строку фиксированной длины. Популярные алгоритмы: SHA-256, bcrypt, scrypt. Обычно используется для паролей.
- **Шифрование:** Это обратимая операция, которая позволяет зашифровать данные и расшифровать их при необходимости.

Мы будем использовать библиотеку `cryptography` для симметричного шифрования данных с использованием алгоритма AES.

### Практическая часть

1. **Установка библиотеки для шифрования:**

Установите библиотеку `cryptography`:

    ```bash
    pip install cryptography
    ```

2. **Шифрование и расшифровка данных:**

Шифрование данных будет реализовано с помощью симметричного ключа. Этот ключ будет использоваться как для шифрования, так и для расшифровки данных.

3. **Реализация шифрования:**

Мы будем шифровать пароли пользователей перед их сохранением в базу данных и расшифровывать при необходимости.

### Пример реализации

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from cryptography.fernet import Fernet

# Генерация ключа для шифрования
key = Fernet.generate_key()
cipher_suite = Fernet(key)

Base = declarative_base()

class User(Base):
    """Модель для таблицы пользователей с зашифрованными паролями."""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)  # Храним зашифрованный пароль

# Подключение к базе данных SQLite
engine = create_engine('sqlite:///secure_users.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def encrypt_password(password):
    """Шифрует пароль."""
    encrypted_password = cipher_suite.encrypt(password.encode())
    return encrypted_password

def decrypt_password(encrypted_password):
    """Расшифровывает пароль."""
    decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
    return decrypted_password

def create_user(username, email, password):
    """Создает нового пользователя с зашифрованным паролем."""
    encrypted_password = encrypt_password(password)
    new_user = User(username=username, email=email, password=encrypted_password)
    session.add(new_user)
    session.commit()
    print(f'Пользователь {username} добавлен в базу данных.')

def get_all_users():
    """Получает всех пользователей из базы данных."""
    users = session.query(User).all()
    for user in users:
        decrypted_password = decrypt_password(user.password.encode())
        print(f'ID: {user.id}, Имя: {user.username}, Email: {user.email}, Пароль: {decrypted_password}')

# Пример работы с пользователями
create_user('Alice', 'alice@example.com', 'mysecretpassword')
get_all_users()
