from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.label import MDLabel

# from kivy.core.window import Window
# # Window.softinput_mode = 'pan'
# Window.size = (400,300)

import AutoCARB
import numpy as np
import webbrowser

# from kivy.metrics import dp
# from kivymd.uix.menu import MDDropdownMenu

# Builder.load_file('credits.kv') # serve per importare il file *.kv



#################################################################################################
from kivy.uix.boxlayout import BoxLayout
# from kivy.properties import StringProperty, ListProperty

# from kivymd.theming import ThemableBehavior
# from kivymd.uix.list import OneLineIconListItem, MDList
from kivy.uix.popup import Popup
from kivy.uix.image import Image

from kivymd.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty

from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
import os

aperto=False #inizializzo "aperto". Serve pe evitare di aprire tanti popup involontariamente (Jacopo non rompere)

class ContentNavigationDrawer(BoxLayout):
    pass
# class ItemDrawer(OneLineIconListItem):
    # icon = StringProperty()
    # text_color = ListProperty((1, 1, 1, 1))
# class DrawerList(ThemableBehavior, MDList):
#     def set_color_item(self, instance_item):
#         """Called when tap on a menu item."""

#         # Set the color of the icon and text for the menu item.
#         for item in self.children:
#             if item.text_color == self.theme_cls.primary_color:
#                 item.text_color = self.theme_cls.text_color
#                 break
#         instance_item.text_color = self.theme_cls.primary_color
#################################################################################################
# from kivy.uix.textinput import TextInput
# class LimitInput(TextInput):
#     def insert_text(self, substring, from_undo=False):
#         if not self.filled:
#             return super(IdeaInput, self).insert_text(substring, from_undo=from_undo)
            

    # def on_text(self, instance, value):
    #     if len(self.text.strip()) >= 6:
    #         self.readonly = False

from kivy.clock import Clock

class AutoCARB_app(MDApp):
    def refresh_callback(self, *args):
        
        def refresh_callback(interval): #fake refresh
            # self.start_button()
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

    #################################################################################################
    # def on_start(self):
    #     icons_item = {
    #         "folder": "My files",
    #         "account-multiple": "Shared with me",
    #         "star": "Starred",
    #         "history": "Recent",
    #         "checkbox-marked": "Shared with me",
    #         "upload": "Upload",
    #     }
    #     for icon_name in icons_item.keys():
    #         self.root.ids.content_drawer.ids.md_list.add_widget(
    #             ItemDrawer(icon=icon_name, text=icons_item[icon_name])
    #         )
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

    def dialog_error(self,shown_text):

        if not self.dialog:

            dialog = MDDialog(
                #FF5050 B380FF
                title='[color=BE3636]ERROR[/color]',
                text=shown_text,
                # text= 'Invalid input values. Refer to User Manual for further informations.', 
                
                radius=[20, 20, 20, 20],

                buttons = [

                    MDFlatButton(

                        text="Close", text_color=self.theme_cls.primary_color, on_press=lambda x: dialog.dismiss(force=True)
                    )
                ]
            )

        # dialog.bind(on_dismiss=self.close_error) #nel caso in cui si dovesse fare qualcosa alla chiusura

        dialog.open()

    # def close_error(self, *args): #nel caso in cui si dovesse fare qualcosa alla chiusura

    #     dialog.dismiss(force=True)

    #     print("close")

    #---------------------------------------------------------------------------------------------------------------------------------------------


    # credits = ObjectProperty(None)
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
Antipatico and Alessio Lei

The splash page and the icon are edited by:
Roberta Carlevaris

Contact: app.autocarb@gmail.com
            ''',
                        padding_x=20,
                        markup = True,
                        # size_hint=(None, None),
                        # text_size = self.texture_size,
                        # font_style='H6',
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
                    # title_size='14sp',
                    #  size=(400, 400)
                     )
        btn.bind(on_press=pop.dismiss)
        # btn.bind(on_press=self.check_pop_open)
        pop.bind(on_dismiss=self.check_pop_open)
        aperto=True
        pop.open()
        return 
        
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
        # with open('inputs_startup.txt') as inputs:
        #     entries=[line.rstrip() for line in inputs]
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

    def start_button(self):
        if float(self.root.ids["temp"].text)>50:
            self.dialog_error('''
The temperature value is too high and
generates a bad interplation in the absolute humidity calculations.
To avoid errors, when the ambient temperature of 50 ° C the humidity value will be considered zero.'''
            )
        try:
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
        # except (TypeError, IndexError, UnboundLocalError):
        except:
            self.dialog_error('Invalid input values. Refer to User Manual for further informations.')
            return

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