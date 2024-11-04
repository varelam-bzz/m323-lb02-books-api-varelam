"""Book blueprint"""
from functools import reduce
from flask import Blueprint, jsonify, request
from book_dao import BookDao
from book import Book
from utils import get_book_response, get_discounted_book_info, filter_and_sort_books_by_price_range

book_blueprint = Blueprint("book_blueprint", __name__)
book_dao = BookDao("books.db")

@book_blueprint.route("/books", methods=["GET"])
def get_all_books():
    """Retrieve and return all books."""
    books = book_dao.get_all_books()
    return jsonify([get_book_response(book) for book in books]), 200

@book_blueprint.route("/books/<string:isbn>", methods=["GET"])
def get_book(isbn):
    """Retrieve a single book by its ISBN."""
    book = book_dao.get_book(isbn)
    if book:
        return jsonify(get_book_response(book)), 200
    return jsonify({"message": "Book not found"}), 404

@book_blueprint.route("/books", methods=["POST"])
def add_book():
    """Add a new book based on provided JSON data."""
    data = request.get_json()
    new_book = Book(
        isbn=data["isbn"],
        title=data["title"],
        author=data["author"],
        published_year=data["published_year"],
        price=data["price"],
        genre=data["genre"],
    )
    book_dao.add_book(new_book)
    return jsonify({"message": "Book created"}), 201

@book_blueprint.route("/books/<string:isbn>", methods=["PUT"])
def update_book(isbn):
    """Update an existing book based on provided JSON data."""
    data = request.get_json()
    updated_book = Book(
        isbn=isbn,
        title=data["title"],
        author=data["author"],
        published_year=data["published_year"],
        price=data["price"],
        genre=data["genre"],
    )
    if book_dao.update_book(updated_book):
        return jsonify({"message": "Book updated"}), 200
    return jsonify({"message": "Book not found or not updated"}), 404

@book_blueprint.route("/books/<string:isbn>", methods=["DELETE"])
def delete_book(isbn):
    """Delete a book by its ISBN."""
    if book_dao.delete_book(isbn):
        return jsonify({"message": "Book deleted"}), 200
    return jsonify({"message": "Book not found or not deleted"}), 404

@book_blueprint.route("/books/discount/<string:isbn>/<int:discount_percentage>", methods=["GET"])
def apply_discount(isbn, discount_percentage):
    """Apply a discount to a book and return detailed pricing info."""
    book = book_dao.get_book(isbn)
    if not book:
        return jsonify({"message": "Book not found"}), 404
    return jsonify(get_discounted_book_info(book, discount_percentage)), 200

@book_blueprint.route("/books/sorted-by-price", methods=["GET"])
def get_sorted_books():
    """Retrieve all books sorted by price and title in ascending order."""
    books = book_dao.get_all_books()
    sorted_books = sorted(books, key=lambda book: (book.price, book.title))
    return jsonify([get_book_response(book) for book in sorted_books]), 200

@book_blueprint.route("/books/genre_price/<string:genre>", methods=["GET"])
def get_genre_price(genre):
    """Calculate and return the total price of all books in a specified genre."""
    books = book_dao.get_all_books()
    filtered_books = filter(lambda book: genre.lower() in [g.lower() for g in book.genre], books)
    total_price = reduce(lambda acc, book: acc + book.price, filtered_books, 0)
    return jsonify({"genre": genre, "total_price": round(total_price, 2)}), 200

@book_blueprint.route("/books/discounted/<int:discount_percentage>", methods=["GET"])
def get_discounted_books(discount_percentage):
    """Return a list of all books with an applied discount."""
    def discount_closure(percentage):
        def apply_discount_inner(price):
            return price * (1 - percentage / 100)
        return apply_discount_inner

    applied_discount = discount_closure(discount_percentage)
    books = book_dao.get_all_books()
    discounted_books = [
        {
            "isbn": book.isbn,
            "title": book.title,
            "original_price": book.price,
            "discounted_price": round(applied_discount(book.price), 2),
        }
        for book in books
    ]
    return jsonify(discounted_books), 200

@book_blueprint.route("/books/filter_sort/<int:min_price>/<int:max_price>", methods=["GET"])
def get_filtered_sorted_books(min_price, max_price):
    """Retrieve books within a specified price range and return them sorted by price."""
    books = book_dao.get_all_books()
    sorted_books = filter_and_sort_books_by_price_range(books, min_price, max_price)
    return jsonify([get_book_response(book) for book in sorted_books]), 200
