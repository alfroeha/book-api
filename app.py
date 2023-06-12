<<<<<<< HEAD
from flask import Flask, request, jsonify, render_template
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from werkzeug.security import generate_password_hash, check_password_hash
from . import models
=======
from flask import Flask, jsonify, request, render_template, g, redirect, url_for
import sqlite3
>>>>>>> 7389cda2ae609a41546f8f734d4aea440ac398a0

app = Flask(__name__)
app.config['DATABASE'] = 'books.db'

<<<<<<< HEAD
# Fungsi untuk menghasilkan token berdasarkan username dan password


def generate_token(username):
    return username + '_token'

# Fungsi untuk verifikasi token


def verify_token(token):
    return token.endswith('_token')

# Fungsi untuk menghasilkan response saat autentikasi gagal


@auth.error_handler
def unauthorized():
    return jsonify({'error': 'Unauthorized access'}), 401

# Fungsi untuk memverifikasi username dan password


@auth.verify_password
def verify_password(username, password):
    # Ganti kode ini dengan logika autentikasi yang sesuai, misalnya mengambil data pengguna dari database
    if username == 'admin' and password == 'password':
        return username

# Fungsi untuk memverifikasi token


@token_auth.verify_token
def verify_token(token):
    return verify_token(token)

# Halaman utama


@app.route('/')
def home():
    return render_template('books.html')

# Halaman daftar buku


@app.route('/books', methods=['GET'])
@auth.login_required
def get_books():
    books = models.get_all_books()
    return render_template('books.html', books=books)

# Halaman detail buku


@app.route('/books/<int:book_id>', methods=['GET'])
@auth.login_required
def get_book(book_id):
    book = models.get_book_by_id(book_id)
    if book:
        return render_template('book.html', book=book)
    return 'Book not found', 404

# Endpoint untuk menambahkan buku baru


=======
# Function to get the SQLite database connection
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

# Initialize the database and create the books table if it doesn't exist
def init_db():
    with app.app_context():
        conn = get_db()
        cursor = conn.cursor()

        # Create the books table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year TEXT NOT NULL,
                publisher TEXT NOT NULL
            )
        ''')

        conn.commit()

# Create a new book
>>>>>>> 7389cda2ae609a41546f8f734d4aea440ac398a0
@app.route('/books', methods=['POST'])
def create_book():
    data = request.form
    if 'title' not in data or 'author' not in data or 'year' not in data or 'publisher' not in data:
        return jsonify({'message': 'Missing required fields'}), 400

<<<<<<< HEAD
    if title and author:
        models.insert_book(title, author)
        return 'Book added successfully', 201
    return 'Invalid request', 400

# Endpoint untuk mengupdate buku


@app.route('/books/<int:book_id>', methods=['PUT'])
@auth.login_required
def update_book(book_id):
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')

    if title and author:
        book = models.get_book_by_id(book_id)
        if book:
            models.update_book(book_id, title, author)
            return 'Book updated successfully', 200
        return 'Book not found', 404
    return 'Invalid request', 400

# Endpoint untuk menghapus buku


@app.route('/books/<int:book_id>', methods=['DELETE'])
@auth.login_required
def remove_book(book_id):
    book = models.get_book_by_id(book_id)
    if book:
        models.delete_book(book_id)
        return 'Book deleted successfully', 200
    return 'Book not found', 404

# Endpoint untuk autentikasi dengan token


@app.route('/auth/token', methods=['POST'])
@auth.login_required
def get_auth_token():
    token = generate_token(auth.current_user())
    return jsonify({'token': token})
=======
    title = data['title']
    author = data['author']
    year = data['year']
    publisher = data['publisher']

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO books (title, author, year, publisher) VALUES (?, ?, ?, ?)',
                   (title, author, year, publisher))
    conn.commit()
    book_id = cursor.lastrowid

    return jsonify({'id': book_id, 'title': title, 'author': author, 'year': year, 'publisher': publisher}), 201

# Home route - Display the form
@app.route('/', methods=['GET','POST'])
def home():
    return render_template('form.html')

# Retrieve all books
@app.route('/books', methods=['GET'])
def get_all_books():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()

    book_list = []
    for book in books:
        book_dict = {
            'id': book['id'],
            'title': book['title'],
            'author': book['author'],
            'year': book['year'],
            'publisher': book['publisher']
        }
        book_list.append(book_dict)

    return jsonify({'books': book_list})


# Retrieve a specific book
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    book = cursor.fetchone()

    if book is None:
        return jsonify({'message': 'Book not found'}), 404

    book_dict = {
        'id': book['id'],
        'title': book['title'],
        'author': book['author'],
        'year': book['year'],
        'publisher': book['publisher']
    }

    return jsonify(book_dict)

@app.route('/books/<int:book_id>/update', methods=['GET','POST', 'PUT'])
def update_book_form(book_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    book = cursor.fetchone()

    if book is None:
        return jsonify({'message': 'Book not found'}), 404
    
    if request.method=='GET':
        return render_template('update.html',book=book)

    elif request.method == 'POST' or request.method == 'PUT':
        data = request.form
        if 'title' not in data or 'author' not in data or 'year' not in data or 'publisher' not in data:
            return jsonify({'message': 'Missing required fields'}), 400

        title = data['title']
        author = data['author']
        year = data['year']
        publisher = data['publisher']
        try:
            conn = sqlite3.connect('books.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE books SET title=?, author=?, year=?, publisher=? WHERE id=?',
                           (title, author, year, publisher, book_id))
            conn.commit()
            conn.close()
        except sqlite3.Error as error:
            return jsonify({'message': 'Error updating book: {}'.format(str(error))}), 500

        return jsonify({'message': 'Book updated successfully'})

    else:
        return jsonify({'message': 'Invalid request method'}), 405


# Delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()

    return jsonify({'message': 'Book deleted successfully'})

>>>>>>> 7389cda2ae609a41546f8f734d4aea440ac398a0


if __name__ == '__main__':
<<<<<<< HEAD
    models.create_table()
=======
    init_db()
>>>>>>> 7389cda2ae609a41546f8f734d4aea440ac398a0
    app.run(debug=True)
