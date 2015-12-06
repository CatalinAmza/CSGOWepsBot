from threading import Thread
from Log import Log
from constants import *
import requests
import os
from time import sleep


class LoungeMiner(Thread):
    def __init__(self, tasks):
        self.tasks = tasks
        Thread.__init__(self)
        self.searches = Log(SEARCHES_FILE, separator=SEPARATOR)
        print(SEARCHES_HEADER)
        self.searches.log.sort(key=lambda x: x[0])
        self.searches.create_printable()
        for i in range(len(self.searches.text)):
            print(str(i) + ". " + self.searches.text[i])
        self.get_demand()
        self.session = requests.Session()
        self.session.cookies.update(LOUNGE_COOKIE)

    @staticmethod
    def trim_name(weapon_name):
        key = weapon_name.replace(" |", "")
        key = key.replace(" 龍王", "")
        key = key.replace("™", "")
        key = key.replace("★", "")
        key = key.replace(" 弐", "")
        key = key.replace(" 壱", "")
        key = key.strip(" \n")
        return key

    def get_demand(self):
        print(LOUNGE_MINER_ITEM_CHOICE)
        item_name = input(INPUT_PROMPT_MSG)
        try:
            self.item_name = self.searches.log[int(item_name)][0]
            self.url = self.searches.log[int(item_name)][1]
        except:
            self.item_name = LoungeMiner.trim_name(item_name)
            print(LOUNGE_MINER_MSG)
            self.url = input(INPUT_PROMPT_MSG)
            self.searches.add([ self.item_name, self.url])
        try:
            os.remove(SEARCHES_FILE)
        except:
            ()
        searches = open(SEARCHES_FILE, "w")
        self.searches.create_printable()
        searches.write(self.searches.__str__())
        searches.close()

    def get_page_source(self, url):
        i = 0
        while i < LOUNGE_RETRY_LIMIT:
            try:
                    page_source = self.session.get(url).content.decode()
                    if LOUNGE_ERROR in page_source:
                        raise Exception(LOUNGE_ERROR)
            except Exception as error:
                print(error)
            else:
                print(url + LOAD_SUCCESS)
                return page_source
            i += 1
        return -1

    def mine_lounge(self):
        print(LOUNGE_MINER_START + self.item_name + ".")
        for i in range(1, 21):
            print(LOUNGE_PAGE_HEAD + str(i) + LOUNGE_PAGE_TAIL)
            page_source = self.get_page_source(self.url + LOUNGE_CONNECTER + str(i))
            x=page_source
            start = 0
            have_threads = False
            while start != -1 + len(LOUNGE_THREAD_ID_QUEUE):
                start = page_source.find(LOUNGE_THREAD_ID_QUEUE) + len(LOUNGE_THREAD_ID_QUEUE)
                if start != -1 + len(LOUNGE_THREAD_ID_QUEUE):
                    have_threads = True
                    end = page_source[start:].find(LOUNGE_THREAD_ID_END)
                    thread_id = page_source[start:start + end]
                    thread = self.get_page_source(LOUNGE_THREAD_HEAD + thread_id)
                    position = thread.find(LOUNGE_ID_QUEUE) + len(LOUNGE_ID_QUEUE)
                    length = thread[position:].find(LOUNGE_ID_END)
                    if "meta" in thread[position: position + length]:
                        print(x)
                    y = thread[position: position + length]
                    if "/" in y:
                        print("Slash found (LoungeMiner/mine_lounge/")
                        y = y.replace("/", "")
                    self.tasks.put(y)
                    page_source = page_source[start + end:]
            if have_threads:
                print(LOUNGE_PAGE_SUCCESSFUL_HEAD + str(i) + LOUNGE_PAGE_SUCCESSFUL_TAIL)
            else:
                print(LOUNGE_DONE_HEAD + str(i-1) + LOUNGE_DONE_TAIL)
                break
            sleep(LOUNGE_TIMEOUT)

    def run(self):
        self.mine_lounge()
