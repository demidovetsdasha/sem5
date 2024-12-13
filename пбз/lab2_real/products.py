from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
import pyodbc  # SQL Server

from connect import *
from colors import *

class ProductMenu(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        layout.add_widget(Label(text="Операции с товарами", font_size='24sp'))

        
        buttons = [("Добавить товар", "add_product"),
                   ("Редактировать товар", "edit_product"),
                   ("Удалить товар", "delete_product")]
        for text, screen_name in buttons:
            btn = Button(
                text=text,
                font_size='18sp',
                on_release=lambda x, scr=screen_name: setattr(self.manager, 'current', scr)
            )
            layout.add_widget(btn)

        back_btn = Button(text="Назад", on_release=lambda x: setattr(self.manager, 'current', 'main_menu'))
        layout.add_widget(back_btn)

        self.add_widget(layout)



class AddProduct(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        layout.add_widget(Label(text="Добавление товара", font_size='24sp'))

        self.code_input = TextInput(hint_text="Код товара", multiline=False)
        layout.add_widget(self.code_input)

        self.name_input = TextInput(hint_text="Наименование товара", multiline=False)
        layout.add_widget(self.name_input)

        self.spinner = Spinner(
            text="Бытовые",  
            values=("Торговое оборудование", "Бытовые", "Промышленное"),  
            size_hint=(1, 0.2)
        )
        layout.add_widget(self.spinner)

        add_btn = Button(text="Добавить новый товар", on_release=self.add_product)
        layout.add_widget(add_btn)

        back_btn = Button(text="Назад", on_release=lambda x: setattr(self.manager, 'current', 'products'))
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def add_product(self, instance):
        product_code = self.code_input.text
        product_name = self.name_input.text
        product_category = self.spinner.text

        self.code_input.text = ''
        self.name_input.text = ''
        self.spinner.text = ''

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('EXEC AddProducts ?, ?, ?', product_name, product_category, product_code)
                conn.commit()
                print("Товар успешно добавлен!")
                setattr(self.manager, 'current', 'products')
            except pyodbc.Error as err:
                print(f"Ошибка при добавлении товара: {err}")
            finally:
                conn.close()


class EditProduct(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        layout.add_widget(Label(text="Редактировать товар", font_size='24sp'))

        self.code_input = TextInput(hint_text="Код товара (для поиска)", multiline=False)
        layout.add_widget(self.code_input)

        self.name_input = TextInput(hint_text="Новое наименование товара", multiline=False)
        layout.add_widget(self.name_input)

        self.category_input = TextInput(hint_text="Новая категория", multiline=False)
        layout.add_widget(self.category_input)

        edit_btn = Button(text="Сохранить изменения", on_release=self.edit_product)
        layout.add_widget(edit_btn)

        back_btn = Button(text="Назад", on_release=lambda x: setattr(self.manager, 'current', 'products'))
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def edit_product(self, instance):
        product_code = self.code_input.text
        product_name = self.name_input.text
        product_category = self.category_input.text

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('EXEC EditProducts ?, ?, ?', product_code, product_name, product_category)
                conn.commit()
                print("Товар успешно обновлен!")
                setattr(self.manager, 'current', 'products')
            except pyodbc.Error as err:
                print(f"Ошибка при редактировании товара: {err}")
            finally:
                conn.close()

        self.code_input.text = ''
        self.name_input.text = ''
        self.spinner.text = ''


class DeleteProduct(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        layout.add_widget(Label(text="Удалить товар", font_size='24sp'))

        self.code_input = TextInput(hint_text="Введите код товара", multiline=False)
        layout.add_widget(self.code_input)

        delete_btn = Button(text="Удалить", on_release=self.delete_product)
        layout.add_widget(delete_btn)

        back_btn = Button(text="Назад", on_release=lambda x: setattr(self.manager, 'current', 'products'))
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def delete_product(self, instance):
        product_code = self.code_input.text

        self.code_input.text = ''

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('EXEC DeleteProducts ?', product_code)
                conn.commit()
                print("Товар успешно удален!")
                setattr(self.manager, 'current', 'products')
            except pyodbc.Error as err:
                print(f"Ошибка при удалении товара: {err}")
            finally:
                conn.close()

        self.code_input.text = ''