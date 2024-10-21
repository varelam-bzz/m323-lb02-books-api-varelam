from flask import Blueprint, jsonify, request
from book_dao import BookDao
from book import Book

book_blueprint = Blueprint("book_blueprint", __name__)
book_dao = BookDao("books.db")


@book_blueprint.route("/books", methods=["GET"])
def get_all_books():
    books = book_dao.get_all_books()
    return jsonify([book.__dict__ for book in books]), 200


@book_blueprint.route("/books/<string:isbn>", methods=["GET"])
def get_book(isbn):
    book = book_dao.get_book(isbn)
    if book:
        return jsonify(book.__dict__), 200
    else:
        return jsonify({"message": "Book not found"}), 404


@book_blueprint.route("/books", methods=["POST"])
def add_book():
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
    else:
        return jsonify({"message": "Book not found or not updated"}), 404


@book_blueprint.route("/books/<string:isbn>", methods=["DELETE"])
def delete_book(isbn):
    if book_dao.delete_book(isbn):
        return jsonify({"message": "Book deleted"}), 200
    else:
        return jsonify({"message": "Book not found or not deleted"}), 404
