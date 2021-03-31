from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.label import MDLabel

# from kivy.core.window import Window
# # Window.softinput_mode = 'pan'
# Window.size = (400,300)

import AutoCARB
import numpy as np
import webbrowser

from kivy.uix.popup import Popup
from kivy.uix.image import Image

Builder.load_file('licence_label.kv') # serve per importare il file *.kv
class AutoCARB_app(MDApp):


    def build(self):
        self.title = "AutoCARB"
        self.theme_cls.theme_style = "Dark"  # "Light"
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.primary_hue = "300"
        return Builder.load_file("AutoCARB_layout.kv")

    # def on_start(self):
    #     for name_style in range(30):
    #         self.root.ids.box.add_widget(
    #             MDLabel(
    #                 text=f"{name_style} style",
    #                 halign="center",
    #             )
    #         )
    
    def image_button(self):
        pop = Popup(title='Carburetor Dimensions',
                content=Image(source='./media/drawing.jpg'),
                    size_hint=(1, 1),
                    separator_color= [0.7, 0.5, 1, 1],
                    separator_height='5dp',
                    title_align='center',
                    # title_size='14sp',
                    #  size=(400, 400)
                     )
        pop.open()

    def help_button(self):
        # webbrowser.open('https://github.com/dogengineer/AutoCARB/blob/main/Manuale_di_AutoCARB.pdf')
        webbrowser.open_new('https://drive.google.com/drive/folders/1Jhl9PxwQLWuTAZI_e3_Zsp0LWXrp-Qie')

    def start_button(self):
        AF = AutoCARB.rapporto_aria_benzina(float(self.root.ids["temp"].text), float(self.root.ids["pressione"].text),
        float(self.root.ids["phi"].text), float(self.root.ids["dpressione"].text),
        float(self.root.ids["d1"].text)*1e-3, float(self.root.ids["d3"].text)*1e-3,
        float(self.root.ids["d2max"].text)*1e-3, float(self.root.ids["d2min"].text)*1e-3,
        float(self.root.ids["hc"].text)*1e-3,float(self.root.ids["hd"].text)*1e-3,
        float(self.root.ids["dgetto"].text)*1e-5, float(self.root.ids["lcd"].text)*1e-3)

        error = AutoCARB.errore_rapporto_AF(float(self.root.ids["temp"].text), float(self.root.ids["pressione"].text),
        float(self.root.ids["phi"].text), float(self.root.ids["dpressione"].text),
        float(self.root.ids["d1"].text)*1e-3, float(self.root.ids["d3"].text)*1e-3,
        float(self.root.ids["d2max"].text)*1e-3, float(self.root.ids["d2min"].text)*1e-3,
        float(self.root.ids["hc"].text)*1e-3,float(self.root.ids["hd"].text)*1e-3,
        float(self.root.ids["dgetto"].text)*1e-5, float(self.root.ids["lcd"].text)*1e-3)

        lable = AutoCARB.lable_mixture(float(self.root.ids["temp"].text), float(self.root.ids["pressione"].text),
        float(self.root.ids["phi"].text), float(self.root.ids["dpressione"].text),
        float(self.root.ids["d1"].text)*1e-3, float(self.root.ids["d3"].text)*1e-3,
        float(self.root.ids["d2max"].text)*1e-3, float(self.root.ids["d2min"].text)*1e-3,
        float(self.root.ids["hc"].text)*1e-3,float(self.root.ids["hd"].text)*1e-3,
        float(self.root.ids["dgetto"].text)*1e-5, float(self.root.ids["lcd"].text)*1e-3)

        self.root.ids["af"].text = str(np.round(AF, decimals = 2))
        self.root.ids["err"].text = str(str(np.round(error, decimals = 2))+' %')

        self.root.ids["mixture_label"].text = lable
        if lable == "Rich mixture":
            self.root.ids["mixture_label"].text_color = (255/255, 80/255, 80/255, 1)     
        if lable == "Stoichiometric mixture":
            self.root.ids["mixture_label"].text_color = (51/255, 153/255, 51/255, 1)     
        if lable == "Lean mixture":
            self.root.ids["mixture_label"].text_color = (255/255, 80/255, 80/255, 1)   
                


AutoCARB_app().run()