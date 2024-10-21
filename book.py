"""Book dataclass"""

from dataclasses import dataclass


@dataclass
class Book:
    isbn: str
    title: str
    author: str
    published_year: int
    price: float
    genre: list[str]
