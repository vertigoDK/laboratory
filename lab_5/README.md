# Тестирование базы данных с использованием pytest

**Цель работы:** Написать тесты для CRUD-операций с базой данных, используя библиотеку pytest.

### Теоретическая часть

**pytest** — это популярная библиотека для тестирования в Python. Она упрощает написание и запуск тестов, поддерживая как простые, так и сложные сценарии тестирования.

**Тестирование CRUD-операций:**
Тестирование баз данных включает проверку правильности выполнения всех CRUD-операций (создание, чтение, обновление и удаление). Мы также будем проверять, что данные сохраняются в зашифрованном виде.

### Практическая часть

1. **Установка pytest:**
Установите pytest для выполнения тестов:

    ```bash
    pip install pytest
    ```

2. **Создание фикстур для тестов:**
Фикстуры позволяют инициализировать базу данных для тестов и сбрасывать её состояние после завершения тестов.

3. **Написание тестов для CRUD-операций:**
Напишите тесты для проверки операций создания, чтения, обновления и удаления данных в базе данных.

### Пример тестов с использованием pytest

Создайте файл `test_myapp.py` с содержимым:

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from cryptography.fernet import Fernet
from myapp import Base, User, encrypt_password, decrypt_password

# Инициализация ключа шифрования и движка базы данных
key = Fernet.generate_key()
cipher_suite = Fernet(key)

@pytest.fixture(scope='function')
def db_session():
    """Фикстура для создания и сброса базы данных для каждого теста."""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_create_user(db_session):
    """Тест создания пользователя."""
    encrypted_password = encrypt_password('mypassword')
    user = User(username='TestUser', email='test@example.com', password=encrypted_password)
    db_session.add(user)
    db_session.commit()

    saved_user = db_session.query(User).filter_by(username='TestUser').first()
    assert saved_user is not None
    assert decrypt_password(saved_user.password.encode()) == 'mypassword'

def test_read_user(db_session):
    """Тест чтения данных пользователя."""
    encrypted_password = encrypt_password('testpassword')
    user = User(username='ReadUser', email='read@example.com', password=encrypted_password)
    db_session.add(user)
    db_session.commit()

    retrieved_user = db_session.query(User).filter_by(username='ReadUser').first()
    assert retrieved_user is not None
    assert decrypt_password(retrieved_user.password.encode()) == 'testpassword'

def test_update_user(db_session):
    """Тест обновления пользователя."""
    user = User(username='UpdateUser', email='update@example.com', password=encrypt_password('oldpassword'))
    db_session.add(user)
    db_session.commit()

    user.email = 'new_email@example.com'
    user.password = encrypt_password('newpassword')
    db_session.commit()

    updated_user = db_session.query(User).filter_by(username='UpdateUser').first()
    assert updated_user.email == 'new_email@example.com'
    assert decrypt_password(updated_user.password.encode()) == 'newpassword'

def test_delete_user(db_session):
    """Тест удаления пользователя."""
    user = User(username='DeleteUser', email='delete@example.com', password=encrypt_password('deletepassword'))
    db_session.add(user)
    db_session.commit()

    db_session.delete(user)
    db_session.commit()

    deleted_user = db_session.query(User).filter_by(username='DeleteUser').first()
    assert deleted_user is None
