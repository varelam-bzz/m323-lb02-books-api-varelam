"""Book blueprint"""

from flask import Blueprint, jsonify, request
from book_dao import BookDao
from book import Book

book_blueprint = Blueprint("book_blueprint", __name__)
book_dao = BookDao("books.db")


@book_blueprint.route("/books", methods=["GET"])
def get_all_books():
    """Retrieve all books."""
    books = book_dao.get_all_books()
    return jsonify([book.__dict__ for book in books]), 200


@book_blueprint.route("/books/<string:isbn>", methods=["GET"])
def get_book(isbn):
    """Retrieve a book by its ISBN."""
    book = book_dao.get_book(isbn)
    if book:
        return jsonify(book.__dict__), 200
    return jsonify({"message": "Book not found"}), 404


@book_blueprint.route("/books", methods=["POST"])
def add_book():
    """Add a new book."""
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
    """Update an existing book."""
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


def get_discount(isbn, discount):
    """Calculate the discounted price of a book."""
    book = book_dao.get_book(isbn)
    if not book:
        return jsonify({"message": "Book not found"}), 404

    discounted_price = book.price * (1 - discount / 100)
    return (
        jsonify(
            {
                "isbn": book.isbn,
                "title": book.title,
                "original_price": book.price,
                "discount": str(discount) + "%",
                "discounted_price": round(discounted_price, 2),
            }
        ),
        200,
    )


@book_blueprint.route("/books/discount/<string:isbn>/<int:discount>", methods=["GET"])
def apply_discount(isbn, discount):
    """Apply a discount to a book and return its new price."""
    return get_discount(isbn, discount)
