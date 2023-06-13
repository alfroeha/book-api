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

'''endpoint init_db()'''
@app.route('/create-db')
def create_db():
    init_db()
    return jsonify({'message': 'Database created'})

# Create a new book
@app.route('/add-books', methods=['POST'])
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
 
    
    return redirect(url_for('get_all_books'))

# Home route - Display the form
@app.route('/books', methods=['GET','POST'])
def insert_book():
    return render_template('form.html')

# Retrieve all books
@app.route('/', methods=['GET'])
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
            'publisher': book['publisher'],
            'update_url': url_for('update_book_form', book_id=book['id']),
            'delete_url': url_for('delete_book', book_id=book['id'])
        }
        book_list.append(book_dict)

    return render_template('books.html', books=book_list)


# Retrieve a specific book
@app.route('/books/<int:book_id>/', methods=['GET'])
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

    #return redirect(url_for('get_all_books'))

    return jsonify(book_dict)

# update book
@app.route('/books/<int:book_id>/update/', methods=['GET','POST', 'PUT'])
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

# Delete a book ketika menggunakan web
@app.route('/books/<int:book_id>/delete', methods=['POST', 'DELETE'])
def delete_book(book_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    book = cursor.fetchone()

    if book is None:
        return jsonify({'message': 'Book not found'}), 404

    if request.method == 'POST' or (request.method == 'DELETE' and request.form.get('_method') == 'DELETE'):
        cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
        conn.commit()
        return redirect(url_for('get_all_books'))

    return jsonify({'message': 'Invalid request method'}), 405
'''


if __name__ == '__main__':
    init_db()
    app.run(debug=True)

