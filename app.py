from flask import Flask, request, jsonify, render_template
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from werkzeug.security import generate_password_hash, check_password_hash
from .models import books, users

app = Flask(__name__)
auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme='Bearer')

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
    return render_template('index.html')

# Halaman daftar buku
@app.route('/books', methods=['GET'])
@auth.login_required
def get_books():
    books = books.get_all_books()
    return render_template('books.html', books=books)

# Halaman detail buku
@app.route('/books/<int:book_id>', methods=['GET'])
@auth.login_required
def get_book(book_id):
    book = books.get_book_by_id(book_id)
    if book:
        return render_template('book.html', book=book)
    return 'Book not found', 404

# Endpoint untuk menambahkan buku baru
@app.route('/books', methods=['POST'])
@auth.login_required
def add_book():
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')

    if title and author:
        books.insert_book(title, author)
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
        book = books.get_book_by_id(book_id)
        if book:
            books.update_book(book_id, title, author)
            return 'Book updated successfully', 200
        return 'Book not found', 404
    return 'Invalid request', 400

# Endpoint untuk menghapus buku
@app.route('/books/<int:book_id>', methods=['DELETE'])
@auth.login_required
def remove_book(book_id):
    book = books.get_book_by_id(book_id)
    if book:
        books.delete_book(book_id)
        return 'Book deleted successfully', 200
    return 'Book not found', 404

# Endpoint untuk autentikasi dengan token
@app.route('/auth/token', methods=['POST'])
@auth.login_required
def get_auth_token():
    token = generate_token(auth.current_user())
    return jsonify({'token': token})

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
