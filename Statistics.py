from process_python_api import Logger, LError, LInfo
load_time_list = []
process_site_list = []
sleep_time_list = []


def load_page(url, time):
    load_time_list.append((url, time))


def process_site(url, pages_list):
    process_site_list.append((url, pages_list))


def sleep_time(url, time):
    sleep_time_list.append((url, time))


def output_statistics():
    for page in load_time_list:
        print(page)
    Logger.log(LInfo, "")
