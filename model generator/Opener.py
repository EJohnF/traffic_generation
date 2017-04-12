import random
from threading import Thread
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, WebKit
import time
from process_python_api import Logger, LError, LInfo
import subprocess

#Logger.init("Opener")

def open_page(link):
    print('open link', link)
    subprocess.Popen('python3 open.py ' + link, shell=True)
