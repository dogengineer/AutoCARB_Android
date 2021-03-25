from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.label import MDLabel

import AutoCARB
import numpy as np

class AutoCARB_app(MDApp):

    def build(self):
        self.title = "AutoCARB"
        self.theme_cls.primary_palette = "Purple"
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
        
        self.root.ids["af"].text = str(np.round(AF, decimals = 2))
        self.root.ids["err"].text = str(np.round(error, decimals = 2))


AutoCARB_app().run()