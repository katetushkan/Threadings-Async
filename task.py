import datetime
import os
import threading

import requests
from lxml import html

DOWNLOAD_URL = 'https://www.countryflags.io'
DOWNLOAD_DIR = './flags'


class Flag:

    def __init__(self, flag_url, flag_name):
        self.flag_url = flag_url
        self.flag_name = flag_name


def flag_download_path_forming():

    flags_info = html.fromstring(requests.get(DOWNLOAD_URL).content)
    flags_id = flags_info.xpath('//div[@class="item_country cell small-4 medium-2 large-2"]')

    flags = list()
    for item_id in flags_id:
        child = item_id.getchildren()
        flags.append(Flag(child[0].attrib['src'], child[2].text))

    return flags


def download_single_flag(flag):
    source = requests.get(DOWNLOAD_URL + flag.flag_url).content
    image = '{}.png'.format(flag.flag_name)
    path = os.path.join(DOWNLOAD_DIR, image)

    with open(path, 'wb') as file:
        file.write(source)


def simple_download():
    flags = flag_download_path_forming()
    for flag in flags:
        download_single_flag(flag)


def multipal_thread_download():
    flags = flag_download_path_forming()

    threads = []
    for flag in flags:
        thread = threading.Thread(target=download_single_flag, kwargs={'flag': flag})
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    multipal_thread_download_start = datetime.datetime.now()
    multipal_thread_download()
    print(datetime.datetime.now() - multipal_thread_download_start)

    simple_download_start = datetime.datetime.now()
    simple_download()
    print(datetime.datetime.now() - simple_download_start)