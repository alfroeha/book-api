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
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
        )
    ''')
    conn.commit()
    conn.close()
