"""Book dataclass"""

from dataclasses import dataclass


@dataclass
class Book:
    """Book dataclass"""
    isbn: str
    title: str
    author: str
    published_year: int
    price: float
    genre: tuple
