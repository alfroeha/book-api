# Konfigurasi database SQLite
DATABASE = 'books.db'

# Fungsi untuk membuat koneksi ke database
def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

# Fungsi untuk membuat tabel books
def create_table():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Fungsi untuk menambahkan buku baru ke database
def insert_book(title, author):
    conn = get_db()
    conn.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
    conn.commit()
    conn.close()

# Fungsi untuk mengupdate buku berdasarkan ID
def update_book(book_id, title, author):
    conn = get_db()
    conn.execute("UPDATE books SET title = ?, author = ? WHERE id = ?", (title, author, book_id))
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
    book = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    conn.close()
    return book