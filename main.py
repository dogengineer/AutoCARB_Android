import kivy # Importa il package "kiwi", che contiene tanti moduli
from kivy.properties import ObjectProperty
from kivy.app import App # Dal modulo "kiwi.app" importa la classe "App"
from kivy.uix.boxlayout import BoxLayout # Dal modulo "kiwi.uix.label" importa la classe "Label"
from kivy.uix.popup import Popup

import AutoCARB

import numpy as np

class CustomPopup(Popup):
    invia_form = ObjectProperty(None)
    def dismiss_popup(self):
        self.dismiss()


class MainWindow(BoxLayout):
    submit_button = ObjectProperty(None)
    tamb = ObjectProperty(None)
    pamb = ObjectProperty(None)
    phi = ObjectProperty(None)
    deltap = ObjectProperty(None)
    d1 = ObjectProperty(None)
    d3 = ObjectProperty(None)
    d2max = ObjectProperty(None)
    d2min = ObjectProperty(None)
    hc = ObjectProperty(None)
    hd = ObjectProperty(None)
    dgetto = ObjectProperty(None)
    lcd = ObjectProperty(None)
    rapporto_AF = ObjectProperty(None)
    errore_AF = ObjectProperty(None)
    def conferma_invio_form(self):
        custom_popup = CustomPopup(title="Conderma invio form", size_hint=(0.5, 0.5), invia_form=self.invia_form)
        custom_popup.open()

    def invia_form(self):
        
        AF = AutoCARB.rapporto_aria_benzina(float(self.tamb.text), float(self.pamb.text), float(self.phi.text),
             float(self.deltap.text), float(self.d1.text)*1e-3, float(self.d3.text)*1e-3, float(self.d2max.text)*1e-3, 
             float(self.d2min.text)*1e-3, float(self.hc.text)*1e-3, float(self.hd.text)*1e-3, float(self.dgetto.text)*1e-5, 
             float(self.lcd.text)*1e-3)
        self.rapporto_AF.text = str(np.round(AF,decimals=2))
        
        err = AutoCARB.errore_rapporto_AF(float(self.tamb.text), float(self.pamb.text), float(self.phi.text),
             float(self.deltap.text), float(self.d1.text)*1e-3, float(self.d3.text)*1e-3, float(self.d2max.text)*1e-3, 
             float(self.d2min.text)*1e-3, float(self.hc.text)*1e-3, float(self.hd.text)*1e-3, float(self.dgetto.text)*1e-5, 
             float(self.lcd.text)*1e-3)
        self.errore_AF.text = str(np.round(err,decimals=2))

        

class MainApp(App):
    def build(self):
        return MainWindow()


if __name__ == '__main__': # non eseguire se vieni importato come libreria
    # AutoCARB.cp_air_interp(20)

    # AutoCARB.Coefficiente_efflusso_aria(20, 101325, 13325, 0.042, 0.02, 0.019, 0.019)

    #AutoCARB.portata_benzina()

    # AutoCARB.rapporto_aria_benzina(20, 101325, 40, 13325, 0.042, 0.02, 0.019, 0.019, 0.017, 0.045, 0.00097, 50, 0.002)
    app_carb = MainApp()
    app_carb.title = "AutoCARB"
    app_carb.run()
#    app = MyApp()
#    app.title = "Titolo della mia applicazione"
#    app.run()