"""Util functions file"""

def calculate_discounted_price(price, discount_percentage):
    """Calculate and return the discounted price based on a given discount percentage."""
    return round(price * (1 - discount_percentage / 100), 2)

def get_book_response(book):
    """Return a dictionary representation of a book."""
    return {
        "isbn": book.isbn,
        "title": book.title,
        "author": book.author,
        "published_year": book.published_year,
        "price": book.price,
        "genre": book.genre,
    }

def get_discounted_book_info(book, discount_percentage):
    """Generate response data for a book with original and discounted prices."""
    return {
        "isbn": book.isbn,
        "title": book.title,
        "original_price": book.price,
        "discount": f"{discount_percentage}%",
        "discounted_price": calculate_discounted_price(book.price, discount_percentage),
    }

def filter_books_by_price(books, min_price, max_price):
    """Filter books within the given price range."""
    if max_price < min_price:
        return []
    return [book for book in books if min_price <= book.price <= max_price]

def sort_books_by_price(books):
    """Sort books by price (and title if prices are identical) in ascending order."""
    return sorted(books, key=lambda book: (book.price, book.title))

def filter_and_sort_books_by_price_range(books, min_price, max_price):
    """Filter and sort books within a given price range."""
    filtered_books = filter_books_by_price(books, min_price, max_price)
    return sort_books_by_price(filtered_books)
