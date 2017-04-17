import gtk 
import webkit 

view = webkit.WebView() 
sw = gtk.ScrolledWindow() 
sw.add(view) 

win = gtk.Window(gtk.WINDOW_TOPLEVEL) 
win.add(sw) 
win.show_all() 

# settings = webkit.WebSettings()
# settings.set_property("user-agent", 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0')
# settings.set_property("Accept-Language", "ru-ru")
# view.set_settings(settings)

view.open("https://panopticlick.eff.org")
gtk.main()
