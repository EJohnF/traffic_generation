import getopt
import json
import sys
import subprocess
import time
import os
from process_python_api import Logger, LError, LInfo
Logger.init("Launcher")

def main(argv):
    config_file = ''
    try:
        opts, args = getopt.getopt(argv, "hc:", ["config=", "configuration="])
    except getopt.GetoptError:
        print('Launcher.py -c <trackFile>')
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print('Launcher.py -c <trackFile>')
            sys.exit()
        elif opt in ("-c", "--config", "--configuration"):
            config_file = arg

    if config_file == '':
        config_file = 'config/track.json'

    print('Config file is ', config_file)

    f = open(config_file, 'r')
    config = json.load(f)

    for proc in config['processes']:
        launched_string = 'python3 Generator.py ' + '-n ' + proc['name'] + ' -c ' + proc['config']
        Logger.log(LInfo, "launch new process {}".format(proc['name']))
        Logger.log(LInfo, "launched string {}".format(launched_string))
        subprocess.Popen(launched_string, shell=True)
    time.sleep(config['time_to_live'])

if __name__ == "__main__":
    main(sys.argv[1:])
