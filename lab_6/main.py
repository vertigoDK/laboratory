import sqlite3

def connect_db():
    """
    Создает подключение к базе данных SQLite.
    Возвращает объект подключения.
    """
    return sqlite3.connect('example.db')

def create_table(conn):
    """
    Создает таблицу 'notes', если она не существует.
    Использует переданное подключение.
    """
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT
            )
        ''')

def insert_record(conn, title, content):
    """
    Вставляет новую запись в таблицу 'notes'.
    Использует переданное подключение и параметры title и content.
    """
    with conn:
        conn.execute('''
            INSERT INTO notes (title, content) VALUES (?, ?)
        ''', (title, content))

def update_record(conn, note_id, title, content):
    """
    Обновляет запись в таблице 'notes' по заданному ID.
    Использует переданное подключение и параметры note_id, title и content.
    """
    with conn:
        conn.execute('''
            UPDATE notes SET title = ?, content = ? WHERE id = ?
        ''', (title, content, note_id))

def delete_record(conn, note_id):
    """
    Удаляет запись из таблицы 'notes' по заданному ID.
    Использует переданное подключение и параметр note_id.
    """
    with conn:
        conn.execute('''
            DELETE FROM notes WHERE id = ?
        ''', (note_id,))

def fetch_records(conn):
    """
    Извлекает все записи из таблицы 'notes'.
    Возвращает список кортежей с результатами.
    """
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, content FROM notes')
    return cursor.fetchall()

def main():
    """
    Основная функция для работы с приложением.
    Обеспечивает взаимодействие с пользователем через текстовый интерфейс.
    """
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
