import os
from constants import *
from Log import Log

NEED_STRING = "Your parameter should be a string (best_wears/get_limit_wears)"
CONDITION_DETAILS = {"Exterior: Factory New": ["FN", [0.00, 0.07]], "Exterior: Minimal Wear": ["MW", [0.07, 0.15]],
                     "Exterior: Field-Tested": ["FT", [0.15, 0.37]], "Exterior: Well-Worn": ["WW", [0.37, 0.44]], "Exterior: Battle-Scarred": ["BS", [0.44, 1.00]]}
WEAR_PREFIX = "Exterior: "
INT_TO_WEAR = {1: "Factory New", 2: "Minimal Wear", 3: "Field-Tested", 4: "Well-Worn", 5: "Battle-Scarred"}
ITW_RANGE = 6
GLW_ERROR = "Error in get_limit_wears"


def get_limit_wears(weapon_id):
    if weapon_id.__class__.__name__ != "str":
        print(NEED_STRING)
        weapon_id = str(weapon_id)
    limits = MINMAX_WEAR[weapon_id]
    min_wear = -1
    max_wear = -1
    for i in range(1, ITW_RANGE):
        if CONDITION_DETAILS[WEAR_PREFIX + INT_TO_WEAR[i]][1][0] <= limits[0] < CONDITION_DETAILS[WEAR_PREFIX + INT_TO_WEAR[i]][1][1]:
            min_wear = i
        if CONDITION_DETAILS[WEAR_PREFIX + INT_TO_WEAR[i]][1][0] < limits[1] <= CONDITION_DETAILS[WEAR_PREFIX + INT_TO_WEAR[i]][1][1]:
            max_wear = i
    if min_wear == -1 or max_wear == -1:
        raise Exception(GLW_ERROR)
    return [min_wear, max_wear]


def get_all_limit_wears():
    res = {}
    for weapon_id in MINMAX_WEAR.keys():
        res[weapon_id] = get_limit_wears(weapon_id)
    return res


def extract_wear_to_int(string):
    for i in range(1, ITW_RANGE):
        if INT_TO_WEAR[i] in string:
            return i


def best_wears():
    interests = get_all_limit_wears()
    result = []
    for file in os.listdir(os.getcwd() + "\\" + VAULT_FOLDER):
        weapons = Log(os.getcwd() + "\\" + VAULT_FOLDER + file, SEPARATOR)
        wear = extract_wear_to_int(file)
        if wear == interests[weapons.log[0][WEAPON_ID_ID]][0]:
            result.append([float(weapons.log[0][1]) - MINMAX_WEAR[weapons.log[0][WEAPON_ID_ID]][0], file])
        if wear == interests[weapons.log[0][WEAPON_ID_ID]][1]:
            result.append([MINMAX_WEAR[weapons.log[0][6]][1] - float(weapons.log[0][1]), file])
    result.sort(key=lambda x: x[0])
    for i in result:
        print(i)
