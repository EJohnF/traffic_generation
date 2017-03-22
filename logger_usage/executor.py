import sys
import subprocess
import json
import signal
import os
import time
from process_python_api import Logger, LError, LInfo


def main(config):
    executable = config.get("executable")
    name = config.get("name")
    arguments = config.get("arguments", [])

    if not name:
        Logger.init("Undefined executable")
        Logger.log(
            LError,
            "Can't get name for executable at {}, exiting".format(config_path))
        return -1
    else:
        Logger.init(name)

    if not executable:
        Logger.log(
            LError,
            "Can't get executable for executable at {}, exiting".format(
                config_path))
        return -1

    if not isinstance(arguments, (list,)):
        Logger.log(
            LError,
            "Can't incorrect arguments at {}: must be a list, exiting".format(
                config_path))
        return -1

    cmd = [executable] + arguments
    Logger.log(LInfo, "Starting '{}'".format(" ".join(cmd)))
    popen = subprocess.Popen(cmd)
    try:
        popen.wait()
    except KeyboardInterrupt:
        popen.send_signal(
            signal.SIGINT if os.name == 'posix'
            else signal.CTRL_C_EVENT)
        for _ in range(0, 10):
            if popen.poll() is None:
                time.sleep(0.15)
        if popen.poll() is None:
            print("Still running, trying to kill")
            popen.kill()
        Logger.log(LInfo, "'{}' stopped with return code {}".format(
            " ".join(cmd), popen.returncode))
    return popen.returncode

if __name__ == '__main__':
    config = {}
    config_path = sys.argv[1]
    if type(config_path) == str:
        with open(config_path) as c:
            config = json.load(c)
    main(config)
