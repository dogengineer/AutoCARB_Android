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


class AutoCARB_app(MDApp):


    def build(self):
        self.title = "AutoCARB"
        self.theme_cls.theme_style = "Dark"  # "Light"
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.primary_hue = "300"
        return Builder.load_file("AutoCARB_layout.kv")
    

    def help_button(self):
        webbrowser.open_new('https://drive.google.com/drive/folders/1Jhl9PxwQLWuTAZI_e3_Zsp0LWXrp-Qie')

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
    
    #-----------------------Gestione Errori----------------------------------------------------------------#
    
    dialog=None

    def dialog_error(self):

        if not self.dialog:

            dialog = MDDialog(
                #FF5050 B380FF
                title='[color=BE3636]ERROR[/color]',

                text= 'Invalid input values. Refer to User Manual for further informations.', 
                
                radius=[20, 20, 20, 20],

                buttons = [

                    MDFlatButton(

                        text="close", text_color=self.theme_cls.primary_color, on_press=lambda x: dialog.dismiss(force=True)
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
Alessio Lei and Scorbutico 

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
        else:
            self.theme_cls.theme_style = "Dark"
            self.root.ids['btt_layout'].panel_color = (.2, .2, .2, 1)

    def licence_button(self):
        webbrowser.open_new('https://github.com/dogengineer/AutoCARB_Android/blob/main/LICENSE')

    def donation_button(self):
        webbrowser.open_new('https://www.paypal.com/paypalme/DavideMaieron') 

    def code_button(self):
        webbrowser.open_new('https://github.com/dogengineer/AutoCARB_Android') 
        
    #################################################################################################     

    def start_button(self):

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
            self.dialog_error()
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