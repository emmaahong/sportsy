from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout

Builder.load_file('box1.kv')

class main_kv(GridLayout):
    pass

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return main_kv()


MainApp().run() 