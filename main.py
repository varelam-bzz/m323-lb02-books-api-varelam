"""Main file"""

from flask import Flask
from book import Book
from book_blueprint import book_blueprint
from book_dao import BookDao

app = Flask(__name__)
app.secret_key = "my_secret_key"

app.register_blueprint(book_blueprint)


def generate_testdata():
    """Generates necessary testdata"""
    book_dao = BookDao("books.db")

    book_dao.create_table()

    book_dao.add_book(
        Book(
            isbn="9781401232565",
            title="Batman: Year One",
            author="Frank Miller",
            published_year=1987,
            price=19.99,
            genre=["Action", "Crime", "Superhero"],
        )
    )
    book_dao.add_book(
        Book(
            isbn="9781401285516",
            title="Batman: The Killing Joke",
            author="Alan Moore",
            published_year=1988,
            price=17.99,
            genre=["Action", "Psychological", "Superhero"],
        )
    )
    book_dao.add_book(
        Book(
            isbn="9780785121792",
            title="Spider-Man: Blue",
            author="Jeph Loeb",
            published_year=2002,
            price=24.99,
            genre=["Action", "Romance", "Superhero"],
        )
    )
    book_dao.add_book(
        Book(
            isbn="9781401207529",
            title="Superman: Red Son",
            author="Mark Millar",
            published_year=2003,
            price=21.99,
            genre=["Action", "Alternate Universe", "Superhero"],
        )
    )
    book_dao.add_book(
        Book(
            isbn="9781401263112",
            title="Wonder Woman: The Hiketeia",
            author="Greg Rucka",
            published_year=2002,
            price=14.99,
            genre=["Action", "Mythology", "Superhero"],
        )
    )

    book_dao.close()


if __name__ == "__main__":
    generate_testdata()
    app.run(debug=True)
