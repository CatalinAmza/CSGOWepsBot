from threading import Thread
from constants import *
import requests
import os
from Log import Log
import json
from LoungeMiner import LoungeMiner
from best_wears import *
import time


class SteamMiner(Thread):
    def __init__(self, tasks, blacklist, dumpers):
        Thread.__init__(self)
        self.tasks = tasks
        self.dumpers = dumpers
        self.blacklist = blacklist
        self.collector = {}
        self.done = []

    def get_API_contents(self, steam_id):
        url = API_URL_HEAD + API_KEY + API_URL_TAIL + steam_id
        i = 0
        while i < STEAM_RETRY_LIMIT:
            try:
                page_source = requests.get(url).content.decode()
                if STEAM_API_ERROR_1 in page_source or STEAM_API_ERROR_2 in page_source:
                    print(STEAM_PRIVATE_PROFILE)
                    if STEAM_PERMISSION_DENIED != page_source:
                        print(page_source)
                    self.blacklist.add(steam_id)
                    return -1
                if STEAM_INTERNAL_ERROR in page_source:
                    print(STEAM_INTERNAL_ERROR + ": " + steam_id)
                    return -1
                if STEAM_API_ERROR_3 in page_source:
                    raise Exception(API_UNSUCCESSFUL)
            except Exception as error:
                print(error)
            else:
                print(url + LOAD_SUCCESS)
                return page_source
            i += 1
        return -1

    def get_Public_contents(self, steam_id):
        url = PUBLIC_URL_HEAD + steam_id + PUBLIC_URL_TAIL
        i = 0
        while i < STEAM_RETRY_LIMIT:
            try:
                page_source = requests.get(url).content.decode()
                if STEAM_PUBLIC_ERROR in page_source or "{\"success\":false}" in page_source or "\"rgInventory\":[]," in page_source:
                    if len(page_source) > 100:
                        raise Exception(page_source)
                    raise Exception
                if "{\"success\":false,\"Error\":\"This profile is private.\"}" in page_source:
                    print(steam_id + " is private.")
                    self.blacklist.add(steam_id)
                    return -1
            except Exception as error:
                if str(error) != "":
                    print(error)
            else:
                print(url + LOAD_SUCCESS)
                return page_source
            i += 1
        return -1

    def still_running(self):
        result = False
        for thread in self.dumpers:
            result = result or thread.is_alive()
        return result

    def get_inventory_backup(self, steam_id):
        age = -1
        try:
            age = int((time.time() - os.stat(INVENTORY_FOLDER + steam_id + INVENTORY_EXTENSION).st_mtime)/3600)
        except Exception as error:
            if "The system cannot find the file specified" not in str(error):
                print(error)
            return -1
        else:
            if age < 4:
                return Log(INVENTORY_FOLDER + steam_id + INVENTORY_EXTENSION, separator=SEPARATOR)
            return -1

    def get_inventory(self, steam_id):
        if steam_id in self.blacklist.log or steam_id in self.done:
            return
        self.done.append(steam_id)
        inventory = self.get_inventory_backup(steam_id)
        if inventory == -1:
            Public_contents = self.get_Public_contents(steam_id)
            if Public_contents == -1:
                print(INVENTORY_ERROR)
                return -1
            API_contents = self.get_API_contents(steam_id)
            x = API_contents
            if API_contents == -1:
                print(INVENTORY_ERROR)
                return -1
            all_weapons = {}
            Public_contents = json.loads(Public_contents)
            API_contents = json.loads(API_contents)
            for item_id in Public_contents["rgInventory"].keys():  # item_id = string
                try:
                    identifier = Public_contents["rgInventory"][item_id]["classid"] + "_" + Public_contents["rgInventory"][item_id]["instanceid"]
                    condition_wear = CONDITION_DETAILS[Public_contents["rgDescriptions"][identifier]["descriptions"][0]['value']][1]
                    name = LoungeMiner.trim_name(Public_contents["rgDescriptions"][identifier]["market_name"])  # Public_contents[...] is a string
                    all_weapons[item_id] = []
                    all_weapons[item_id].append(name)  # string
                    all_weapons[item_id].append(condition_wear)  # list of two floats
                except Exception as error:
                    if "KeyError" not in str(type(error)):
                        print(error)
            for item in API_contents["result"]["items"]:
                try:
                    item_id = str(item["id"])
                    if item_id in all_weapons.keys():
                        weapon_model = None
                        wear = None
                        attributes = item["attributes"]
                        for attribute in attributes:
                            if attribute["defindex"] == 8:
                                wear = attribute["float_value"]  # originally a float
                            if attribute["defindex"] == 6:
                                weapon_model = attribute["float_value"]  # originally a flost
                        condition_wear = all_weapons[item_id].pop()
                        all_weapons[item_id].append(wear)  # float
                        all_weapons[item_id].append([max(MINMAX_WEAR[str(weapon_model)][0], condition_wear[0]), min(MINMAX_WEAR[str(weapon_model)][1], condition_wear[1])])  # list of two floats
                        all_weapons[item_id].append(weapon_model)  # int
                except Exception as error:
                    print(error)
            try:
                os.remove(INVENTORY_FOLDER + steam_id + INVENTORY_EXTENSION)
            except:
                ()
            inventory = Log(INVENTORY_FOLDER + steam_id + INVENTORY_EXTENSION, separator="|")
            for item in all_weapons.keys():
                try:
                    inventory.add([str(all_weapons[item][2][0]), str(all_weapons[item][1]), str(all_weapons[item][2][1]), str(all_weapons[item][0]), steam_id, str(item), str(all_weapons[item][3])])
                except:
                    print(steam_id, "ERROR")
            inventory.log.sort(key=lambda x: float(x[1]))
            inventory.save()
        for item in inventory.log:
            if item[3] in self.collector.keys():
                self.collector[item[3]].append(item)
            else:
                self.collector[item[3]] = [item]
        return inventory

    def run(self):
        while self.still_running():
            while not self.tasks.empty():
                self.get_inventory(self.tasks.get())
        while not self.tasks.empty():
                self.get_inventory(self.tasks.get())
        for item_name in self.collector.keys():
            limits = get_limit_wears(self.collector[item_name][0][WEAPON_ID_ID])
            if extract_wear_to_int(item_name) == limits[0] or (("rimson" in item_name or "erpent" in item_name or "owl" in item_name) and extract_wear_to_int(item_name) != limits[1]):
                garbage = Log(VAULT_FOLDER + item_name + VAULT_EXTENSION, separator=SEPARATOR)
                garbage.log += self.collector[item_name]
                items = []
                for item in garbage.log:
                    if item[5] not in [x[5] for x in items]:
                        items.append(item)
                items.sort(key=lambda x: float(x[1]))
                if "oppler" in item_name or "owl" in item_name:
                    garbage.replace_log(items)
                else:
                    garbage.replace_log(items[:min(20, len(items))])
                garbage.save()
            if extract_wear_to_int(item_name) == limits[1]:
                garbage = Log(VAULT_FOLDER + item_name + VAULT_EXTENSION, separator=SEPARATOR)
                garbage.log += self.collector[item_name]
                items = []
                for item in garbage.log:
                    if item[5] not in [x[5] for x in items]:
                        items.append(item)
                items.sort(key=lambda x: -float(x[1]))
                if "oppler" in item_name or "owl" in item_name:
                    garbage.replace_log(items)
                else:
                    garbage.replace_log(items[:min(20, len(items))])
                garbage.save()