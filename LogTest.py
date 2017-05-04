from process_python_api import Logger, LError, LInfo
import time
Logger.init("Tester")
while True:
    Logger.log(LInfo, "sleep 5 something")
    Logger.log(LInfo, "sleep 4")
    time.sleep(2)