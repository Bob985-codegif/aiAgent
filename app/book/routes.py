from flask import render_template, request, jsonify, redirect, url_for
from app.book import book_bp
from app.book.models import Book, db
from datetime import datetime


@book_bp.route('/books')
def books():
    """图书列表页面"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    books = Book.query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('book/books.html', books=books)


@book_bp.route('/books/add', methods=['GET', 'POST'])
def add_book():
    """添加图书"""
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        publication_date = request.form['publication_date']
        publisher = request.form['publisher']
        
        new_book = Book(
            title=title,
            author=author,
            isbn=isbn,
            publication_date=datetime.strptime(publication_date, '%Y-%m-%d') if publication_date else None,
            publisher=publisher,
            created_at=datetime.now()
        )
        
        db.session.add(new_book)
        db.session.commit()
        
        return redirect(url_for('book.books'))
    
    return render_template('book/add_book.html')


@book_bp.route('/books/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    """编辑图书"""
    book = Book.query.get_or_404(book_id)
    
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.isbn = request.form['isbn']
        book.publication_date = datetime.strptime(request.form['publication_date'], '%Y-%m-%d') if request.form['publication_date'] else None
        book.publisher = request.form['publisher']
        book.updated_at = datetime.now()
        
        db.session.commit()
        
        return redirect(url_for('book.books'))
    
    return render_template('book/edit_book.html', book=book)


@book_bp.route('/books/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    """删除图书"""
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    
    return jsonify({'success': True})


@book_bp.route('/api/books/search')
def search_books():
    """搜索图书API"""
    query = request.args.get('q', '')
    books = Book.query.filter(Book.title.contains(query) | Book.author.contains(query)).all()
    return jsonify([{
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'isbn': book.isbn
    } for book in books])