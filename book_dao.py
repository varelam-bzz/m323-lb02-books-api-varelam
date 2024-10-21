"""Book Data Access Object"""
import sqlite3
from book import Book

class BookDao:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_table(self):
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
        # Insert a new book into the database
        self.cursor.execute(
            "INSERT INTO books (isbn, title, author, published_year, price, genre) VALUES (?, ?, ?, ?, ?, ?)",
            (book.isbn, book.title, book.author, book.published_year, book.price, ",".join(book.genre))
        )
        self.conn.commit()

    def get_book(self, isbn: str):
        self.cursor.execute("SELECT * FROM books WHERE isbn = ?", (isbn,))
        row = self.cursor.fetchone()
        if row:
            return Book(
                isbn=row[0],
                title=row[1],
                author=row[2],
                published_year=row[3],
                price=row[4],
                genre=row[5].split(',')
            )
        return None

    def get_all_books(self):
        self.cursor.execute("SELECT * FROM books")
        rows = self.cursor.fetchall()
        return [
            Book(
                isbn=row[0],
                title=row[1],
                author=row[2],
                published_year=row[3],
                price=row[4],
                genre=row[5].split(',')
            )
            for row in rows
        ]

    def update_book(self, book: Book):
        self.cursor.execute(
            "UPDATE books SET title = ?, author = ?, published_year = ?, price = ?, genre = ? WHERE isbn = ?",
            (book.title, book.author, book.published_year, book.price, ",".join(book.genre), book.isbn)
        )
        if self.cursor.rowcount > 0:
            self.conn.commit()
            return True
        return False

    def delete_book(self, isbn: str):
        self.cursor.execute("DELETE FROM books WHERE isbn = ?", (isbn,))
        if self.cursor.rowcount > 0:
            self.conn.commit()
            return True
        return False

    def close(self):
        self.conn.close()
