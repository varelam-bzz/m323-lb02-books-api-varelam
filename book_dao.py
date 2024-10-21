"""Book Data Access Object"""

import sqlite3
from book import Book


class BookDao:
    """Data Access Object for managing book data in the database."""

    def __init__(self, db_file):
        """Initialize the DAO with the database file."""
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_table(self):
        """Create the books table in the database."""
        self.cursor.execute("""DROP TABLE IF EXISTS books""")
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS books (
                isbn TEXT PRIMARY KEY,
                title TEXT,
                author TEXT,
                published_year INTEGER,
                price REAL,
                genre TEXT
            )"""
        )
        self.conn.commit()

    def add_book(self, book: Book):
        """Insert a new book into the database."""
        self.cursor.execute(
            "INSERT INTO books (isbn, title, author, "
            "published_year, price, genre) VALUES (?, ?, ?, ?, ?, ?)",
            (book.isbn, book.title, book.author,
             book.published_year, book.price, ",".join(book.genre))
        )
        self.conn.commit()

    def get_book(self, isbn: str):
        """Retrieve a book from the database by its ISBN."""
        self.cursor.execute("SELECT * FROM books WHERE isbn = ?", (isbn,))
        row = self.cursor.fetchone()
        if row:
            return Book(
                isbn=row[0],
                title=row[1],
                author=row[2],
                published_year=row[3],
                price=row[4],
                genre=row[5].split(","),
            )
        return None

    def get_all_books(self):
        """Retrieve all books from the database."""
        self.cursor.execute("SELECT * FROM books")
        rows = self.cursor.fetchall()
        return [
            Book(
                isbn=row[0],
                title=row[1],
                author=row[2],
                published_year=row[3],
                price=row[4],
                genre=row[5].split(","),
            )
            for row in rows
        ]

    def update_book(self, book: Book):
        """Update an existing book in the database."""
        self.cursor.execute(
            "UPDATE books SET title = ?, author = ?, "
            "published_year = ?, price = ?, genre = ? WHERE isbn = ?",
            (
                book.title,
                book.author,
                book.published_year,
                book.price,
                ",".join(book.genre),
                book.isbn,
            ),
        )
        if self.cursor.rowcount > 0:
            self.conn.commit()
            return True
        return False

    def delete_book(self, isbn: str):
        """Delete a book from the database by its ISBN."""
        self.cursor.execute("DELETE FROM books WHERE isbn = ?", (isbn,))
        if self.cursor.rowcount > 0:
            self.conn.commit()
            return True
        return False

    def close(self):
        """Close the database connection."""
        self.conn.close()
