from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.core.window import Window
from kivy.uix.button import Button
import json
from kivy.uix.label import Label
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.graphics import Color, Ellipse,Rectangle
from kivy.properties import ListProperty
Config.set("graphics","width","300")
Config.set("graphics","height","700")
from kivy.core.text import LabelBase
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.storage.jsonstore import JsonStore


class uygEkran(ScreenManager):
    pass
class Menu(Screen):
    pass

class Tbutton(Button):
    urls=None
class Tiyatrolar(Screen):
    def __init__(self, **kwargs):
        super(Tiyatrolar, self).__init__(**kwargs)


class Notlarim(Screen):
    def on_pre_enter(self, *args):
        Window.bind(on_request_close=self.kabulet)

    # popup için açılır pencere
    def kabulet(self, *args, **kwargs):
        global popapSes
        popapSes.play()  # çıkış popap sesi
        print('Aradığı')
        kutu = BoxLayout(orientation='vertical', padding=10, spacing=10)
        buton = BoxLayout(padding=10, spacing=10)

        açıl = Popup(title='Çıkmak istediğinden emin misin?', content=kutu, size_hint=(None, None),
                     size=(300, 180))
        evet = OvalButon(text='Evet', on_release=App.get_running_app().stop)
        hayır = OvalButon(text='Hayır', on_release=açıl.dismiss)

        buton.add_widget(evet)
        buton.add_widget(hayır)
        uyarı = Image(source='uyarı.png')

        kutu.add_widget(uyarı)
        kutu.add_widget(buton)

        animasyonText = Animation(color=(0, 0, 0, 1)) + Animation(color=(1, 1, 1, 1))
        animasyonText.repeat = True  # evet seçeneğini sürekli yanıp sönen iki renk yapar
        animasyonText.start(evet)
        animasyon = Animation(size=(300, 180), duration=0.2, t='out_back')
        animasyon.start(açıl)
        açıl.open()
        return True

class OvalButon(ButtonBehavior, Label):
#menüdeki butonkarın köşelerini oval yapmak için

    renk=ListProperty([0.1,0.5,0.7,1])
    renk2=ListProperty([1,1,0,1])
    def __init__(self, **kwargs):
        super(OvalButon,self).__init__(**kwargs)
        self.güncelle()
    def on_pos(self,*args):
        self.güncelle()
    def on_size(self,*args):
        self.güncelle()
    def on_press(self,*args):
        self.renk, self.renk2  =self.renk2, self.renk
    def on_renk(self,*args):
        self.güncelle()
    def on_release(self,*args):
        self.renk, self.renk2  =self.renk2, self.renk

    def güncelle(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=self.renk)
            Ellipse(size=(self.height, self.height),
                    pos=self.pos)
            Ellipse(size=(self.height, self.height),
                    pos=(self.x+self.width-self.height, self.y))
            Rectangle(size=(self.width-self.height,self.height),
                      pos=(self.x+self.height/2.0,self.y))
class Gorevler(Screen):
    gorevler=[] #verilerin tutuldupu liste
    path=''  #verilerin yolu
    #ekran animasyon başlat
    def on_pre_enter(self):
        #self.ids.box.claer_widgets()
        self.path = App.get_running_app().user_data_dir + '/'
        self.veriYükle()
        Window.bind(on_keyboard=self.geridonus)
        #gorevler listesi oluşturulduğu için for içindeki selfçgorevler yazıldı
        for gorev in self.gorevler:
            self.ids.box.add_widget(Gorev(text=gorev))

    def geridonus(self, window, key,*args):
        if key==27:
            App.get_running_app().root.current='not'
            return True
    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.geridonus)


    def veriYükle(self, *args):
        try:
            with open(self.path+'veriler.json','r') as veri:
                self.gorevler = json.load(veri)
        except FileNotFoundError:
            pass

    def veriKaydet(self, *args):
        with open(self.path+'veriler.json', 'w') as veri:
            json.dump(self.gorevler, veri)

    def kaldirWidget(self, gorev):
        global popapSes
        popapSes.play()
        textekle = gorev.ids.label.text
        self.ids.box.remove_widget(gorev)
        self.gorevler.remove(textekle)
        self.veriKaydet()

    def addWidget(self):
        global popSes
        popSes.play()
        textekle=self.ids.textekle.text
        self.ids.box.add_widget(Gorev(text=textekle))
        self.ids.textekle.text=''
        self.gorevler.append(textekle)
        self.veriKaydet()

class Gorev(BoxLayout):
    def __init__(self, text=' ',**kwargs):
        super().__init__(**kwargs)
        self.ids.label.text=text

class uygApp(App):
    def build(self):
        return uygEkran()

if __name__=='__main__':
    Window.clearcolor=(1,1,0,0)
    popSes = SoundLoader.load('pop.mp3') #mesaj gönderme sesi popsese atandı
    popapSes = SoundLoader.load('poppap.mp3') #mesaj silme sesini popapsese atandı
    uygApp().run()