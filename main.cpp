#include <iostream>
#include <boost/thread.hpp>
#include <boost/chrono.hpp>
#include <gtkmm.h>
#include <webkit2/webkit2.h>
#include <stdlib.h>
#include <stdio.h>
#include <pcap.h>
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

void generate_queries( int argc, char **argv)
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
}

void work_with_packets()
{
    pcap_t *fp;
    char errbuf[PCAP_ERRBUF_SIZE];
    u_char packet[100];
    int i;
    std::cout<<"try to open device";
        /* Open the output device */
        if ( (fp= pcap_open_live("wlan0",            // name of the device
                            100,                // portion of the packet to capture (only the first 100 bytes)
                            0,
                            1000,               // read timeout
                            errbuf              // error buffer
                            ) ) == NULL)
        {
            fprintf(stderr,"\nUnable to open the adapter. is not supported by WinPcap\n");
            return;
        }

        /* Supposing to be on ethernet, set mac destination to 1:1:1:1:1:1 */
        packet[0]=224;
        packet[1]=172;
        packet[2]=203;
        packet[3]=122;
        packet[4]=104;
        packet[5]=10;

        /* set mac source to 2:2:2:2:2:2 */
        packet[6]=204;
        packet[7]=82;
        packet[8]=175;
        packet[9]=151;
        packet[10]=131;
        packet[11]=217;

        /* Fill the rest of the packet */
        for(i=12;i<100;i++)
        {
            packet[i]=i%256;
        }

        /* Send down the packet */
        for (i=0; i< 100; i++)
        {
            if (pcap_sendpacket(fp, packet, 100 /* size */) != 0)
            {
                fprintf(stderr,"\nError sending the packet: \n", pcap_geterr(fp));
                return;
            }
        }

        return;
}

int main( int argc, char **argv)
{
//    generate_queries (argc, argv);
    work_with_packets();
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
