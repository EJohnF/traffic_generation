import getopt
import json
import sys
import utils


def main(argv):
    configFile = ''
    try:
        opts, args = getopt.getopt(argv, "hc:", ["config=", "configuration="])
    except getopt.GetoptError:
        print 'MainLoop.py -c <configFile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'MainLoop.py -c <configFile>'
            sys.exit()
        elif opt in ("-c", "--config", "--configuration"):
            configFile = arg

    if configFile == '':
        configFile = 'configuration.json'

    print 'Config file is ', configFile

    f = open(configFile, 'r')
    config = json.load(f)
    utils.parser_site_list(config['sites'], config)

if __name__ == "__main__":
    main(sys.argv[1:])
