import gtk
import webkit

view = webkit.WebView()
sw = gtk.ScrolledWindow()
sw.add(view)

def open_page(link):
    view.open(link)
    gtk.main()

# win = gtk.Window(gtk.WINDOW_TOPLEVEL)
# win.add(sw)
# win.show_all()

