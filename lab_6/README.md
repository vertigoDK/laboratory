# Лабораторная работа №1: Программа для управления базой данных

## Цель работы
Создать консольное приложение для работы с базой данных SQLite, реализовав функции для создания таблицы, вставки, обновления, удаления записей, а также для поиска и вывода данных.

## ТЕОРЕТИЧЕСКАЯ ЧАСТЬ

### 1. SQLite
SQLite — легковесная реляционная база данных, хранящая данные в одном файле и не требующая установки серверного ПО. Интегрируется с Python через модуль `sqlite3`.

### 2. Основы работы с SQLite в Python
- **Подключение:** `conn = sqlite3.connect('example.db')`
- **Курсор:** `cursor = conn.cursor()`
- **Коммит транзакций:** `conn.commit()`
- **Закрытие соединения:** `conn.close()`

### 3. Основные SQL-операции
- **Создание таблицы:** `CREATE TABLE notes (id INTEGER PRIMARY KEY, title TEXT NOT NULL, content TEXT);`
- **Вставка данных:** `INSERT INTO notes (title, content) VALUES ('Sample Title', 'Sample Content');`
- **Обновление данных:** `UPDATE notes SET title = 'Updated Title' WHERE id = 1;`
- **Удаление данных:** `DELETE FROM notes WHERE id = 1;`
- **Выбор данных:** `SELECT * FROM notes;`

### 6. Выполнение SQL запросов
Используйте курсор для выполнения SQL-команд.

## ССЫЛКИ ДЛЯ ДАЛЬНЕЙШЕГО ОЗНАКОМЛЕНИЯ
- **На английском языке:**
  - [SQLite3 documentation](https://docs.python.org/3/library/sqlite3.html)
  - [SQL Tutorial](https://www.tutorialspoint.com/sql/index.htm)
  - [Шпаргалка по SQL](https://www.sqlitetutorial.net/sqlite-cheat-sheet/)
- **На русском языке:**
  - [SQLite3 документация](https://metanit.com/sql/sqlite/)
  - [Основные команды SQL](https://community.exolve.ru/blog/komandy-sql-i-zaprosy-s-primerami/)

## ПРАКТИЧЕСКАЯ ЧАСТЬ

### 1. Создание базы данных
Подключение к базе данных `example.db` и создание таблицы `notes`.

### 2. Реализация функции для работы с данными
- `insert_record()`: Вставка новых записей.
- `update_record()`: Обновление существующих записей.
- `delete_record()`: Удаление записей по идентификатору.
- `fetch_records()`: Извлечение всех записей и вывод на экран.

### 3. Создание пользовательского интерфейса
Реализация текстового интерфейса для работы с данными.

### 4. Тестирование приложения
Проверка функций приложения с различными командами и данными.

## КОД ЛАБОРАТОРНОЙ РАБОТЫ

```python
import sqlite3

def connect_db():
    """Создает подключение к базе данных SQLite."""
    return sqlite3.connect('example.db')

def create_table(conn):
    """Создает таблицу 'notes', если она не существует."""
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT
            )
        ''')

def insert_record(conn, title, content):
    """Вставляет новую запись в таблицу 'notes'."""
    with conn:
        conn.execute('''
            INSERT INTO notes (title, content) VALUES (?, ?)
        ''', (title, content))

def update_record(conn, note_id, title, content):
    """Обновляет запись в таблице 'notes' по заданному ID."""
    with conn:
        conn.execute('''
            UPDATE notes SET title = ?, content = ? WHERE id = ?
        ''', (title, content, note_id))

def delete_record(conn, note_id):
    """Удаляет запись из таблицы 'notes' по заданному ID."""
    with conn:
        conn.execute('''
            DELETE FROM notes WHERE id = ?
        ''', (note_id,))

def fetch_records(conn):
    """Извлекает все записи из таблицы 'notes'."""
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, content FROM notes')
    return cursor.fetchall()

def main():
    """Основная функция для работы с приложением."""
    conn = connect_db()
    create_table(conn)
    
    while True:
        print('1. Добавить заметку')
        print('2. Обновить заметку')
        print('3. Удалить заметку')
        print('4. Просмотреть заметки')
        print('5. Выход')
        choice = input('Введите ваш выбор: ')
        
        if choice == '1':
            title = input('Введите заголовок: ')
            content = input('Введите содержание: ')
            insert_record(conn, title, content)
        elif choice == '2':
            note_id = int(input('Введите ID заметки для обновления: '))
            title = input('Введите новый заголовок: ')
            content = input('Введите новое содержание: ')
            update_record(conn, note_id, title, content)
        elif choice == '3':
            note_id = int(input('Введите ID заметки для удаления: '))
            delete_record(conn, note_id)
        elif choice == '4':
            records = fetch_records(conn)
            for record in records:
                print(record)
        elif choice == '5':
            conn.close()
            break
        else:
            print('Некорректный выбор. Пожалуйста, попробуйте снова.')

if __name__ == '__main__':
    main()
