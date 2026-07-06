# Controller/library_controller.py
from Model.library_model import LibraryModel
from Model.data_manager import DataManager
from Model.book import Book


class LibraryController:
    def __init__(self):
        self.model = LibraryModel()
        self.data_manager = DataManager()
        self.view = None
        self.load_data()
    
    def load_data(self):
        try:
            self.model.books = self.data_manager.load_books()
            print(f"✅ {len(self.model.books)} books loaded!")
        except Exception as e:
            print(f"⚠️ Error: {e}")
            self.model.books = []
    
    def save_data(self):
        try:
            return self.data_manager.save_books(self.model.books)
        except Exception as e:
            return f"❌ Error: {e}"
    
    def add_book(self, title, author, year, isbn, genre):
        if not title or not author:
            msg = "❌ Title and author are required!"
            if self.view:
                self.view.update_message(msg)
            return msg
        
        try:
            year_int = int(year)
            if not (1900 <= year_int <= 2026):
                msg = "❌ Invalid year! (1900-2026)"
                if self.view:
                    self.view.update_message(msg)
                return msg
        except ValueError:
            msg = "❌ Year must be a number!"
            if self.view:
                self.view.update_message(msg)
            return msg
        
        isbn_clean = isbn.replace("-", "").replace(" ", "")
        if len(isbn_clean) not in [10, 13] or not isbn_clean.isdigit():
            msg = "❌ Invalid ISBN! Must be 10 or 13 digits"
            if self.view:
                self.view.update_message(msg)
            return msg
        
        try:
            book = Book(title, author, year_int, isbn, genre or "Unknown")
            result = self.model.add_book(book)
            self.save_data()
            if self.view:
                self.view.update_message(result)
                self.view.update_book_list()
            return result
        except ValueError as e:
            msg = f"❌ {e}"
            if self.view:
                self.view.update_message(msg)
            return msg
    
    def remove_book_from_ui(self, isbn):
        try:
            result = self.model.remove_book(isbn)
            self.save_data()
            if self.view:
                self.view.update_message(result)
                self.view.update_book_list()
            return result
        except ValueError as e:
            msg = f"❌ {e}"
            if self.view:
                self.view.update_message(msg)
            return msg
    
    def search_books_from_ui(self, keyword, search_type):
        if not keyword:
            if self.view:
                self.view.update_message("Please enter a search term!")
                self.view.update_book_list()
            return []
        
        search_type_lower = search_type.lower()
        if search_type_lower == "title":
            results = self.model.search_by_title(keyword)
        elif search_type_lower == "author":
            results = self.model.search_by_author(keyword)
        elif search_type_lower == "genre":
            results = self.model.search_by_genre(keyword)
        else:
            results = []
        
        if self.view:
            if results:
                self.view.update_message(f"✅ Found {len(results)} books!")
            else:
                self.view.update_message("❌ No books found!")
            self.view.update_book_list(results)
        
        return results
    
    def borrow_or_return_book(self, isbn, is_borrowed):
        try:
            if is_borrowed:
                result = self.model.return_book(isbn)
            else:
                result = self.model.borrow_book(isbn)
            
            self.save_data()
            if self.view:
                self.view.update_message(result)
                self.view.update_book_list()
            return result
        except ValueError as e:
            msg = f"❌ {e}"
            if self.view:
                self.view.update_message(msg)
            return msg
    
    def show_statistics(self):
        
        try:
            stats = self.model.get_statistics()
            if stats is None:
                msg = "📊 No data available!"
                if self.view:
                    self.view.update_message(msg)
                return None
            
            msg = f"📊 Total: {stats['total']} | Available: {stats['available']} | Borrowed: {stats['borrowed']}"
            if self.view:
                self.view.update_message(msg)
            return stats
        except Exception as e:
            msg = f"❌ Error getting statistics: {e}"
            if self.view:
                self.view.update_message(msg)
            return None
    
    def get_statistics(self):
        
        try:
            return self.model.get_statistics()
        except Exception as e:
            print(f"⚠️ Error in get_statistics: {e}")
            return {
                "total": 0,
                "available": 0,
                "borrowed": 0,
                "genres": {}
            }
    
    def get_all_books(self):
        return self.model.get_all_books()