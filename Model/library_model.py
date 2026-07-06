
from Model.book import Book


class LibraryModel:
    def __init__(self):
        self.books = []
    
    def add_book(self, book):
        for existing_book in self.books:
            if existing_book.isbn == book.isbn:
                raise ValueError(f"Book with ISBN {book.isbn} already exists!")
        
        self.books.append(book)
        return f"✅ Book '{book.title}' added successfully!"
    
    def remove_book(self, isbn):
        for i, book in enumerate(self.books):
            if book.isbn == isbn:
                removed = self.books.pop(i)
                return f"❌ Book '{removed.title}' removed!"
        raise ValueError(f"Book with ISBN {isbn} not found!")
    
    def search_by_title(self, title):
        return [book for book in self.books if title.lower() in book.title.lower()]
    
    def search_by_author(self, author):
        return [book for book in self.books if author.lower() in book.author.lower()]
    
    def search_by_genre(self, genre):
        return [book for book in self.books if genre.lower() in book.genre.lower()]
    
    def borrow_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                if book.is_borrowed:
                    raise ValueError(f"Book '{book.title}' is already borrowed!")
                book.is_borrowed = True
                return f"✅ Book '{book.title}' borrowed successfully!"
        raise ValueError(f"Book with ISBN {isbn} not found!")
    
    def return_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                if not book.is_borrowed:
                    raise ValueError(f"Book '{book.title}' is not borrowed!")
                book.is_borrowed = False
                return f"✅ Book '{book.title}' returned successfully!"
        raise ValueError(f"Book with ISBN {isbn} not found!")
    
    def get_statistics(self):
        
        total = len(self.books)
        borrowed = sum(1 for book in self.books if book.is_borrowed)
        available = total - borrowed
        
        genres = {}
        for book in self.books:
            genres[book.genre] = genres.get(book.genre, 0) + 1
        
        return {
            "total": total,
            "available": available,
            "borrowed": borrowed,
            "genres": genres
        }
    
    def get_all_books(self):
        return self.books