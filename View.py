# view.py
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock  
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle


Window.size = (1000, 700)
Window.clearcolor = (0.95, 0.95, 0.98, 1)


class BookItem(BoxLayout):
    text = StringProperty("")
    isbn = StringProperty("")
    is_borrowed = BooleanProperty(False)
    controller = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 10
        self.size_hint_y = None
        self.height = 50
        self.padding = [10, 5]
        
        
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[8])
        self.bind(size=self.update_rect, pos=self.update_rect)
        
        
        self.label = Label(
            text=self.text,
            size_hint_x=0.55,
            color=(0.1, 0.1, 0.1, 1),
            font_size=13
        )
        self.add_widget(self.label)
        
        
        self.btn_borrow = Button(
            text="📖 Borrow" if not self.is_borrowed else "🔄 Return",
            size_hint_x=0.2,
            background_color=(0.2, 0.7, 0.3, 1) if not self.is_borrowed else (0.9, 0.6, 0.1, 1),
            color=(1, 1, 1, 1),
            font_size=12
        )
        self.btn_borrow.bind(on_press=self.on_borrow)
        self.add_widget(self.btn_borrow)
        
        
        self.btn_delete = Button(
            text="🗑️",
            size_hint_x=0.1,
            background_color=(0.8, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size=14
        )
        self.btn_delete.bind(on_press=self.on_delete)
        self.add_widget(self.btn_delete)
    
    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos
    
    def on_borrow(self, instance):
        if self.controller:
            self.controller.borrow_or_return_book(self.isbn, self.is_borrowed)
    
    def on_delete(self, instance):
        if self.controller:
            self.controller.remove_book_from_ui(self.isbn)


class MainScreen(BoxLayout):
    controller = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        
        self.build_ui()
    
    def build_ui(self):
        title = Label(
            text="📚 Personal Library Manager",
            font_size=28,
            bold=True,
            color=(0.2, 0.4, 0.7, 1),
            size_hint_y=None,
            height=60
        )
        self.add_widget(title)
        
        self.message_label = Label(
            text="✨ Welcome to your library!",
            font_size=14,
            color=(0.2, 0.6, 0.8, 1),
            size_hint_y=None,
            height=30
        )
        self.add_widget(self.message_label)
        
        main = BoxLayout(spacing=15)
        
        left = BoxLayout(
            orientation='vertical',
            spacing=8,
            size_hint_x=0.35
        )
        
        form_card = BoxLayout(
            orientation='vertical',
            spacing=8,
            padding=15,
            size_hint_y=None,
            height=400
        )
        with form_card.canvas.before:
            Color(1, 1, 1, 1)
            self.form_rect = RoundedRectangle(size=form_card.size, pos=form_card.pos, radius=[12])
        form_card.bind(size=self.update_form_rect, pos=self.update_form_rect)
        
        form_card.add_widget(Label(
            text="➕ Add New Book",
            font_size=18,
            bold=True,
            color=(0.2, 0.4, 0.7, 1),
            size_hint_y=None,
            height=35
        ))
        
        self.title_input = TextInput(
            hint_text="Title *",
            size_hint_y=None,
            height=35,
            background_color=(0.95, 0.95, 0.98, 1)
        )
        form_card.add_widget(self.title_input)
        
        self.author_input = TextInput(
            hint_text="Author *",
            size_hint_y=None,
            height=35,
            background_color=(0.95, 0.95, 0.98, 1)
        )
        form_card.add_widget(self.author_input)
        
        self.year_input = TextInput(
            hint_text="Year (e.g., 2020)",
            size_hint_y=None,
            height=35,
            background_color=(0.95, 0.95, 0.98, 1)
        )
        form_card.add_widget(self.year_input)
        
        self.isbn_input = TextInput(
            hint_text="ISBN (10 or 13 digits)",
            size_hint_y=None,
            height=35,
            background_color=(0.95, 0.95, 0.98, 1)
        )
        form_card.add_widget(self.isbn_input)
        
        self.genre_input = TextInput(
            hint_text="Genre (e.g., Fiction)",
            size_hint_y=None,
            height=35,
            background_color=(0.95, 0.95, 0.98, 1)
        )
        form_card.add_widget(self.genre_input)
        
        btn_add = Button(
            text="➕ Add Book",
            size_hint_y=None,
            height=40,
            background_color=(0.2, 0.7, 0.3, 1),
            color=(1, 1, 1, 1),
            font_size=14
        )
        btn_add.bind(on_press=self.on_add_book)
        form_card.add_widget(btn_add)
        
        btn_clear = Button(
            text="🗑️ Clear Form",
            size_hint_y=None,
            height=35,
            background_color=(0.8, 0.2, 0.2, 0.8),
            color=(1, 1, 1, 1),
            font_size=13
        )
        btn_clear.bind(on_press=self.on_clear_form)
        form_card.add_widget(btn_clear)
        
        left.add_widget(form_card)
        main.add_widget(left)
        
        
        right = BoxLayout(
            orientation='vertical',
            spacing=8,
            size_hint_x=0.65
        )
        
        
        search_box = BoxLayout(size_hint_y=None, height=40, spacing=8)
        self.search_input = TextInput(
            hint_text="🔍 Search books...",
            size_hint_x=0.7,
            background_color=(0.95, 0.95, 0.98, 1)
        )
        search_box.add_widget(self.search_input)
        
        btn_search = Button(
            text="🔍 Search",
            size_hint_x=0.3,
            background_color=(0.3, 0.6, 0.9, 1),
            color=(1, 1, 1, 1)
        )
        btn_search.bind(on_press=self.on_search)
        search_box.add_widget(btn_search)
        right.add_widget(search_box)
        
        
        right.add_widget(Label(
            text="Books in Library",
            font_size=16,
            bold=True,
            color=(0.2, 0.4, 0.7, 1),
            size_hint_y=None,
            height=30
        ))
        
        self.book_list = RecycleView(
            viewclass='BookItem',
            data=[],
            size_hint_y=1
        )
        
        layout = RecycleBoxLayout(
            default_size=(1, 55),
            default_size_hint=(1, None),
            size_hint_y=None,
            height=self.book_list.height,
            orientation='vertical',
            spacing=5
        )
        layout.bind(minimum_height=layout.setter('height'))
        self.book_list.layout = layout
        self.book_list.add_widget(layout)
        right.add_widget(self.book_list)
        
        main.add_widget(right)
        self.add_widget(main)
        
        Clock.schedule_once(lambda dt: self.update_stats(), 0.3)
    
    def update_form_rect(self, *args):
        self.form_rect.size = self.children[0].size
        self.form_rect.pos = self.children[0].pos
    
    def update_stats(self):
        if self.controller:
            stats = self.controller.get_statistics()
            if stats:
                self.message_label.text = (
                    f"📊 {stats['total']} books | {stats['available']} available | {stats['borrowed']} borrowed"
                )
    
    def update_message(self, text):
        self.message_label.text = text
    
    def update_book_list(self, books=None):
        if books is None:
            books = self.controller.get_all_books()
        if books is None:
            books = []
        data = []
        for book in books:
            data.append({
                "text": f"{book.title} | {book.author} ({book.year}) - {book.genre}",
                "isbn": book.isbn,
                "is_borrowed": book.is_borrowed,
                "controller": self.controller
            })
        self.book_list.data = data
        self.update_stats()
    
    def on_add_book(self, instance):
        self.controller.add_book(
            self.title_input.text,
            self.author_input.text,
            self.year_input.text,
            self.isbn_input.text,
            self.genre_input.text
        )
        self.on_clear_form(None)
    
    def on_search(self, instance):
        self.controller.search_books_from_ui(self.search_input.text, "Title")
    
    def on_clear_form(self, instance):
        self.title_input.text = ""
        self.author_input.text = ""
        self.year_input.text = ""
        self.isbn_input.text = ""
        self.genre_input.text = ""


class LibraryApp(App):
    def build(self):
        self.title = "📚 Library Manager"
        
        from Controller.library_controller import LibraryController
        self.controller = LibraryController()
        self.main_screen = MainScreen()
        self.main_screen.controller = self.controller
        self.controller.view = self.main_screen
        self.main_screen.update_book_list()
        return self.main_screen


def run():
    LibraryApp().run()


if __name__ == "__main__":
    run()