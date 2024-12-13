from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
import pyodbc  # SQL Server

from connect import *
from colors import *

class ListScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        layout.add_widget(Label(text="Просмотр списков", font_size='20sp'))
        layout.add_widget(Button(text="Список максимальных покупок",
                                 on_press=lambda x: setattr(self.manager, 'current', 'top_customers_screen')))
        layout.add_widget(Button(text="Список изменений цены товара",
                                 on_press=lambda x: setattr(self.manager, 'current', 'price_changes_screen')))
        layout.add_widget(Button(text="Список категорий товаров",
                                 on_press=lambda x: setattr(self.manager, 'current', 'categories_screen')))
        layout.add_widget(Button(text="Назад", on_press=lambda x: setattr(self.manager, 'current', 'main_menu')))

        self.add_widget(layout)



class TopCustomersScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        self.layout.add_widget(Label(text="Введите дату", font_size='20sp'))
        self.layout.add_widget(
            Label(text="Для получения покупателей с максимальной суммой покупки напишите интересующую Вас дату"))

        self.date_input = TextInput(hint_text="ГГГГ-ММ-ДД")
        self.layout.add_widget(self.date_input)
        self.layout.add_widget(Button(text="Найти", on_press=self.get_top_customers))
        self.layout.add_widget(Button(text="Назад", on_press=lambda x: setattr(self.manager, 'current', 'list_screen')))

        self.add_widget(self.layout)

    def get_top_customers(self, instance):
        date = self.date_input.text
        try:
            conn = connect_to_db()
            cursor = conn.cursor()

            query = f"SELECT * FROM dbo.GetTopCustomersByDate(?)"
            cursor.execute(query, date)
            results = cursor.fetchall()

            cursor.close()
            conn.close()

            
            self.manager.get_screen('top_customers_result_screen').display_results(results)
            self.manager.current = 'top_customers_result_screen'
        except pyodbc.Error as e:
            self.layout.add_widget(Label(text=f"Ошибка: {str(e)}", color=(1, 0, 0, 1)))



class TopCustomersResultScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        self.add_widget(self.layout)

    def display_results(self, results):
        self.layout.clear_widgets()
        self.layout.add_widget(Label(text="Результаты", font_size='20sp'))

        table_layout = GridLayout(cols=3, size_hint_y=None)
        table_layout.bind(minimum_height=table_layout.setter('height'))
        table_layout.add_widget(Label(text="Дата покупки"))
        table_layout.add_widget(Label(text="Покупатель"))
        table_layout.add_widget(Label(text="Сумма покупки"))

        for row in results:
            for cell in row:
                table_layout.add_widget(Label(text=str(cell)))

        scroll = ScrollView(size_hint=(1, None), size=(self.width, 400))
        scroll.add_widget(table_layout)
        self.layout.add_widget(scroll)
        self.layout.add_widget(
            Button(text="Назад", on_press=lambda x: setattr(self.manager, 'current', 'top_customers_screen')))



class PriceChangesScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        self.layout.add_widget(Label(text="Введите данные", font_size='20sp'))
        self.product_code = TextInput(hint_text="Код отслеживаемого товара")
        self.start_date = TextInput(hint_text="Дата начала периода (ГГГГ-ММ-ДД)")
        self.end_date = TextInput(hint_text="Дата окончания периода (ГГГГ-ММ-ДД)")

        self.layout.add_widget(Label(text="Код отслеживаемого товара"))
        self.layout.add_widget(self.product_code)
        self.layout.add_widget(Label(text="Дата начала периода"))
        self.layout.add_widget(self.start_date)
        self.layout.add_widget(Label(text="Дата окончания периода"))
        self.layout.add_widget(self.end_date)

        self.layout.add_widget(Button(text="Отследить изменения стоимости", on_press=self.get_price_changes))
        self.layout.add_widget(Button(text="Назад", on_press=lambda x: setattr(self.manager, 'current', 'list_screen')))

        self.add_widget(self.layout)

    def get_price_changes(self, instance):
        code = self.product_code.text
        start_date = self.start_date.text
        end_date = self.end_date.text

        try:
            conn = connect_to_db()
            cursor = conn.cursor()

            query = f"SELECT * FROM dbo.GetPriceChanges(?, ?, ?)"
            cursor.execute(query, code, start_date, end_date)
            results = cursor.fetchall()

            cursor.close()
            conn.close()
            
            self.manager.get_screen('price_changes_result_screen').display_results(results)
            self.manager.current = 'price_changes_result_screen'
        except pyodbc.Error as e:
            self.layout.add_widget(Label(text=f"Ошибка: {str(e)}", color=(1, 0, 0, 1)))



class PriceChangesResultScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        self.results_list = BoxLayout(orientation='vertical', size_hint_y=None)
        self.results_list.bind(minimum_height=self.results_list.setter('height'))

        self.scroll_view = ScrollView()
        self.scroll_view.add_widget(self.results_list)

        self.layout.add_widget(Label(text="Результаты изменения цен", font_size='20sp'))
        self.layout.add_widget(self.scroll_view)
        self.layout.add_widget(Button(text="Назад", on_press=lambda x: setattr(self.manager, 'current', 'price_changes_screen')))

        self.add_widget(self.layout)

    def display_results(self, results):
        self.results_list.clear_widgets()
        if not results:
            self.results_list.add_widget(Label(text="Нет данных для отображения", size_hint_y=None, height=40))
            return

        self.results_list.add_widget(Label(text="Товар | Покупатель | Дата | Цена", size_hint_y=None, height=40))

        for record in results:
            product_name, costumer,date, price = record
            row = Label(text=f"{product_name} | {costumer} | {date} | {price}", size_hint_y=None, height=40)
            self.results_list.add_widget(row)



class CategoriesScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        self.layout.add_widget(Label(text="Список категорий", font_size='20sp'))
        self.layout.add_widget(Button(text="Назад", on_press=lambda x: setattr(self.manager, 'current', 'list_screen')))
        self.add_widget(self.layout)

    def on_pre_enter(self, *args):
        self.display_categories()

    def display_categories(self):
        try:
            conn = connect_to_db()
            cursor = conn.cursor()

            query = "SELECT * FROM dbo.GetCategories()"
            cursor.execute(query)
            results = cursor.fetchall()

            cursor.close()
            conn.close()

            self.layout.clear_widgets()
            self.layout.add_widget(Label(text="Категория | Наименование", font_size='20sp'))
            for category, name in results:
                self.layout.add_widget(Label(text=f"{category} | {name}"))

            self.layout.add_widget(
                Button(text="Назад", on_press=lambda x: setattr(self.manager, 'current', 'list_screen')))
        except pyodbc.Error as e:
            self.layout.add_widget(Label(text=f"Ошибка: {str(e)}", color=(1, 0, 0, 1)))