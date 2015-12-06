import requests
import time
from name_to_wear import *

acceptable = {1: 0.055, 2: 0.075, 3: 0.12, 4: 0.17}

std_link = 'http://steamcommunity.com/market/search/render/?query=holo&start=0&count=100&search_descriptions=1&sort_column=price&sort_dir=desc&appid=730&category_730_ItemSet[]=any&category_730_ProPlayer[]=any&category_730_TournamentTeam[]=any&category_730_Weapon[]=any&category_730_Quality[]=tag_normal&category_730_Quality[]=tag_strange&category_730_Tournament[]=tag_Tournament3&category_730_Type[]=tag_CSGO_Type_Pistol&category_730_Type[]=tag_CSGO_Type_Rifle&category_730_Type[]=tag_CSGO_Type_SniperRifle'
wep_link = 'http://steamcommunity.com/market/listings/730/item/render/?query=&start=0&count=100&currency=3&filter=katowice 2014 holo'
sticker_link = 'http://steamcommunity.com/market/search/render/?query=katowice%202014%20sticker&start=0&count=100&search_descriptions=0&sort_column=default&sort_dir=desc'
market_template_link = 'https://steamcommunity.com/market/listings/730/'

# define cookies

sticker_price = {}
session = requests.Session()
session.cookies.update(cookie)


def is_stattrak(wep):
    if 'stattrak' in wep.lower():
        return 0.025
    else:
        return 0


def get_source(link):
    qprint('Loading %s.' % str(link))
    try:
        time.sleep(15)
        source = session.get(link).content.decode()
    except:
        return get_source(link)
    if len(source) > 10 and 'The server is temporarily unable to service your request' not in source and 'You\'ve made too many requests recently.' not in source:
        return source
    else:
        return get_source(link)


def get_capsule(source, start_pos, start_cue, end_cue):                              # returns (chunk, start, end) where
    if start_cue in end_cue or end_cue in start_cue:                                # $chunk is the first chunk of $source, after $start_pos, that's encapsulated between $start_cue and $end_cue
        qprint('Your cues contain each other. Illegal use', color=RED+BOLD)         # (including the capsule) and $start is the index of the beginning of the core and $end its end.
        raise Exception()
    else:
        first_start_occurrence = source[start_pos:].find(start_cue)
        first_end_occurrence = source[start_pos:].find(end_cue)
        if first_start_occurrence == -1 or first_end_occurrence == -1:
            #qprint('Your source doesn't contain any capsules corresponding to your description')
            return -1
        else:
            current = start_pos + first_start_occurrence + len(start_cue)
            count = 1
            while count > 0:
                current_start = source[current:].find(start_cue)
                current_end = source[current:].find(end_cue)
                if current_end == -1:
                    return -1
                if current_start == -1:
                    current_start = current_end + 1
                if current_start < current_end:
                    count += 1
                    current += current_start + len(start_cue)
                else:
                    count -= 1
                    current += current_end + len(end_cue)
            return [source[start_pos + first_start_occurrence: current], start_pos + first_start_occurrence + len(start_cue), current - len(end_cue)]


def get_core(source, start_pos, start_cue, end_cue):  # returns the first chunk of $source, after $start_pos, that's encapsulated between $start_cue and $end_cue (excluding the capsule)
    res = get_capsule(source, start_pos, start_cue, end_cue)
    if res == -1:
        return -1
    else:
        return source[res[1]: res[2]]


def get_all_cores(source, start_pos, start_cue, end_cue):
    res = []
    item = get_capsule(source, start_pos, start_cue, end_cue)
    while item != -1:
        res.append(source[item[1]:item[2]])
        item = get_capsule(source, item[2] + len(end_cue), start_cue, end_cue)
    return res


def get_sticker_prices():
    source = get_source(sticker_link)
    stickers = [x for x in get_all_cores(source, 0, ';\\\">', '<') if x != '']
    for sticker in stickers:
        sticker_price[sticker] = -1
        while sticker_price[sticker] < 0:
            source = get_source(market_template_link + sticker)
            coeff = 1
            if ('ninjas' in sticker.lower() or 'fnatic' in sticker.lower() or '3dmax' in sticker.lower()) and 'holo' in sticker.lower():
                coeff = 1/2
            if ('clan-mystic' in sticker.lower() or 'complexity' in sticker.lower()) and 'holo' in sticker.lower():
                coeff = 2/3
            if 'ibuypower' in sticker.lower() and 'holo' not in sticker.lower():
                coeff = 1/2
            if ('natus' in sticker.lower() or 'virtus' in sticker.lower()) and 'holo' in sticker.lower():
                coeff = 3/4
            sticker_price[sticker] = int(get_core(source, 0, 'converted_price\":', ',\"')) + int(get_core(source, 0, 'converted_fee\":', ',\"')) * coeff
            if 'ibuy' in sticker.lower() and 'holo' in sticker.lower():
                sticker_price[sticker] = 32000
            if 'titan' in sticker.lower() and 'holo' in sticker.lower():
                sticker_price[sticker] = 25000

get_sticker_prices()
mp = {}

bonus = [0.07, 0.03, 0, 0, 0, 0]

while 1:
    total_count = -1
    pages_swept = 0
    weps = []
    while pages_swept * 100 < total_count or pages_swept == 0:
        source = get_source(std_link.replace('start=0', 'start=%d' % (pages_swept * 100)))
        if pages_swept == 0:
            total_count = int(get_core(source, 0, '\"total_count\":', ','))
        weps.extend([x.replace('\\u2122', '™') for x in get_all_cores(source, 0, ';\\\">', '<') if ('dragon' not in x.lower() or 'king' not in x.lower()) and (x != '') and 'aug' not in x.lower() and 'scar-20' not in x.lower() and 'g3sg1' not in x.lower() and 'berettas' not in x.lower()])
        pages_swept += 1
    for wep in weps:
        if wep not in mp:
            source = get_source(market_template_link + wep)
            try:
                mp[wep] = [int(x) * 1.15 for x in get_all_cores(source, 0, '\"converted_price\":', ',\"') if 'sold' not in x.lower()][0]
                if mp[wep] > 50000:
                    print(source)
            except:
                qprint('Couldn\'t get market price for %s.\n %s' % (wep, source))
        coeff = 1
        if 'blue laminate' in wep.lower() or 'pit viper' in wep.lower() or 'predator' in wep.lower() or 'blood  tiger' in wep.lower() or 'boreal' in wep.lower():
            coeff = 2/3
        source = get_source(wep_link.replace('item', wep))
        stickers = []
        STicks = get_all_cores(source, 0, '<br>Sticker: ', '<\\/center>')
        PRices = [int(100 * float(x.replace('-', '0').replace(',', '.').replace('\\u20ac', ''))) for x in get_all_cores(source, 0, 'with_fee\\\">\\r\\n\\t\\t\\t\\t\\t\\t', '\\t\\t\\t\\t\\t<\\/span')]
        for i in range(len(STicks)):
            z = [stick.strip() for stick in STicks[i].split(',')]
            all_sticks = ['Sticker | ' + y for y in z]
            holos = [stick for stick in all_sticks if '(Holo) | Katowice 2014' in stick]
            katos = [stick for stick in all_sticks if '| Katowice 2014' in stick and '3dmax' not in stick.lower() and 'mystic' not in stick.lower() and 'mousesports' not in stick.lower() and 'fnatic' not in stick.lower() and 'ninjas' not in stick.lower() and 'virtus' not in stick.lower()]
            if len(katos) > 2 or len(holos) > 1:
                sum = 0
                for stick in all_sticks:
                    if stick in sticker_price:
                       sum += sticker_price[stick]
                if True or (PRices[i] - mp[wep]) / sum < coeff * acceptable[len(holos)] + bonus[reverse[get_core(wep, 0, '(', ')')] - rez[get_core(wep, 0, '|', '(').strip()]] + is_stattrak(wep):
                    sticks = ''
                    for stick in katos:
                        sticks += stick + ' '
                    if len(holos) > 0:
                        if len(katos) > 0:
                            sticks += 'holo'
                        else:
                            sticks += holos[0]
                    qprint((PRices[i] - mp[wep]) / sum, end=' for: ')
                    qprint(all_sticks)
                    webbrowser.open_new_tab(market_template_link + wep + '?filter=' + sticks)
    time.sleep(10)
