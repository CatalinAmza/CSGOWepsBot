import requests
import webbrowser
import time
import urllib.parse

link = "http://steamcommunity.com/market/search/render/?query=&start=0&count=100&search_descriptions=0&sort_column=price&sort_dir=asc&appid=730&category_730_ItemSet[]=any&category_730_TournamentTeam[]=any&category_730_Weapon[]=any&category_730_Exterior[]=tag_WearCategory2&category_730_Exterior[]=tag_WearCategory1&category_730_Exterior[]=tag_WearCategory0&category_730_Rarity[]=tag_Rarity_Ancient_Weapon&category_730_Type[]=tag_CSGO_Type_Pistol&category_730_Type[]=tag_CSGO_Type_Rifle&category_730_Type[]=tag_CSGO_Type_SniperRifle&category_730_Type[]=tag_CSGO_Type_Knife"

prefix = "http://steamcommunity.com/market/listings/730/"

weapons_cheap = ["StatTrak™ Galil AR | Chatterbox (Field-Tested)", "M4A1-S | Hyper Beast (Minimal Wear)", "M4A1-S | Hyper Beast (Factory New)", "StatTrak™ M4A1-S | Hyper Beast (Field-Tested)",
                 "StatTrak™ M4A1-S | Hyper Beast (Minimal Wear)", "StatTrak™ M4A1-S | Cyrex (Field-Tested)", "StatTrak™ M4A1-S | Cyrex (Factory New)", "StatTrak™ M4A1-S | Cyrex (Minimal Wear)",
                 "M4A4 | Howl (Factory New)", "StatTrak™ M4A4 | Howl (Factory New)", "M4A4 | Howl (Minimal Wear)", "StatTrak™ M4A4 | Howl (Minimal Wear)", "M4A4 | Howl (Field-Tested)",
                 "StatTrak™ M4A4 | Howl (Field-Tested)", "StatTrak™ M4A4 | Asiimov (Field-Tested)", "StatTrak™ M4A4 | Asiimov (Well-Worn)", "StatTrak™ CZ75-Auto | Victoria (Factory New)",
                 "StatTrak™ Desert Eagle | Golden Koi (Factory New)", "StatTrak™ Desert Eagle | Golden Koi (Minimal Wear)", "StatTrak™ P2000 | Fire Elemental (Factory New)",
                 "AK-47 | Aquamarine Revenge (Factory New)", "AK-47 | Aquamarine Revenge (Minimal Wear)", "StatTrak™ AK-47 | Aquamarine Revenge (Field-Tested)", "StatTrak™ AK-47 | Aquamarine Revenge (Minimal Wear)",
                 "StatTrak™ AK-47 | Aquamarine Revenge (Factory New)", "AK-47 | Wasteland Rebel (Factory New)", "StatTrak™ AK-47 | Wasteland Rebel (Minimal Wear)", "StatTrak™ AK-47 | Wasteland Rebel (Field-Tested)",
                 "StatTrak™ AK-47 | Wasteland Rebel (Factory New)", "StatTrak™ AK-47 | Jaguar (Minimal Wear)", "StatTrak™ AK-47 | Jaguar (Factory New)", "AK-47 | Vulcan (Factory New)",
                 "StatTrak™ AK-47 | Vulcan (Minimal Wear)", "StatTrak™ AK-47 | Vulcan (Field-Tested)", "StatTrak™ AK-47 | Vulcan (Factory New)", "AK-47 | Fire Serpent (Minimal Wear)",
                 "AK-47 | Fire Serpent (Field-Tested)", "StatTrak™ AK-47 | Fire Serpent (Factory New)", "StatTrak™ AK-47 | Fire Serpent (Minimal Wear)", "StatTrak™ AK-47 | Fire Serpent (Field-Tested)",
                 "AWP | Hyper Beast (Minimal Wear)", "AWP | Hyper Beast (Factory New)", "StatTrak™ AWP | Hyper Beast (Field-Tested)", "StatTrak™ AWP | Hyper Beast (Minimal Wear)",
                 "StatTrak™ AWP | Hyper Beast (Factory New)", "AWP | Dragon Lore (Factory New)", "AWP | Dragon Lore (Minimal Wear)", "AWP | Dragon Lore (Field-Tested)", "StatTrak™ AWP | Asiimov (Field-Tested)",
                 "StatTrak™ AWP | Lightning Strike (Factory New)", "StatTrak™ AWP | Lightning Strike (Minimal Wear)", "AWP | Medusa (Factory New)", "AWP | Medusa (Minimal Wear)", "AWP | Medusa (Field-Tested)"]

cancers = ["safari", "urban", "scorched", "ddpat", "boreal"]
genius = ["tiger", "fade", "slaughter", "doppler"]

# define cookies and headers

std_header = {"User-Agent": "refresher"}

buy_prefix = "https://steamcommunity.com/market/buylisting/"

choices = [(cookie_1, header_1), (cookie_2, header_2), (cookie_3, header_3)]

listing_cue = "listingid"
instance_cue = "instanceid"
total_cue = "<span class=\"market_listing_price market_listing_price_with_fee\">"
net_cue = "<span class=\"market_listing_price market_listing_price_without_fee\">"


def good_knife(name):
    if "karambit" in name.lower():
        return True
    elif "bayonet" in name.lower() or "butterfly" in name.lower():
        res = True
        for x in cancers:
            if x in name.lower():
                res = False
        return res
    elif "falchion" in name.lower():
        res = True
        for x in cancers + ["night"]:
            if x in name.lower():
                res = False
        return res
    elif "flip" in name.lower():
        for x in genius:
            if x in name.lower():
                return True
        return False
    elif "huntsman" in name.lower():
        res = True
        for x in cancers + ["stained"]:
            if x in name.lower():
                res = False
        return res
    return False

stop = False

name_cue = "class=\\\"market_listing_item_name\\\" style=\\\"color:"


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

j = 1
start_time = time.time()

while not stop:
    now = time.time()
    diff = int(now - start_time)
    hours = int(diff / 3600)
    mins = int((diff - 3600 * hours) / 60)
    secs = diff - 3600 * hours - 60 * mins
    print("Round %s (time elapsed: %d hours, %d mins, %d secs)." % (j, hours, mins, secs))
    j += 1
    source = requests.get(link).content.decode()
    pos = 0
    for i in range(source.count(name_cue)):
        pos = source.find(name_cue, pos)
        pos = source.find(">", pos)
        end = source.find("<", pos)
        name = source[pos + 1:end].replace("\\u2605", "★").replace("\\u2122", "™")
        if name in weapons_cheap or good_knife(name):
            print("Found a %s." % name)
            buy(prefix + name, 0)
            webbrowser.open(prefix + name, new=0, autoraise=True)
