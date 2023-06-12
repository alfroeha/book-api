import sqlite3

# Konfigurasi database SQLite
conn = sqlite3.connect('books.db')
cursor = conn.cursor()


# Fungsi untuk membuat tabel books
def create_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            judul TEXT NOT NULL,
            penulis TEXT NOT NULL,
            tahun terbit TEXT NOT NULL,
            penerbit TEXT NOT NULL,
        )
    ''')
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS users (id VARCHAR(255) PRIMARY KEY, username VARCHAR(50) UNIQUE, password VARCHAR(255))')
    conn.commit()
    conn.close()

# Fungsi untuk menambahkan buku baru ke database


def insert_book(title, author):
    conn = get_db()
    conn.execute(
        "INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
    conn.commit()
    conn.close()

# Fungsi untuk mengupdate buku berdasarkan ID


def update_book(book_id, title, author):
    conn = get_db()
    conn.execute("UPDATE books SET title = ?, author = ? WHERE id = ?",
                 (title, author, book_id))
    conn.commit()
    conn.close()

# Fungsi untuk menghapus buku berdasarkan ID


def delete_book(book_id):
    conn = get_db()
    conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()

# Fungsi untuk mendapatkan daftar semua buku


def get_all_books():
    conn = get_db()
    books = conn.execute("SELECT * FROM books").fetchall()
    conn.close()
    return books

# Fungsi untuk mendapatkan detail buku berdasarkan ID


def get_book_by_id(book_id):
    conn = get_db()
    book = conn.execute("SELECT * FROM books WHERE id = ?",
                        (book_id,)).fetchone()
    conn.close()
    return book
