import gtk 
import webkit 

view = webkit.WebView() 
sw = gtk.ScrolledWindow() 
sw.add(view) 

view.open("http://tinkoff.ru/") 
gtk.main()
