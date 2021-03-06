import getopt
import json
import sys
import subprocess
import time
import os
import signal
from process_python_api import Logger, LError, LInfo
Logger.init("Launcher")
import argparse

process = ''

def main(argv):
    parser = argparse.ArgumentParser(description='The script for launch generators')
    parser.add_argument("-c", help='a configuration of system to be launched', metavar='configuration', dest='config',
                        default='config/track.json')
    arguments = parser.parse_args(argv)

    f = open(arguments.config, 'r')
    config = json.load(f)
    global process
    for proc in config['processes']:
        launched_string = 'python3 Generator.py ' + '-n ' + proc['name'] + ' -c ' + proc['config']
        Logger.log(LInfo, "new_process 0 {}".format(proc['name']))
        Logger.log(LInfo, "launched_string 0 {}".format(launched_string))
        process = subprocess.Popen(launched_string, shell=True)
    time.sleep(config['time_to_live'])

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Interrupted')
