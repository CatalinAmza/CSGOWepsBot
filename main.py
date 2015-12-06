import json
import time
from urllib.request import *
import requests
import os
import re
from threading import Thread
from queue import Queue
from constants import *
from Log import Log
from RedditMiner import RedditMiner
from LoungeMiner import LoungeMiner
from SteamMiner import SteamMiner
from best_wears import best_wears
from random import randrange


def parse_steam_id(steam_id):
    if steam_id == "":
        print("Mining the SteamID64: " + STEAM_ID + "\n")
        return STEAM_ID
    try:
        if "7656119" != steam_id[:7] or len(steam_id) != 17:
            raise Exception
        int(steam_id)
    except:
        raise Exception("Invalid SteamID64: " + steam_id + ".")
    else:
        return steam_id


def put_friends(steam_id, queue):
    page_source = requests.get(FRIENDS_URL_HEAD + API_KEY + FRIENDS_URL_TAIL + steam_id).content.decode()
    try:
        data = json.loads(page_source)
    except Exception as error:
        print(error, FRIENDS_URL_HEAD + API_KEY + FRIENDS_URL_TAIL + steam_id)
        print(page_source)
        return
    for index in range(len(data["friendslist"]["friends"])):
        queue.put(data["friendslist"]["friends"][index]["steamid"])
    queue.put(steam_id)


def choice_5():
    roots = []
    for file_name in os.listdir(os.getcwd() + "\\inventories"):
        roots.append(file_name[:-4])
    queue = Queue()
    for i in range(50):
        put_friends(roots[randrange(len(roots))], queue)
    blacklist = Log(BLACKLIST_FILE)
    x = SteamMiner(queue, blacklist, [])
    x.start()
    x.join()
    blacklist.save()


def choice_4():
    for file_name in os.listdir(os.getcwd() + "\\vault"):
        os.remove(os.getcwd() + "\\vault\\" + file_name)
    queue = Queue()
    for file_name in os.listdir(os.getcwd() + "\\inventories"):
        queue.put(file_name[:-4])
    blacklist = Log(BLACKLIST_FILE)
    for steam_id in blacklist.log:
        queue.put(steam_id)
    blacklist.replace_log([])
    x = SteamMiner(queue, blacklist, [])
    x.start()
    x.join()
    blacklist.save()


def choice_3():
    valid_id = False
    while not valid_id:
        input_id = input("Press \"Enter\" for your own inventory or paste the guy's SteamID64.\nSteamID64: ")
        try:
            steam_id = parse_steam_id(input_id)
        except Exception as error:
            print(error)
        else:
            valid_id = True
            queue = Queue()
            put_friends(steam_id, queue)
            blacklist = Log(BLACKLIST_FILE)
            x = SteamMiner(queue, blacklist, [])
            x.start()
            x.join()
            blacklist.save()


def choice_2():
    best_wears()
    steam_ids = Queue()
    blacklist = Log(BLACKLIST_FILE)
    thread_1 = LoungeMiner(steam_ids)
    thread_2 = RedditMiner(steam_ids)
    thread_3 = SteamMiner(steam_ids, blacklist, [thread_1, thread_2])
    thread_1.start()
    thread_2.start()
    thread_3.start()
    thread_1.join()
    thread_2.join()
    thread_3.join()
    blacklist.save()


def choice_1():
    valid_id = False
    while not valid_id:
        input_id = input("Press \"Enter\" for your own inventory or paste the guy's SteamID64.\nSteamID64: ")
        try:
            steam_id = parse_steam_id(input_id)
        except Exception as error:
            print(error)
        else:
            valid_id = True
            x = SteamMiner(Queue(), Log(), [])
            inventory = x.get_inventory(steam_id)
            if inventory != -1:
                inventory.log.sort(key=lambda y: float(y[1]))
                print(inventory)


def get_choice():
    choice = int(input(INPUT_PROMPT_MSG))
    if choice - 1 not in [i for i in range(len(OPTION_MSG))]:
        raise Exception
    return choice


def list_options():
    print(SPLITTER)
    for i in range(len(OPTION_MSG)):
        print(PRESS_MSG + "\"" + str(i + 1) + "\" " + OPTION_MSG[i])

def launch():
    list_options()
    valid_choice = False
    while not valid_choice:
        try:
            choice = get_choice()
        except:
            print(INVALID_MSG)
            print(SPLITTER)
        else:
            valid_choice = True
            print(SPLITTER)
            globals()[FUNCTION_NAME + str(choice)]()
            print(SPLITTER)

launch()
