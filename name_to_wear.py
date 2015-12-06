import json
import webbrowser
from Qprint import *
from best_wears import *

CONDITION_DETAILS = {"Exterior: Factory New": ["FN", [0.00, 0.07]], "Exterior: Minimal Wear": ["MW", [0.07, 0.15]],
                     "Exterior: Field-Tested": ["FT", [0.15, 0.37]], "Exterior: Well-Worn": ["WW", [0.37, 0.44]], "Exterior: Battle-Scarred": ["BS", [0.44, 1.00]]}
names = ['', "Factory New", 'Minimal Wear', 'Field-Tested', 'Well-Worn', 'Battle-Scarred']
reverse = {}
for x in range(1,6):
    reverse[names[x]] = x

file = open('wear_values.wv', 'r')
x = json.loads(file.read())
file.close()

file =  # location of resource/csgo_english.txt duplicate (you need to copy-paste the contents of the file, to a new one, to avoid encoding issues)
y = file.read()

res = {}  # vulcan - 0.0, 0.9 (instance of key: value)

for z in x:
    try:
        pos = y.index(x[z][2]) + len(x[z][2]) + 1
        res[y[pos: pos + y[pos:].find('\"\n')].strip()[1:]] = x[z][:-1]
        qprint(y[pos: pos + y[pos:].find('\"\n')].strip()[1:], end = ' ')
        qprint(x[z][-1][9:-4])
    except:
        pass


def get_wear_names(limits):
    min_wear = -1
    max_wear = -1
    for i in range(1, ITW_RANGE):
        if CONDITION_DETAILS[WEAR_PREFIX + INT_TO_WEAR[i]][1][0] <= limits[0] < CONDITION_DETAILS[WEAR_PREFIX + INT_TO_WEAR[i]][1][1]:
            min_wear = i
        if CONDITION_DETAILS[WEAR_PREFIX + INT_TO_WEAR[i]][1][0] < limits[1] <= CONDITION_DETAILS[WEAR_PREFIX + INT_TO_WEAR[i]][1][1]:
            max_wear = i
    return min_wear


rez = {}
for skin in res:
    rez[skin] = get_wear_names(res[skin])

qprint(rez)

