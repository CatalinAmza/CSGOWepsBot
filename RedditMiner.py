from threading import Thread
from constants import *
import os
import time
import requests


class RedditMiner(Thread):
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        try:
            file = open(LAST_THREAD_FILE, "r")
            if int(time.time() - os.stat(LAST_THREAD_FILE).st_mtime)/3600 > 7:
                raise Exception(OLD_FILE)
        except:
            self.last_thread = -1
        else:
            self.last_thread = file.read().strip()
            file.close()
        if self.last_thread == -1:
            self.get_new_thread()

    def get_new_thread(self):
        i = 0
        valid_content = False
        while i < REDDIT_RETRY_LIMIT and not valid_content:
            try:
                page_source = requests.get(REDDIT_HOT_PAGE, headers=REDDIT_HEADER).content.decode()
                if "developers" in page_source:
                    raise Exception(TIMEOUT_OF_DEATH)
            except Exception as error:
                print(error)
                page_source = -1
            else:
                time.sleep(REDDIT_TIMEOUT)
                valid_content = True
                print(REDDIT_HOT_PAGE + LOAD_SUCCESS)
            time.sleep(REDDIT_TIMEOUT)
            i += 1
        if page_source != -1:
            result = []
            for i in range(REDDIT_HOT_THREADS + REDDIT_OFFSET_1):
                start = page_source.find(REDDIT_TIME_QUEUE) + len(REDDIT_TIME_QUEUE)
                page_source = page_source[start:]
                end = page_source.find(REDDIT_TIME_END)
                if i > 0:
                    try:
                        thread_start = page_source.find(REDDIT_THREAD_QUEUE) + len(REDDIT_THREAD_QUEUE)
                        age = int(page_source[: end])
                        if age > 7:
                            age = -1
                        result.append([age, page_source[thread_start: thread_start + REDDIT_THREAD_LENGTH]])
                        page_source = page_source[end:]
                    except:
                        page_source = page_source[1:]
                        result.append([-1, REDDIT_NULL_TEMPLATE])
            result.sort(key=lambda x: x[0])
            self.last_thread = result[-1][1]

    def get_url(self):
        return REDDIT_THREAD_HEAD + self.last_thread

    def save(self):
        try:
            os.remove(LAST_THREAD_FILE)
        except:
            ()
        file = open(LAST_THREAD_FILE, "w")
        file.write(self.last_thread)
        file.close()

    def get_page_source(self):
        i = 0
        while i < REDDIT_RETRY_LIMIT:
            try:
                page_source = requests.get(self.get_url(), headers=REDDIT_HEADER).content.decode()
                if REDDIT_ERROR in page_source:
                    print(page_source)
                    raise Exception(TIMEOUT_OF_DEATH)
            except Exception as error:
                print(error)
            else:
                time.sleep(REDDIT_TIMEOUT)
                print(self.get_url() + LOAD_SUCCESS)
                return page_source
            time.sleep(REDDIT_TIMEOUT)
            i += 1
        return -1

    def mine_page(self):
        page_source = self.get_page_source()
        if page_source == -1:
            print(REDDIT_ERROR_MSG)
            return False
        else:
            source_copy = page_source
            start = 0
            while start != -1 + len(REDDIT_ID_QUEUE):
                start = page_source.find(REDDIT_ID_QUEUE) + len(REDDIT_ID_QUEUE)
                if start != -1 + len(REDDIT_ID_QUEUE):
                    end = page_source[start:].find(REDDIT_ID_END)
                    y = page_source[start:start + end]
                    if "/" in y:
                        print("Slash found (RedditMiner/mine_page/")
                        y = y.replace("/", "")
                    self.tasks.put(y)
                    page_source = page_source[start + end:]
            start = 0
            for i in range(REDDIT_TRICK_1):
                value = source_copy[start:].find(REDDIT_THREAD_QUEUE)
                start = start + value + len(REDDIT_THREAD_QUEUE)
            if value != -1:
                self.last_thread = source_copy[start: start + REDDIT_THREAD_LENGTH]
            if source_copy.count(REDDIT_THREAD_QUEUE) != REDDIT_THREAD_QUEUE_DEFAULT_COUNT:
                print("count: %s" % source_copy.count(REDDIT_THREAD_QUEUE))
                print("Maybe new reddit mod changes")
            return source_copy.count(REDDIT_THREAD_QUEUE) == REDDIT_THREAD_QUEUE_DEFAULT_COUNT

    def run(self):
        while self.mine_page():
            ()
        self.save()
