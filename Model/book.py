# Model/book.py
class Book:
    def __init__(self, title, author, year, isbn, genre="Unknown"):
        self.title = title
        self.author = author
        self.year = year
        self.isbn = isbn
        self.genre = genre
        self.is_borrowed = False
    
    def __str__(self):
        status = "📖 Available" if not self.is_borrowed else "🚀 Borrowed"
        return f"{self.title} | {self.author} ({self.year}) | {status}"
    
    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "isbn": self.isbn,
            "genre": self.genre,
            "is_borrowed": self.is_borrowed
        }
    
    @classmethod
    def from_dict(cls, data):
        book = cls(data["title"], data["author"], data["year"], data["isbn"], data["genre"])
        book.is_borrowed = data["is_borrowed"]
        return book