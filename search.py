import os
from constants import *
from Log import Log
import webbrowser

print("What are you looking for?")
user_input = ""
while user_input == "":
    user_input = input()
words = []
st = False
open = False
limit = 100000
phase = 0
for x in user_input.split():
    if x.lower() == "st":
        st = True
    elif x.lower() == "open":
        open = True
    elif x.lower() in ["p1", "p2", "p3", "p4"]:
        phase = int(x.lower()[1])
    else:
        try:
            limit = int(x)
        except:
            words.append(x)
names = []
for file in os.listdir(os.getcwd() + "\\" + VAULT_FOLDER):
    keep = True
    for x in words:
        if x not in file.lower():
            keep = False
    if keep:
        names.append(file)

res = []
if st:
    for x in names:
        if "stattrak" in x.lower():
            res.append(x)
else:
    for x in names:
        if "stattrak" not in x.lower():
            res.append(x)

print("Searching for: %s" % str(res))
if len(res) != 1:
    print("You probably didn't provide enough terms for a good result.")

i = 0
for weapon in res:
    weps = Log(os.getcwd() + "\\" + VAULT_FOLDER + weapon, SEPARATOR)
    if phase == 0:
        print(weps)
    else:
        weps.create_printable()
        for j in range(len(weps.log)):
            if int(weps.log[j][6]) == phase + 417:
                print(weps.text[j])
    if open:
        for wep in weps.log:
            if i < limit:
                if phase == 0 or int(wep[6]) == phase + 417:
                    #webbrowser.open("http://csgolounge.com/profile?id=" + wep[4], new=0, autoraise=True)
                    webbrowser.open("http://www.steamcommunity.com/profiles/" + wep[4] + "/inventory", new=0, autoraise=True)
                    i += 1
