from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from products import *
from invoices import *
from lists import *
from colors import *

class MainMenu(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        layout.add_widget(Label(text="Доступные разделы", font_size='24sp'))

        
        buttons = [("Товары", "products"),
                   ("Накладные", "invoices"),
                   ("Списки", "list_screen")]
        for text, screen_name in buttons:
            btn = Button(
                text=text,
                font_size='18sp',
                on_release=lambda x, scr=screen_name: setattr(self.manager, 'current', scr)
            )

            layout.add_widget(btn)

        self.add_widget(layout)




class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='main_menu'))
        sm.add_widget(ProductMenu(name='products'))
        sm.add_widget(InvoiceMenu(name='invoices'))
        sm.add_widget(ListScreen(name='list_screen'))

        sm.add_widget(AddProduct(name='add_product'))
        sm.add_widget(EditProduct(name='edit_product'))
        sm.add_widget(DeleteProduct(name='delete_product'))

        sm.add_widget(AddInvoice(name='add_invoice'))
        sm.add_widget(AddInvoiceStepTwo(name='add_invoice_two'))
        sm.add_widget(InvoiceToEditSelect(name="find_invoice"))
        sm.add_widget(EditInvoice(name='edit_invoice'))
        sm.add_widget(EditInvoiceStepTwo(name='edit_invoice_two'))
        sm.add_widget(DeleteInvoice(name='delete_invoice'))

        sm.add_widget(TopCustomersScreen(name='top_customers_screen'))
        sm.add_widget(TopCustomersResultScreen(name='top_customers_result_screen'))
        sm.add_widget(CategoriesScreen(name='categories_screen'))
        sm.add_widget(PriceChangesScreen(name='price_changes_screen'))
        sm.add_widget(PriceChangesResultScreen(name='price_changes_result_screen'))
        return sm


if __name__ == '__main__':
    MainApp().run()
