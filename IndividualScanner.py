import webbrowser
import requests
import time
import random
from threading import Thread
import urllib.parse
import ast
import os

# define cookies and headers 

std_header = {"User-Agent": "refresher"}

prefix = "http://steamcommunity.com/market/listings/730/"

buy_prefix = "https://steamcommunity.com/market/buylisting/"

names_limit = ["★ M9 Bayonet | Tiger Tooth (Factory New)", "★ Karambit | Doppler (Factory New)"]

names_all = ["StatTrak™ AK-47 | Fire Serpent (Factory New)", "StatTrak™ AK-47 | Fire Serpent (Minimal Wear)", "StatTrak™ AK-47 | Fire Serpent (Field-Tested)", "AK-47 | Fire Serpent (Factory New)",
             "StatTrak™ AWP | Hyper Beast (Factory New)", "AWP | Dragon Lore (Factory New)", "AWP | Dragon Lore (Minimal Wear)",
             "StatTrak™ M4A1-S | Hyper Beast (Factory New)", "StatTrak™ M4A4 | Howl (Factory New)", "★ StatTrak™ M9 Bayonet | Slaughter (Factory New)",
             "StatTrak™ M4A4 | Howl (Minimal Wear)", "StatTrak™ M4A4 | Howl (Field-Tested)", "★ StatTrak™ Bayonet | Marble Fade (Factory New)", "★ StatTrak™ Bayonet | Tiger Tooth (Factory New)",
             "★ Bayonet | Ultraviolet (Factory New)", "★ StatTrak™ Bayonet | Ultraviolet (Factory New)", "★ Bayonet | Crimson Web (Factory New)", "★ StatTrak™ Bayonet | Crimson Web (Factory New)",
             "★ StatTrak™ Bayonet | Slaughter (Factory New)", "★ StatTrak™ Butterfly Knife | Crimson Web (Factory New)", "★ Butterfly Knife | Crimson Web (Factory New)",
             "★ StatTrak™ Falchion Knife | Crimson Web (Factory New)", "★ Falchion Knife | Crimson Web (Factory New)", "★ StatTrak™ Flip Knife | Crimson Web (Factory New)", "★ Karambit | Fade (Factory New)",
             "★ StatTrak™ Karambit | Fade (Factory New)", "★ StatTrak™ Karambit | Night (Factory New)", "★ Karambit | Night (Factory New)", "★ StatTrak™ Karambit | Slaughter (Factory New)",
             "★ StatTrak™ Karambit | Doppler (Factory New)", "★ StatTrak™ Karambit | Marble Fade (Factory New)", "★ Karambit | Marble Fade (Factory New)", "★ StatTrak™ Karambit | Tiger Tooth (Factory New)",
             "★ Karambit | Tiger Tooth (Factory New)", "★ StatTrak™ Karambit | Ultraviolet (Factory New)", "★ Karambit | Ultraviolet (Factory New)", "★ StatTrak™ Karambit | Crimson Web (Factory New)",
             "★ Karambit | Crimson Web (Factory New)", "★ StatTrak™ M9 Bayonet | Doppler (Factory New)", "★ StatTrak™ M9 Bayonet | Marble Fade (Factory New)", "★ M9 Bayonet | Marble Fade (Factory New)",
             "★ StatTrak™ M9 Bayonet | Tiger Tooth (Factory New)", "★ StatTrak™ M9 Bayonet | Ultraviolet (Factory New)",
             "★ M9 Bayonet | Ultraviolet (Factory New)", "★ StatTrak™ M9 Bayonet | Crimson Web (Factory New)", "★ M9 Bayonet | Crimson Web (Factory New)", "★ StatTrak™ M9 Bayonet | Fade (Factory New)"]

choices = [(cookie_1, header_1), (cookie_2, header_2), (cookie_3, header_3)]
names = names_all + names_limit

listing_cue = "listingid"
instance_cue = "instanceid"
total_cue = "<span class=\"market_listing_price market_listing_price_with_fee\">"
net_cue = "<span class=\"market_listing_price market_listing_price_without_fee\">"

check_1 = "An error was encountered while processing your request"
check_2 = "You don't have permission to access"

data_ez = {"currency": "3"}


def update_log(name):
    name = name.replace("★ ", "")
    file = open("guns.log", "r")
    try:
        history = ast.literal_eval(file.read())
    except:
        history = {}
    if name in history:
        history[name] += 1
    else:
        history[name] = 1
    file.close()
    os.unlink("guns.log")
    file = open("guns.log", "w")
    file.write("{\n")
    for x in history:
        if x != name:
            file.write("\'%s\': %d,\n" % (x, history[x]))
    file.write("\'%s\': %d\n" % (name, history[name]))
    file.write("}")


class TimeOut(Thread):
    def __init__(self, name, link):
        Thread.__init__(self)
        self.name = name
        self.link = link

    def run(self):
        global names
        webbrowser.open(self.link, new=0, autoraise=True)
        update_log(self.name)
        names.remove(self.name)
        time.sleep(100)
        names.append(self.name)


def buy(link, choice_index):
    global choices
    if choice_index >= len(choices):
        return
    cookie = choices[choice_index][0]
    header = choices[choice_index][1]
    header["Referer"] = urllib.parse.quote(link).replace("%3A", ":")
    session = requests.Session()
    session.cookies.update(cookie)
    source = session.get(link, headers=header).content.decode()
    listing_id_start_index = source.find(listing_cue) + 3 + len(listing_cue)
    listing_id_end_index = source.find("\"", listing_id_start_index + 1)
    buy_link = buy_prefix + source[listing_id_start_index: listing_id_end_index]
    first = source.find(total_cue)
    second = source.find("&#", first)
    total = source[first + len(total_cue):second].strip().replace(",", "").replace("-", "0")
    if "sold" not in total.lower():
        third = source.find(net_cue, first)
        fourth = source.find("&#", third)
        net = source[third + len(net_cue):fourth].strip().replace(",", "").replace("-", "0")
        print(total, net)
        data = {"sessionid": '',  # session id from browser log on
                "currency": "3",
                "subtotal": net,
                "fee": str(int(total)-int(net)),
                "total": total,
                "quantity": "1"}
        #print(session.post(buy_link, data=data, headers=header).content.decode())
        global stop
        stop = True
    else:
        print("Sold before we saw it!")
stop = False
i = 1
start_time = time.time()
while True:
    session = requests.Session()
    name = names[random.randrange(len(names))]
    now = time.time()
    diff = int(now - start_time)
    hours = int(diff / 3600)
    mins = int((diff - 3600 * hours) / 60)
    secs = diff - 3600 * hours - 60 * mins
    print("Round %s (time elapsed: %d hours, %d mins, %d secs): Scanning for %s" % (i, hours, mins, secs, name.replace("★", "")))
    i += 1
    link = prefix + name
    source = session.get(link, data=data_ez, headers=std_header).content.decode()
    if source.find(instance_cue) != -1:
        if name in names_limit:
            x = TimeOut(name, link)
            x.start()
        else:
            print("HERE WE GO !!")
            x = TimeOut(name, link)
            x.start()
            buy(link, 0)
    if source.find(check_1) != -1 or source.find(check_2) != -1:
        print("ERROR for %s" % name.replace("★", ""))
