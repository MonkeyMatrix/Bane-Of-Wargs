# source imports
import terminal_handling
import logger_sys
import dialog_handling
import text_handling
from colors import *
from terminal_handling import cout, cinput
# external imports
import random


# Functions to handle missions
def get_mission_id_from_name(mission_name, mission_data):
    logger_sys.log_message(f"INFO: Getting mission name '{mission_name}' corresponding id")
    global mission_id
    count = 0
    continue_action = True

    while count < len(list(mission_data)) and continue_action:
        current_mission_data = mission_data[str(list(mission_data)[count])]
        if current_mission_data["name"] == mission_name:
            continue_action = False
            mission_id = str(list(mission_data)[count])

        count += 1
    logger_sys.log_message(f"INFO: Found corresponding id of mission name '{mission_name}': {mission_id}")
    return mission_id


def print_description(mission_data, map):
    logger_sys.log_message(f"INFO: Printing mission '{mission_data}' description to GUI")

    logger_sys.log_message(f"INFO: Generating mission text replacements")
    # Get text replacements
    # Payment of the mission when completed
    payment_for_mission = None
    if "on complete" in list(mission_data):
        if "payment" in list(mission_data["on complete"]):
            payment_for_mission = mission_data["on complete"]["payment"]
    # Destination of the mission
    destination_point = map["point" + str(mission_data["destination"])]
    destination_for_mission = "[X:" + str(destination_point["x"]) + ", Y:" + str(destination_point["y"]) + "]"
    # Deadline of the mission to be completed
    deadline_for_mission = None
    if "deadline" in list(mission_data):
        deadline_for_mission = mission_data["deadline"]
    # Stopovers of the mission
    stopovers_for_mission = None
    if "stopovers" in list(mission_data):
        stopovers_for_mission = mission_data["stopovers"]
        new_stopovers_for_mission = []
        count = 0
        while count < len(stopovers_for_mission):
            current_map_point_data = map["point" + str(stopovers_for_mission[count])]
            current_map_point_coordinates = (
                "[X:" + str(current_map_point_data["x"]) + ", Y:" +
                str(current_map_point_data["y"]) + "]"
            )
            new_stopovers_for_mission.append(current_map_point_coordinates)

            count += 1
        new_stopovers_for_mission = str(new_stopovers_for_mission)
    else:
        new_stopovers_for_mission = None

    # Load text replacements
    mission_text_replacements = {
        "$name_mission": mission_data["name"],
        "$description": mission_data["description"],
        "$payment": payment_for_mission,
        "$destination": destination_for_mission,
        "$deadline": deadline_for_mission,
        "$stopovers": new_stopovers_for_mission
    }
    logger_sys.log_message(f"INFO: Loading missions text replacements: '{mission_text_replacements}'")

    text = str(mission_data["description"])
    # Replace text replacement in the description by
    # its corresponding value in the mission_text_replacements
    # dictionary defined sooner
    count = 0
    while count < len(list(mission_text_replacements)):
        current_text_replacement = list(mission_text_replacements)[count]
        text = text.replace(current_text_replacement, str(mission_text_replacements[current_text_replacement]))

        count += 1

    # Print the text
    new_input = ""
    for i, letter in enumerate(text):
        if i % 54 == 0:
            new_input += '\n'
        new_input += letter

    # This is just because at the beginning too a `\n` character gets added
    new_input = new_input[1:]
    cout(str(new_input))


def mission_checks(mission_data, player, which_key):
    global checks_passed
    # Get every checks required
    # for running which_key operations

    checks = []
    generic_keys = ['to offer', 'to complete', 'to fail', 'to despawn', 'to spawn']

    # If which_key input is invalid, quit
    # the game and output the error to the
    # game logs files
    if (
        which_key != 'to offer'
        and which_key != 'to complete'
        and which_key != 'to fail'
        and which_key != 'to spawn'
        and which_key != 'to despawn'
    ):
        logger_sys.log_message(f"ERROR: Stopping mission checks for mission data '{mission_data}' --> invalid key '{which_key}'")
        text_handling.exit_game()

    if which_key in generic_keys:
        if "player attributes" in list(mission_data[which_key]):
            checks.append('Player Attributes')
        if "visited locations" in list(mission_data[which_key]):
            checks.append('Visited Locations')
        if "known enemies" in list(mission_data[which_key]):
            checks.append('Known Enemies')
        if "known zones" in list(mission_data[which_key]):
            checks.append('Known Zones')
        if "known npcs" in list(mission_data[which_key]):
            checks.append('Known Npcs')
        if "has items" in list(mission_data[which_key]):
            checks.append('Has Items')
        if "random" in list(mission_data[which_key]):
            checks.append('Random')

        # Check if checks are passing
        # and the action can continue
        checks_passed = True
        count = 0

        # Player attributes checks
        if 'Player Attributes' in checks:
            while count < len(mission_data[which_key]["player attributes"]) and checks_passed:
                current_attribute = mission_data[which_key]["player attributes"][count]
                if str(current_attribute) not in player["attributes"]:
                    checks_passed = False

                count += 1
            count = 0

        # Visited locations checks
        if 'Visited Locations' in checks:
            while count < len(mission_data[which_key]["visited locations"]) and checks_passed:
                current_location = mission_data[which_key]["visited locations"][count]
                if current_location not in player["visited points"]:
                    checks_passed = False

                count += 1
            count = 0

        # Known enemies checks
        if 'Known Enemies' in checks:
            while count < len(mission_data[which_key]["known enemies"]) and checks_passed:
                current_enemy = mission_data[which_key]["known enemies"][count]
                if current_enemy not in player["enemies list"]:
                    checks_passed = False

                count += 1
            count = 0

        # Known zones checks
        if 'Known Zones' in checks:
            while count < len(mission_data[which_key]["known zones"]) and checks_passed:
                current_enemy = mission_data[which_key]["known zones"][count]
                if current_enemy not in player["visited zones"]:
                    checks_passed = False

                count += 1
            count = 0

        # Known npcs checks
        if 'Known Npcs' in checks:
            while count < len(mission_data[which_key]["known npcs"]) and checks_passed:
                current_enemy = mission_data[which_key]["known npcs"][count]
                if current_enemy not in player["met npcs names"]:
                    checks_passed = False

                count += 1
            count = 0

        # Has items checks
        if 'Has Items' in checks:
            while count < len(mission_data[which_key]["has items"]) and checks_passed:
                current_item = mission_data[which_key]["has items"][count]

                if which_key == 'to fail':
                    if current_item in player["inventory"]:
                        checks_passed = False
                else:
                    if current_item not in player["inventory"]:
                        checks_passed = False

                count += 1
            count = 0

        # Random chance check
        if 'Random' in checks:
            if mission_data[which_key]["random"] > random.uniform(0, 1):
                checks_passed = True
            else:
                checks_passed = False

    return checks_passed


def execute_triggers(
    mission_data, player, which_key, dialog, preferences,
    text_replacements_generic, drinks, item, enemy, npcs,
    start_player, lists, zone, mission, mounts, start_time,
    map
):
    # If which_key input is invalid, quit
    # the game and output the error to the
    # game logs files
    if (
        which_key != 'on offer'
        and which_key != 'on complete'
        and which_key != 'on fail'
    ):
        logger_sys.log_message(f"ERROR: Stopping mission checks for mission data '{mission_data}' --> invalid key '{which_key}'")
        text_handling.exit_game()

    if which_key in mission_data:
        if "dialog" in mission_data[which_key]:
            dialog_handling.print_dialog(
                mission_data[which_key]["dialog"], dialog, preferences, text_replacements_generic, player, drinks,
                item, enemy, npcs, start_player, lists, zone,
                mission, mounts, start_time, map
            )
            text_handling.print_separator('=')
        if "payment" in mission_data[which_key]:
            player["gold"] += mission_data[which_key]["payment"]
        if "fine" in mission_data[which_key]:
            player["gold"] -= mission_data[which_key]["fine"]
        if "exp addition" in mission_data[which_key]:
            player["xp"] += mission_data[which_key]["exp addition"]


def offer_mission(
    mission_id, player, missions_data, dialog, preferences,
    text_replacements_generic, drinks, item, enemy, npcs,
    start_player, lists, zone, mission, mounts, start_time,
    map
):
    logger_sys.log_message(f"INFO: Offering mission '{mission_id}' to player")
    data = missions_data[mission_id]

    # Add the mission ID to the player's
    # offered missions list and add
    # the mission data in the player's
    # data of its save

    if 'to offer' in data:
        can_offer = mission_checks(data, player, 'to offer')
    else:
        can_offer = True

    if can_offer:
        player["offered missions"].append(mission_id)

        mission_dict = {
            "went to all stopovers": False,
            "stopovers went": []
        }

        player["missions"][mission_id] = mission_dict

        # Trigger the mission 'on offer'
        # triggers if there are

        logger_sys.log_message(f"INFO: Triggering mission '{mission_id}' 'on offer' triggers")
        if "on offer" in list(data):
            # Only ask for accepting mission if there is a dialog,
            # else, make the player automatically accept it
            if "dialog" in list(data["on offer"]):
                dialog_handling.print_dialog(
                    data["on offer"]["dialog"], dialog, preferences, text_replacements_generic, player, drinks,
                    item, enemy, npcs, start_player, lists, zone,
                    mission, mounts, start_time, map
                )
                if "force accept" in list(data):
                    if not data["force accept"]:
                        accept = cinput("Do you want to accept this task? (y/n) ")
                    else:
                        accept = "y"
                else:
                    accept = cinput("Do you want to accept this task? (y/n) ")
                text_handling.print_separator('=')
                if accept.startswith('y'):
                    if player["active missions"] is None:
                        player["active missions"] = []
                    player["active missions"].append(mission_id)
                    cout(
                        COLOR_CYAN + COLOR_STYLE_BRIGHT + "You obtained mission '" + data["name"] + "'" + COLOR_RESET_ALL
                    )
            else:
                if player["active missions"] is None:
                    player["active missions"] = []
                player["active missions"] += [mission_id]
            if "payment" in list(data["on offer"]):
                player["gold"] += int(data["on offer"]["payment"])
            if "fine" in list(data["on offer"]):
                player["gold"] -= int(data["on offer"]["fine"])
            if "exp addition" in list(data["on offer"]):
                player["xp"] += int(data["on offer"]["exp addition"])
        else:
            if player["active missions"] is None:
                player["active missions"] = []
            player["active missions"].append(mission_id)
            cout(COLOR_CYAN + COLOR_STYLE_BRIGHT + "You obtained mission '" + data["name"] + "'" + COLOR_RESET_ALL)
        logger_sys.log_message(f"INFO: Finished triggering mission '{mission_id}' 'on offer' triggers")


def mission_completing_checks(
    mission_id, missions_data, player, dialog, preferences,
    text_replacements_generic, drinks, item, enemy, npcs, start_player,
    lists, zone, mission, mounts, start_time
):
    # Load mission data and check if the
    # required attributes to complete the
    # mission are here and also check if the
    # player has been on every stopovers and
    # is on the destination point too
    mission_data = missions_data[mission_id]
    logger_sys.log_message(f"INFO: Checking if the player can complete mission '{mission_id}'")

    if "to complete" in list(mission_data):
        attributes_checks_passed = mission_checks(mission_data, player, 'to complete')
    else:
        attributes_checks_passed = True

    if "stopovers" in list(mission_data):
        stopovers_checks_passed = player["missions"][mission_id]["went to all stopovers"]
    else:
        stopovers_checks_passed = True

    # If the player has done everything
    # required to complete the mission, then
    # execute the 'on complete' triggers and
    # remove the mission id from the player
    # 'active missions' list and add it to the
    # 'done missions' list
    if attributes_checks_passed and stopovers_checks_passed:
        logger_sys.log_message(f"INFO: Executing mission '{mission_id}' completing triggers")

        execute_triggers(
            mission_data, player, 'on complete', dialog, preferences,
            text_replacements_generic, drinks, item, enemy, npcs,
            start_player, lists, zone, mission, mounts, start_time,
            map
        )

        logger_sys.log_message(f"INFO: Set mission '{mission_id}' as done")
        cout(COLOR_CYAN + COLOR_STYLE_BRIGHT + "You completed mission '" + mission_data["name"] + "'" + COLOR_RESET_ALL)
        player["active missions"].remove(mission_id)
        player["done missions"].append(mission_id)
