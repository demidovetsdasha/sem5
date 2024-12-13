from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle


APP_BACKGROUND_COLOR = "#356C57"  # Основной цвет фона
BUTTON_BACKGROUND_COLOR = "#D0DB9D"  # Цвет фона кнопок
BUTTON_TEXT_COLOR = "#000000"  # Цвет текста на кнопках

class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*self.hex_to_rgb(APP_BACKGROUND_COLOR))  # Установить цвет фона
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    @staticmethod
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i + 2], 16) / 255.0 for i in (0, 2, 4))