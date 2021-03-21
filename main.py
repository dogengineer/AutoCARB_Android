#import kivy # Importa il package "kiwi", che contiene tanti moduli
#from kivy.app import App # Dal modulo "kiwi.app" importa la classe "App"
#from kivy.uix.label import Label # Dal modulo "kiwi.uix.label" importa la classe "Label"

import AutoCARB

#class MyApp(App): # Definisco la classe MyApp che eredita da App
#    def build(self): # Ri-definisco il metodo build
#        return Label(text='Hello world')


if __name__ == '__main__': # non eseguire se vieni importato come libreria
    AutoCARB.cp_air_interp(20)

    AutoCARB.Coefficiente_efflusso_aria(20, 101325, 13325, 0.042, 0.02, 0.019, 0.019)

    #AutoCARB.portata_benzina()

    AutoCARB.rapporto_aria_benzina(20, 101325, 40, 13325, 0.042, 0.02, 0.019, 0.019, 0.017, 0.045, 0.00097, 50, 0.002)
#    app = MyApp()
#    app.title = "Titolo della mia applicazione"
#    app.run()