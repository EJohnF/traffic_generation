# import gtk
# import webkit
# from threading import Thread
#
# view = webkit.WebView()
# sw = gtk.ScrolledWindow()
# sw.add(view)
#
#
# def thread_open():
#     gtk.main()
#
#
# threadList = []
#
#
# def open_page(link):
#     print 'open_page', link
#     # view.open("http://www."+link)
#     view.open(link)
#     thread = Thread(target=thread_open, args=( ))
#     thread.setDaemon(True)
#     thread.start()
#     threadList.append(thread)


def open_page(link):
    print 'open_page', link
