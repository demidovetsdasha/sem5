from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
import pyodbc  # SQL Server

from connect import *
from colors import *


class InvoiceMenu(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        layout.add_widget(Label(text="Операции с накладными", font_size='24sp'))

        buttons = [("Добавить накладную", "add_invoice"),
                   ("Редактировать накладную", "find_invoice"),
                   ("Удалить накладную", "delete_invoice")]
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



class AddInvoice(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        layout.add_widget(Label(text="Добавление накладной", font_size='24sp'))

        self.customer_name_input = TextInput(hint_text="Имя покупателя", multiline=False)
        layout.add_widget(self.customer_name_input)

        self.invoice_date_input = TextInput(hint_text="Дата накладной (ГГГГ-ММ-ДД)", multiline=False)
        layout.add_widget(self.invoice_date_input)

        # выпадающий список
        self.spinner = Spinner(
            text="Физ лицо",  
            values=("Физ лицо", "Юр лицо"),  
            size_hint=(1, 0.2)
        )
        layout.add_widget(self.spinner)

        self.price_input = TextInput(hint_text="Итоговая стоимость", multiline=False)
        layout.add_widget(self.price_input)

        self.product_input = TextInput(hint_text="Код товара", multiline=False)
        layout.add_widget(self.product_input)

        self.product_count_input = TextInput(hint_text="Количество отпущенного товара", multiline=False)
        layout.add_widget(self.product_count_input)

        add_btn = Button(text="Далее", on_release=self.to_step_two)
        layout.add_widget(add_btn)

        back_btn = Button(text="Назад", on_release=lambda x: setattr(self.manager, 'current', 'invoices'))
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def to_step_two(self, instance):
        customer_name = self.customer_name_input.text
        invoice_date = self.invoice_date_input.text
        spinner = self.spinner.text
        price = self.price_input.text
        product = self.product_input.text
        product_count = self.product_count_input.text

        self.customer_name_input.text = ""
        self.invoice_date_input.text = ""
        self.spinner.text = ""
        self.price_input.text = ""
        self.product_input.text = ""
        self.product_count_input.text = ""

        self.manager.get_screen('add_invoice_two').continue_invoice_creation(customer_name, invoice_date, spinner, price, product, product_count)
        self.manager.current = 'add_invoice_two'


class AddInvoiceStepTwo(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_count = None
        self.product = None
        self.price = None
        self.costumer_type = None
        self.invoice_date = None
        self.costumer_name = None
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        layout.add_widget(Label(text="Добавление накладной", font_size='24sp'))

        self.point_input = TextInput(hint_text="Пункт назначения (Страна, область, населнный пункт)", multiline=False)
        layout.add_widget(self.point_input)

        self.destination_input = TextInput(hint_text="Адрес", multiline=False)
        layout.add_widget(self.destination_input)

        self.passport_input = TextInput(hint_text="Серия паспорта", multiline=False)
        layout.add_widget(self.passport_input)

        self.passport_id_input = TextInput(hint_text="Номер паспорта", multiline=False)
        layout.add_widget(self.passport_id_input)

        self.bank_input = TextInput(hint_text="Номер банковского счета", multiline=False)
        layout.add_widget(self.bank_input)

        self.bank_name_input = TextInput(hint_text="Название банка", multiline=False)
        layout.add_widget(self.bank_name_input)

        add_btn = Button(text="Добавить накладную", on_release=self.add_invoice)
        layout.add_widget(add_btn)

        back_btn = Button(text="Назад", on_release=lambda x: setattr(self.manager, 'current', 'invoices'))
        layout.add_widget(back_btn)

        self.add_widget(layout)
        
        
    def continue_invoice_creation(self, customer_name, invoice_date, spinner, price, product, product_count):
        self.costumer_name = customer_name
        self.invoice_date = invoice_date
        self.costumer_type = spinner
        self.price = price
        self.product = product
        self.product_count = product_count

    def add_invoice(self, instance):
        point = self.point_input.text.split(", ")
        destination = self.destination_input.text
        passport = self.passport_input.text
        passport_id = self.passport_id_input.text
        bank = self.bank_input.text
        bank_name = self.bank_name_input.text

        self.point_input.text = ""
        self.destination_input.text = ""
        self.passport_input.text = ""
        self.passport_id_input = ""
        self.bank_input.text = ""
        self.bank_input.text = ""

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('EXEC AddInvoiceWithDetails ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?', self.costumer_name, self.invoice_date, self.costumer_type, self.price, self.product, self.product_count, point[2], point[1], point[0], destination, passport, passport_id, bank, bank_name)
                conn.commit()
                print("Накладная успешно добавлена!")
                setattr(self.manager, 'current', 'invoices')
            except pyodbc.Error as err:
                print(f"Ошибка при добавлении накладной: {err}")
            finally:
                conn.close()

class InvoiceToEditSelect(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.invoice_date_input = TextInput(hint_text="Дата накладной (ГГГГ-ММ-ДД)", multiline=False)
        layout.add_widget(self.invoice_date_input)

        self.name_input = TextInput(hint_text="Имя покупателя", multiline=False)
        layout.add_widget(self.name_input)

        self.town_input = TextInput(hint_text="Город назначения", multiline=False)
        layout.add_widget(self.town_input)

        add_btn = Button(text="Далее", on_release=self.to_step_two)
        layout.add_widget(add_btn)

        back_btn = Button(text="Назад", on_release=lambda x: setattr(self.manager, 'current', 'invoices'))
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def to_step_two(self, instance):
        date = self.invoice_date_input.text
        name = self.name_input.text
        town = self.town_input.text

        self.invoice_date_input.text = ''
        self.name_input.text = ''
        self.town_input.text = ''

        try:
            conn = connect_to_db()
            cursor = conn.cursor()

            query = f"SELECT * FROM dbo.GetInvoiceId(?, ?, ?)"
            cursor.execute(query, date, name, town)
            results = cursor.fetchall()

            cursor.close()
            conn.close()

            print(results)

            self.manager.get_screen('edit_invoice').edit_this(0)
            self.manager.current = 'edit_invoice'

        except pyodbc.Error as err:
            print(f"Ошибка при поиске накладной: {err}")

        self.invoice_date_input.text = ''
        self.name_input.text = ''
        self.town_input.text = ''

class EditInvoice(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = None
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        layout.add_widget(Label(text="Редактирование накладной", font_size='24sp'))

        self.customer_name_input = TextInput(hint_text="Имя покупателя", multiline=False)
        layout.add_widget(self.customer_name_input)

        self.invoice_date_input = TextInput(hint_text="Дата накладной (ГГГГ-ММ-ДД)", multiline=False)
        layout.add_widget(self.invoice_date_input)

        # выпадающий список
        self.spinner = Spinner(
            text="Физ лицо",
            values=("Физ лицо", "Юр лицо"),
            size_hint=(1, 0.2)
        )
        layout.add_widget(self.spinner)

        self.price_input = TextInput(hint_text="Итоговая стоимость", multiline=False)
        layout.add_widget(self.price_input)

        self.product_input = TextInput(hint_text="Код товара", multiline=False)
        layout.add_widget(self.product_input)

        self.product_count_input = TextInput(hint_text="Количество отпущенного товара", multiline=False)
        layout.add_widget(self.product_count_input)

        add_btn = Button(text="Далее", on_release=self.to_step_two)
        layout.add_widget(add_btn)

        back_btn = Button(text="Назад", on_release=lambda x: setattr(self.manager, 'current', 'invoices'))
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def edit_this(self, iid):
        self.id = iid

    def to_step_two(self, instance):
        customer_name = self.customer_name_input.text
        invoice_date = self.invoice_date_input.text
        spinner = self.spinner.text
        price = self.price_input.text
        product = self.product_input.text
        product_count = self.product_count_input.text

        self.manager.get_screen('edit_invoice_two').continue_invoice_creation(self.id, customer_name, invoice_date, spinner, price, product, product_count)
        self.manager.current = 'edit_invoice_two'

        self.customer_name_input.text = ""
        self.invoice_date_input.text = ""
        self.spinner.text = ""
        self.price_input.text = ""
        self.product_input.text = ""
        self.product_count_input.text = ""

class EditInvoiceStepTwo(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = None
        self.product_count = None
        self.product = None
        self.price = None
        self.costumer_type = None
        self.invoice_date = None
        self.costumer_name = None
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        layout.add_widget(Label(text="Редактирование накладной", font_size='24sp'))

        self.point_input = TextInput(hint_text="Пункт назначения (Страна, область, населнный пункт)", multiline=False)
        layout.add_widget(self.point_input)

        self.destination_input = TextInput(hint_text="Адрес", multiline=False)
        layout.add_widget(self.destination_input)

        self.passport_input = TextInput(hint_text="Серия паспорта", multiline=False)
        layout.add_widget(self.passport_input)

        self.passport_id_input = TextInput(hint_text="Номер паспорта", multiline=False)
        layout.add_widget(self.passport_id_input)

        self.bank_input = TextInput(hint_text="Номер банковского счета", multiline=False)
        layout.add_widget(self.bank_input)

        self.bank_name_input = TextInput(hint_text="Название банка", multiline=False)
        layout.add_widget(self.bank_name_input)

        add_btn = Button(text="Добавить накладную", on_release=self.add_invoice)
        layout.add_widget(add_btn)

        back_btn = Button(text="Назад", on_release=lambda x: setattr(self.manager, 'current', 'invoices'))
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def continue_invoice_creation(self, id, customer_name, invoice_date, spinner, price, product, product_count):
        self.id = id
        self.costumer_name = customer_name
        self.invoice_date = invoice_date
        self.costumer_type = spinner
        self.price = price
        self.product = product
        self.product_count = product_count

    def add_invoice(self, instance):
        point = self.point_input.text.split(", ")
        destination = self.destination_input.text
        passport = self.passport_input.text
        passport_id = self.passport_id_input.text
        bank = self.bank_input.text
        bank_name = self.bank_name_input.text

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('EXEC EditInvoiceWithDetails ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?',
                               self.id,
                               self.costumer_name, self.invoice_date, self.costumer_type, self.price, self.product,
                               self.product_count, point[2], point[1], point[0], destination, passport, passport_id,
                               bank, bank_name)
                conn.commit()
                print("Накладная успешно добавлена!")
                setattr(self.manager, 'current', 'invoices')
            except pyodbc.Error as err:
                print(f"Ошибка при добавлении накладной: {err}")
            finally:
                conn.close()

        self.point_input.text = ""
        self.destination_input.text = ""
        self.passport_input.text = ""
        self.passport_id_input = ""
        self.bank_input.text = ""
        self.bank_input.text = ""


class DeleteInvoice(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        layout.add_widget(Label(text="Удалить накладную", font_size='24sp'))

        self.invoice_date_input = TextInput(hint_text="Дата накладной (ГГГГ-ММ-ДД)", multiline=False)
        layout.add_widget(self.invoice_date_input)

        self.name_input = TextInput(hint_text="Имя покупателя", multiline=False)
        layout.add_widget(self.name_input)

        self.town_input = TextInput(hint_text="Город назначения", multiline=False)
        layout.add_widget(self.town_input)

        delete_btn = Button(text="Удалить", on_release=self.delete_invoice)
        layout.add_widget(delete_btn)

        back_btn = Button(text="Назад", on_release=lambda x: setattr(self.manager, 'current', 'invoices'))
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def delete_invoice(self, instance):
        date = self.invoice_date_input.text
        name = self.name_input.text
        town = self.town_input.text

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('EXEC DeleteInvoice ?, ?, ?', date, name, town)
                conn.commit()
                print("Накладная успешно удалена!")
                setattr(self.manager, 'current', 'products')
            except pyodbc.Error as err:
                print(f"Ошибка при удалении накладной: {err}")
            finally:
                conn.close()

        self.invoice_date_input.text = ''
        self.name_input.text = ''
        self.town_input.text = ''
