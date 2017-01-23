#include <iostream>
#include <boost/thread.hpp>
#include <boost/chrono.hpp>
#include <gtkmm.h>
#include <webkit2/webkit2.h>
using namespace std;

static void load_finished_cb(WebKitWebView *web_view, gpointer data)
{
    std::cout<<"some event happen" << endl;
}



WebKitWebView * one;

void global()
{
    cout<<"New thread" << endl;
    g_signal_connect(one, "load-changed", G_CALLBACK(load_finished_cb), NULL);

//    webkit_web_view_load_uri(one, "http://rzd.ru");
//    cout<<"opened rzd" << endl;
//    boost::this_thread::sleep_for (boost::chrono::seconds(15));
//    webkit_web_view_load_uri(one, "https://google.com");
//    cout<<"opened google" << endl;
    boost::this_thread::sleep_for (boost::chrono::seconds(3));
//    webkit_web_view_load_uri(one, "http://vk.com");
//    cout<<"opened vk";
}

int main( int argc, char **argv)
{
  Glib::RefPtr<Gtk::Application> app = Gtk::Application::create( argc, argv, "" );

  Gtk::Window window;
  window.set_default_size( 800, 600 );

  WebKitSettings * settings;
  settings = webkit_settings_new ();

  webkit_settings_set_user_agent(settings, "Some string for user Agent. Bla-bla-blaa. Hello for Alex ;-) ");

  one =  WEBKIT_WEB_VIEW( webkit_web_view_new() );

  webkit_web_view_set_settings(one, settings);
  Gtk::Widget * three = Glib::wrap( GTK_WIDGET( one ) );

  window.add( *three );
  webkit_web_view_load_uri(one, "http://rzd.ru");

  boost::thread * t;
  t = new boost::thread(&global);
  boost::this_thread::sleep_for (boost::chrono::seconds(1));

  window.show_all();
  t->join();
  app->run( window );
  exit( 0 );
}


int main_2()
{
    boost::thread * t;
    t = new boost::thread(&global);
    for (int i = 0; i<50; i++){
        cout<< "main " << i << endl;
    }
    boost::this_thread::sleep_for (boost::chrono::seconds(5));
    return 0;
}