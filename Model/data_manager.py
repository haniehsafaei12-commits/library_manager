
import json
import os
from Model.book import Book


class DataManager:
    def __init__(self, filename="data/library.json"):
        self.filename = filename
    
    def save_books(self, books):
        """save books in json file"""
        try:
            
            os.makedirs(os.path.dirname(self.filename), exist_ok=True)
            
            
            data = [book.to_dict() for book in books]
            
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            
            return f"✅ {len(books)} books saved successfully!"
        except Exception as e:
            return f"❌ Error saving data: {e}"
    
    def load_books(self):
        
        if not os.path.exists(self.filename):
            return []
        
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
            
            
            books = [Book.from_dict(item) for item in data]
            return books
        except Exception as e:
            print(f"⚠️ Error loading data: {e}")
            return []