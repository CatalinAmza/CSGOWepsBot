file = open("wear_values.wv", "w")
file.write("{\n")
items_game = open("C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\csgo\scripts\items\items_game.txt","r")
items_game_contents = items_game.read()
paint_kits_position = items_game_contents.find("paint_kits")
count = 505
for weapon_model in range(count):
    start_position = items_game_contents[paint_kits_position:].find("\"" + str(weapon_model) + "\"\n\t\t{")
    jump_position = items_game_contents[paint_kits_position+start_position:].find("name")
    next_name_position = items_game_contents[paint_kits_position + start_position + jump_position + len("name"):].find("name")
    item_paint_kit = items_game_contents[paint_kits_position + start_position: paint_kits_position + start_position + jump_position + next_name_position]
    x = item_paint_kit.replace('{', '').replace('}', '').split()
    try:
        tag = x[6]
    except:
        pass
    wear_remap_min_position = item_paint_kit.find("wear_remap_min")
    wear_remap_max_position = item_paint_kit.find("wear_remap_max")
    wear_remap_min = "0.060000"
    wear_remap_max = "0.800000"
    if wear_remap_min_position != -1:
        temp = item_paint_kit[wear_remap_min_position + len("wear_remap_min\""):]
        start_index = temp.find("\"")
        end_index = temp[start_index + 1:].find("\"")
        wear_remap_min = temp[start_index + 1:start_index + 1 + end_index]
    if wear_remap_max_position != -1:
        temp = item_paint_kit[wear_remap_max_position + len("wear_remap_max\""):]
        start_index = temp.find("\"")
        end_index = temp[start_index + 1:].find("\"")
        wear_remap_max = temp[start_index + 1:start_index + 1 + end_index]
    if 'paint' in tag.lower() and 'default' not in tag.lower():
        file.write("\"" + str(weapon_model) + "\" : [" + wear_remap_min + ", " + wear_remap_max + ', ' + tag.replace('#', '') + "]")
        if weapon_model != count - 1:
            file.write(",\n")
        else:
            file.write("\n")
file.write("}")
