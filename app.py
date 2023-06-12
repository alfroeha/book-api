from flask import Flask, jsonify, request, render_template, g, redirect, url_for
import sqlite3

app = Flask(__name__)
app.config['DATABASE'] = 'books.db'

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
@app.route('/books', methods=['POST'])
def create_book():
    data = request.form
    if 'title' not in data or 'author' not in data or 'year' not in data or 'publisher' not in data:
        return jsonify({'message': 'Missing required fields'}), 400

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


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
