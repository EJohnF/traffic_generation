import random
from threading import Thread
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, WebKit, GObject, Gdk
import time
from process_python_api import Logger, LError, LInfo
import subprocess

sites = [
"http://beetle-club.ru/",
"http://logan-mcv.com.ua/",
"http://www.caravelle-club.ru/",
"http://www.audiv8.ru/",
"http://volvo-club.lv/",
"http://www.jaguar-club.ru/",
"http://www.peugeot-crimea.com/",
"http://volvo-club.na.by/forum",
"http://bmwfanatics.ru/forumvb",
"http://www.alfisti.by/",
"http://citroen-russia.ru/",
"http://volvo-club.kz/",
"http://www.mbclub.kz/",
"http://www.porsche-club.com.ua/forum",
"http://audi80b2.ru/",
"http://opel-rostov.ru/",
"http://www.107klub.com/",
"http://www.vw-club.lv/",
"http://www.fiatclub.by/",
"http://www.SkodaClub-NN.ru/",
"http://bmwpmr.com/",
"http://clublaguna.ru/",
"http://www.audispravka.ru/",
"http://www.opeltigra.ru/",
"http://peugeot205.org/",
"http://virusalfa.at.ua/",
"http://www.bravoclub.ru/",
"http://audiclub.co.il/",
"http://www.porsche-club-russland.ru/",
"http://www.fiatclub.ua/",
"http://www.gelik.ru/",
"http://www.roomster-club.ru/",
"http://www.bmwclubrussia.ru/",
"http://opelrekord.ru/",
"http://www.audi200-club.com/",
"http://www.renault-dacia.com.ua/",
"http://www.bmw55.info/",
"http://b6club.ru/",
"http://volkswagen-golf.kz/",
"http://www.mbclub.by/",
"http://Duster.ru/",
"http://vagbel.com/",
"http://www.seat-club.kiev.ua/",
"http://www.club-espace.ru/",
"http://SmartClub.by/",
"http://www.audi80.ru/",
"http://www.audi-bel.com/",
"http://www.Opel-Insignia.su/",
"http://www.rover-club.by/",
"http://www.opelclub.ru/",
"http://www.minipeople.ru/",
"http://scirocco.ru/",
"http://www.renault-club.kiev.ua/",
"http://seat-club.net/",
"http://www.astra-club.ru/",
"http://www.bmwclub.nnov.ru/",
"http://mokka-club.com/",
"http://www.Touran-Club.ru/",
"http://www.octavia-club.ru/forum",
"http://bmwpower-msk.ru/",
"http://www.volkswagen.lviv.ua/",
"http://www.peugeot-citroen.by/",
"http://DusterClub.ru/",
"http://tavria-auto.narod.ru/",
"http://www.audipiter.ru/",
"http://forum.tiguans.ru/",
"http://jetta-club.org/",
"http://peugeot-citroen.net/",
"http://www.308-club.ru/",
"http://www.bmwland.ru/",
"http://as8.ru/",
"http://www.calibra-club.ru/",
"http://m-power.ru/",
"http://Megane2.ru/",
"http://forum.logan.ru/",
"http://peugeot-club.by/",
"http://www.bmw-avtodom.ru/",
"http://www.MoscowVolvoClub.ru/",
"http://www.VolvoClub.ru/",
"http://Gti-club.ru/",
"http://www.BenzClub.ru/forum",
"http://fiat-club.org.ua/",
"http://www.skoda-club.dn.ua/",
"http://mercedes-club.org/",
"http://www.w201club.com/",
"http://audi-tt.ru/",
"http://www.golf-club.org.ua/",
"http://opc-club.ru/",
"http://www.audi.org.ua/",
"http://forum.opelclub-by.com/",
"http://www.geelygroup.com.ua/",
"http://www.chery-club.spb.ru/",
"http://www.fora-club.ru/",
"http://www.bmwclub.ru/",
"http://www.audi-club.ru/",
"http://vwts.ru/",
"http://www.skoda-club.ru/",
"http://passat-b5.ru/",
"http://b-m-w.ru/",
"http://AstraClub.ru/",
"http://www.opel-club.com.ua/",
"http://lr-club.com/",
"http://clubvolvo.ru/",
"http://www.bmwclub.ua/",
"http://www.vw-golfclub.ru/",
"http://www.E30Club.ru/",
"http://www.OldMerin.net/"]
view = WebKit.WebView()
prevFinished = True
number = 0

def fin():
    print("finish")
    global prevFinished
    prevFinished = True

view.connect("load-finished", lambda v, f: fin())

def main_loop():
    time.sleep(3)
    global prevFinished
    global view, number
    waiting = 0
    while True:
        # Setting a random value for the fraction
        # print(prevFinished)
        print(prevFinished, waiting)
        # if waiting > 10:
        #     Gdk.threads_enter()
        #     view.stop_loading()
        #     Gdk.threads_leave()
        if prevFinished:
            waiting = 0
            print(sites[number])
            prevFinished = False
            Gdk.threads_enter()
            view.open(sites[number])
            Gdk.threads_leave()
            number += 1
        # Releasing the gtk global mutex
        waiting+=1
        time.sleep(1)


# view = WebKit.WebView()
# sw = Gtk.ScrolledWindow()


# win = Gtk.Window()
# win.add(sw)
# win.show_all()
# view.open("https://panopticlick.eff.org")
# Gtk.main()