#import kivy # Importa il package "kiwi", che contiene tanti moduli
from kivy.properties import ObjectProperty
from kivy.app import App # Dal modulo "kiwi.app" importa la classe "App"
from kivy.uix.boxlayout import BoxLayout # Dal modulo "kiwi.uix.label" importa la classe "Label"


import AutoCARB

class MainWindow(BoxLayout):
    submit_button = ObjectProperty(None)
    nome = ObjectProperty(None)
    cognome = ObjectProperty(None)
    data_di_nascita = ObjectProperty(None)
    luogo_di_nascita = ObjectProperty(None)
    def invia_form(self):
        AF=AutoCARB.rapporto_aria_benzina(float(self.nome.text), 101325, 40, 13325, 0.042, 0.02, 0.019, 0.019, 0.017, 0.045, 0.00097, 0.002)
        self.cognome.text = AF
        #self.nome.text per chiamare il testo dentro il campo nome
        

class MainApp(App):
    def build(self):
        return MainWindow()




if __name__ == '__main__': # non eseguire se vieni importato come libreria
    # AutoCARB.cp_air_interp(20)

    # AutoCARB.Coefficiente_efflusso_aria(20, 101325, 13325, 0.042, 0.02, 0.019, 0.019)

    #AutoCARB.portata_benzina()

    # AutoCARB.rapporto_aria_benzina(20, 101325, 40, 13325, 0.042, 0.02, 0.019, 0.019, 0.017, 0.045, 0.00097, 50, 0.002)
    sample_app = MainApp()
    sample_app.run()
#    app = MyApp()
#    app.title = "Titolo della mia applicazione"
#    app.run()