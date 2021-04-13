import os
import webbrowser
from enum import Enum
import numpy as np
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivymd.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
import AutoCARB
from AutoCARB import MixtureType
from AutoCARBErrors import *

aperto=False #inizializzo "aperto". Serve pe evitare di aprire tanti popup involontariamente (Jacopo non rompere)

class DialogType(Enum):
    Error = 0
    Warning = 1

class ContentNavigationDrawer(BoxLayout):
    pass

from kivy.clock import Clock

class AutoCARB_app(MDApp):
    def refresh_callback(self, *args):
        
        def refresh_callback(interval): #fake refresh
            self.root.ids['refresh'].refresh_done()

        Clock.schedule_once(refresh_callback,0)


    def build(self):
        self.title = "AutoCARB"
        self.theme_cls.theme_style = "Dark"  # "Light"
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.primary_hue = "300"
        return Builder.load_file("AutoCARB_layout.kv")
    

    def help_button(self):
        webbrowser.open_new('https://drive.google.com/drive/folders/1R0lzU6_zJvO-YX1yDZe_P2RxIkCc_qsJ?usp=sharing')
    
    
    def on_start(self):
        if os.path.exists('inputs_saved.txt'):
            with open('inputs_saved.txt') as inputs:
                entries=[line.rstrip() for line in inputs]
                self.root.ids["temp"].text=entries[0]
                self.root.ids["pressione"].text=entries[1]
                self.root.ids["phi"].text=entries[2]
                self.root.ids["dpressione"].text=entries[3]
                self.root.ids["d1"].text=entries[4]
                self.root.ids["d3"].text=entries[5]
                self.root.ids["d2min"].text=entries[6]
                self.root.ids["d2max"].text=entries[7]
                self.root.ids["hc"].text=entries[8]
                self.root.ids["hd"].text=entries[9]
                self.root.ids["dgetto"].text=entries[10]
                self.root.ids["lcd"].text=entries[11]


    #-----------------------Gestione Errori----------------------------------------------------------------#
    
    dialog=None

    def dialog_error(self,type: DialogType,message):
        '''
        Arguments:
            type: a DialogType enum either Error or Warning, defining the type of the dialog.
            message: text shown in the popup
        '''
        if self.dialog is None:
            if type == DialogType.Error:
                title = '[color=BE3636]ERROR[/color]'
            if type == DialogType.Warning:
                title = '[color=ff8c00]WARNING[/color]'
            dialog = MDDialog(
                title=title,
                text=message,
                radius=[20, 20, 20, 20],
                buttons = [
                    MDFlatButton(
                        text="Close", text_color=self.theme_cls.primary_color, on_press=lambda x: dialog.dismiss(force=True)
                    )
                ]
            )
        dialog.open()

    def credits_button(self):
        global aperto
        if aperto == True:
            return
        content = GridLayout(rows=2)
        content.add_widget(MDLabel(
                        text='''
This application acts as a support for the regulation of 
the carburetion of internal combustion engines.

[b]AutoCARB[/b] was developed by:
Davide Maieron and Adriano Mazzola 

With the collaboration of:
antipatico and Alessio Lei

The splash page and the icon are edited by:
Roberta Carlevaris

Contact: app.autocarb@gmail.com
            ''',
                        padding_x=20,
                        markup = True,
                        theme_text_color="Custom",
                        text_color=( 0.7, 0.5, 1, 1))
                        )
        btn=Button(text="CLOSE",
                    size_hint_y=None
                    )                            
        content.add_widget(btn)
        pop = Popup(title='Credits',
                    content=content,
                    auto_dismiss=True,
                    size_hint=(1, 1),
                    separator_color= [0.7, 0.5, 1, 0.6],
                    separator_height='5dp',
                    title_align='center',
                     )
        btn.bind(on_press=pop.dismiss)
        pop.bind(on_dismiss=self.check_pop_open)
        aperto=True
        pop.open()
        return 

    def easter_egg(self):
        global aperto
        if aperto == True:
            return
        content = GridLayout(rows=2)
        content.add_widget(Image(source='./media/hot_af.jpg')
                        )
        pop = Popup(title='Even the beans are too HOT!',
                    content=content,
                    auto_dismiss=True,
                    size_hint=(.9, .45),
                    separator_color= [0.7, 0.5, 1, 0.6],
                    separator_height='1dp',
                    title_align='center',
                     )
        pop.bind(on_dismiss=self.check_pop_open)
        aperto=True
        pop.open()
        return     
    
    # THe following is the worst piece of code I have ever witnessed - antipatico
    def check_pop_open(self,istance):
        global aperto
        aperto=False

    def theme_change(self):
        if self.theme_cls.theme_style == "Dark":
            self.theme_cls.theme_style = "Light"
            self.root.ids['btt_layout'].panel_color = (255/255, 255/255, 255/255, 1)
            self.root.ids['img_drawing'].source = "./media/drawing_light.jpg"
        else:
            self.theme_cls.theme_style = "Dark"
            self.root.ids['btt_layout'].panel_color = (.2, .2, .2, 1)
            self.root.ids['img_drawing'].source = "./media/drawing.jpg"

    def licence_button(self):
        webbrowser.open_new('https://github.com/dogengineer/AutoCARB_Android/blob/main/LICENSE')

    def donation_button(self):
        webbrowser.open_new('https://www.paypal.com/paypalme/DavideMaieron') 

    def code_button(self):
        webbrowser.open_new('https://github.com/dogengineer/AutoCARB_Android') 

    def reset_entries(self):
        if os.path.exists('inputs_saved.txt'):
            os.remove('inputs_saved.txt')
        self.root.ids["temp"].text="20"
        self.root.ids["pressione"].text="101325"
        self.root.ids["phi"].text="40"
        self.root.ids["dpressione"].text="13325"
        self.root.ids["d1"].text="42"
        self.root.ids["d3"].text="20"
        self.root.ids["d2min"].text="19"
        self.root.ids["d2max"].text="19"
        self.root.ids["hc"].text="17"
        self.root.ids["hd"].text="45"
        self.root.ids["dgetto"].text="97"
        self.root.ids["lcd"].text="2"
       
    def save_entries(self):
        if os.path.exists('inputs_saved.txt'):
            os.remove('inputs_saved.txt')

        entries=list(range(12)) #inizializzo vettore

        entries[0]=self.root.ids["temp"].text
        entries[1]=self.root.ids["pressione"].text
        entries[2]=self.root.ids["phi"].text
        entries[3]=self.root.ids["dpressione"].text
        entries[4]=self.root.ids["d1"].text
        entries[5]=self.root.ids["d3"].text
        entries[6]=self.root.ids["d2min"].text
        entries[7]=self.root.ids["d2max"].text
        entries[10]=self.root.ids["dgetto"].text
        entries[11]=self.root.ids["lcd"].text

        f=open('inputs_saved.txt','w')
        for item in entries:
            f.write("%s\n" % item)
        f.close()
    #################################################################################################     

    def parse_args(self):
        # Usiamo un dizionario e un ciclo per evitare di dover ripetere il codice.
        user_inputs = ["temp", "pressione", "phi", "dpressione", "d1", "d3", "d2max", "d2min", "d2max", "hc", "hd", "dgetto", "lcd"]
        args = dict() # Creo un dizionario, una struttura dati che dato un valore di chiave, ritorna un valore associato.
        for k in user_inputs:
            args[k] = float(self.root.ids[k].text) # Popolo il dizionario con i valori inseriti dall'utente
        return args
            

    def start_button(self):
        try:
            # Step 1: Acquisizione dell'input da parte dell'utente
            args = self.parse_args()
            for k in ["d1", "d3", "d2max", "d2min", "hc", "hd", "lcd"]:
                args[k] *= 1e-3 # Converto i valori all'interno del dizionario, moltiplicandoli per 0.0001
            args["dgetto"] *= 1e-5 # Questo è per 0.000001
            
            # Step 2: Validazione dell'input
            if args["phi"] > 100:
                raise HighHumidityError()

            # Step3: Calcolo del risultato
            # La prossima funzione torna 3 valori, e quindi salvo il risultato
            # in 3 variabili diverse. Per approfondire, cercare "tuple python"
            # Questo ci permette non solo di calcolare più volte il rapporto AF,
            # ma anche di scrivere meno codice / codice più elegante.
            AF, error, mixture_type = AutoCARB.rapporto_aria_benzina(args["temp"], args["pressione"], args["phi"],
                        args["dpressione"], args["d1"], args["d3"], args["d2max"], args["d2min"],
                        args["hc"], args["hd"], args["dgetto"], args["lcd"])

            # Step 4: Rappresentazione dei risultati e degli avvisi
            self.root.ids["af"].text = str(np.round(AF, decimals = 2))
            self.root.ids["err"].text = str(str(np.round(error, decimals = 2))+' %')
            self.root.ids["mixture_label"].text = str(mixture_type)
            if mixture_type == MixtureType.Rich or mixture_type == MixtureType.Lean:
                self.root.ids["mixture_label"].text_color = (255/255, 80/255, 80/255, 1)
            if mixture_type == MixtureType.Stoichiometric:
                self.root.ids["mixture_label"].text_color = (51/255, 153/255, 51/255, 1)
            if args["temp"] > 50:
                self.dialog_error(DialogType.Warning ,'''
The temperature value is too high and generates a bad interpolation in the absolute humidity calculations.
To avoid errors, when the ambient temperature is above 50 °C, the humidity value will be considered as zero.'''
                )
            if args["temp"] == 50:
                self.easter_egg()
            
        except HighHumidityError:
            self.dialog_error(DialogType.Error ,'Relative humidity value cannot be higher than 100%.')
        
        except MachError:
            self.dialog_error(DialogType.Error , 'Due to sonic or ultrasonic conditions in the Venuturi pipe, we cannot calculate the results.')
        
        except: # This is an horrible idea and SHOULD NOT BE DONE.
            self.dialog_error(DialogType.Error ,'Invalid input values.') 
            #the error window is shown in the case of any general error of the program


if __name__=="__main__":
    AutoCARB_app().run()