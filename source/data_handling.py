import appdirs
import logger_sys
import check_yaml
import colors
import os
import git
import shutil
import tempfile
import yaml
import time
import text_handling
import fsspec
import time
from rich.progress import Progress
from colorama import Fore, Back, Style, init, deinit
from colors import *

# initialize colorama
init()

# Get program add directory
program_dir = str(appdirs.user_config_dir(appname='Bane-Of-Wargs'))

# Handling functions


def load_game_data(which_type, what_plugin=None):

    # Check if the which_type variable is valid,
    # so if it is not either 'vanilla' or
    # 'plugin' which is inputted, send error
    # and stop the program immediately
    if which_type != 'vanilla' and which_type != 'plugin':
        logger_sys.log_message(f"ERROR: Yaml data loading inputted key '{which_type}' is not valid --> crashing program")
        print(
            f"{COLOR_RED}ERROR: {COLOR_STYLE_BRIGHT}Yaml" +
            f"data loading inputted key '{which_type}' is not valid --> crashing program{COLOR_RESET_ALL}"
        )
        time.sleep(5)
        text_handling.exit_game()

    # If the inputted which_type is vanilla, then just
    # load the vanilla game data

    if which_type == 'vanilla':
        logger_sys.log_message("INFO: Loading vanilla game data")
        with Progress() as progress:

            task1 = progress.add_task("[cyan]Loading Data...", total=22)
    
            while not progress.finished:

                with open(program_dir + "/game/data/map.yaml") as f:
                    map = yaml.safe_load(f)
                    progress.update(task1, advance=1)
                    check_yaml.examine(program_dir + '/game/data/map.yaml')
                progress.update(task1, advance=1)

                with open(program_dir + "/game/data/items.yaml") as f:
                    item = yaml.safe_load(f)
                    progress.update(task1, advance=1)
                    check_yaml.examine(program_dir + '/game/data/items.yaml')
                progress.update(task1, advance=1)

                with open(program_dir + "/game/data/drinks.yaml") as f:
                    drinks = yaml.safe_load(f)
                    progress.update(task1, advance=1)
                    check_yaml.examine(program_dir + '/game/data/drinks.yaml')
                progress.update(task1, advance=1)

                with open(program_dir + "/game/data/enemies.yaml") as f:
                    enemy = yaml.safe_load(f)
                    progress.update(task1, advance=1)
                    check_yaml.examine(program_dir + '/game/data/enemies.yaml')
                progress.update(task1, advance=1)

                with open(program_dir + "/game/data/npcs.yaml") as f:
                    npcs = yaml.safe_load(f)
                    progress.update(task1, advance=1)
                    check_yaml.examine(program_dir + '/game/data/npcs.yaml')
                progress.update(task1, advance=1)

                with open(program_dir + "/game/data/start.yaml") as f:
                    start_player = yaml.safe_load(f)
                    progress.update(task1, advance=1)
                    check_yaml.examine(program_dir + '/game/data/start.yaml')
                progress.update(task1, advance=1)

                with open(program_dir + "/game/data/lists.yaml") as f:
                    lists = yaml.safe_load(f)
                    progress.update(task1, advance=1)
                    check_yaml.examine(program_dir + '/game/data/lists.yaml')
                progress.update(task1, advance=1)

                with open(program_dir + "/game/data/zone.yaml") as f:
                    zone = yaml.safe_load(f)
                    progress.update(task1, advance=1)
                    check_yaml.examine(program_dir + '/game/data/zone.yaml')
                progress.update(task1, advance=1)

                with open(program_dir + "/game/data/dialog.yaml") as f:
                    dialog = yaml.safe_load(f)
                    progress.update(task1, advance=1)
                    check_yaml.examine(program_dir + '/game/data/dialog.yaml')
                progress.update(task1, advance=1)

                with open(program_dir + "/game/data/mission.yaml") as f:
                    mission = yaml.safe_load(f)
                    progress.update(task1, advance=1)
                    check_yaml.examine(program_dir + '/game/data/mission.yaml')
                progress.update(task1, advance=1)

                with open(program_dir + "/game/data/mounts.yaml") as f:
                    mounts = yaml.safe_load(f)
                    progress.update(task1, advance=1)
                    check_yaml.examine(program_dir + '/game/data/mounts.yaml')
                progress.update(task1, advance=1)

    else:
        logger_sys.log_message(f"INFO: Loading plugin '{what_plugin}' data")
        check_file = os.path.exists(program_dir + "/plugins/" + what_plugin)
        if not check_file:
            print(COLOR_RED + COLOR_STYLE_BRIGHT + "ERROR: Couldn't find plugin '" + what_plugin + "'" + COLOR_RESET_ALL)
            logger_sys.log_message(f"ERROR: Couldn't find plugin '{what_plugin}'")
            play = 0
            text_handling.exit_game()
     
        with Progress() as progress:

            task1 = progress.add_task("[cyan]Loading Data...", total=22)

            while not progress.finished:
                with open(program_dir + "/plugins/" + what_plugin + "/map.yaml") as f:
                    map = yaml.safe_load(f)
                    progress.update(task1, advance=1)
                    check_yaml.examine(program_dir + "/plugins/" + what_plugin + "/map.yaml")
                progress.update(task1, advance=1)

                with open(program_dir + "/plugins/" + what_plugin + "/items.yaml") as f:
                    item = yaml.safe_load(f)
                    progress.update(task1, advance=1)
                    check_yaml.examine(program_dir + "/plugins/" + what_plugin + "/items.yaml")
                progress.update(task1, advance=1)

                with open(program_dir + "/plugins/" + what_plugin + "/drinks.yaml") as f:
                    drinks = yaml.safe_load(f)
                    progress.update(task1, advance=1)
                    check_yaml.examine(program_dir + "/plugins/" + what_plugin + "/drinks.yaml")
                progress.update(task1, advance=1)

                with open(program_dir + "/plugins/" + what_plugin + "/enemies.yaml") as f:
                    enemy = yaml.safe_load(f)
                    progress.update(task1, advance=1)
                    check_yaml.examine(program_dir + "/plugins/" + what_plugin + "/enemies.yaml")
                progress.update(task1, advance=1)

                with open(program_dir + "/plugins/" + what_plugin + "/npcs.yaml") as f:
                    npcs = yaml.safe_load(f)
                    progress.update(task1, advance=1)
                    check_yaml.examine(program_dir + "/plugins/" + what_plugin + "/npcs.yaml")
                progress.update(task1, advance=1)

                with open(program_dir + "/plugins/" + what_plugin + "/start.yaml") as f:
                    start_player = yaml.safe_load(f)
                    progress.update(task1, advance=1)
                    check_yaml.examine(program_dir + "/plugins/" + what_plugin + "/start.yaml")
                progress.update(task1, advance=1)

                with open(program_dir + "/plugins/" + what_plugin + "/lists.yaml") as f:
                    lists = yaml.safe_load(f)
                    progress.update(task1, advance=1)
                    check_yaml.examine(program_dir + "/plugins/" + what_plugin + "/lists.yaml")
                progress.update(task1, advance=1)

                with open(program_dir + "/plugins/" + what_plugin + "/zone.yaml") as f:
                    zone = yaml.safe_load(f)
                    progress.update(task1, advance=1)
                    check_yaml.examine(program_dir + "/plugins/" + what_plugin + "/zone.yaml")
                progress.update(task1, advance=1)

                with open(program_dir + "/plugins/" + what_plugin + "/dialog.yaml") as f:
                    dialog = yaml.safe_load(f)
                    progress.update(task1, advance=1)
                    check_yaml.examine(program_dir + "/plugins/" + what_plugin + "/dialog.yaml")
                progress.update(task1, advance=1)

                with open(program_dir + "/plugins/" + what_plugin + "/mission.yaml") as f:
                    mission = yaml.safe_load(f)
                    progress.update(task1, advance=1)
                    check_yaml.examine(program_dir + "/plugins/" + what_plugin + "/mission.yaml")
                progress.update(task1, advance=1)

                with open(program_dir + "/plugins/" + what_plugin + "/mounts.yaml") as f:
                    mounts = yaml.safe_load(f)
                    progress.update(task1, advance=1)
                    check_yaml.examine(program_dir + "/plugins/" + what_plugin + "/mounts.yaml")
                progress.update(task1, advance=1)

    return map, item, drinks, enemy, npcs, start_player, lists, zone, dialog, mission, mounts


def fsspec_download(github_file, destination_point, download_branch, download_repo, download_org):
    try:
        destination = destination_point
        fs = fsspec.filesystem("github", org=download_org, repo=download_repo, sha=download_branch)
        fs.get(fs.ls(github_file), destination)
    except Exception as error:
        print(
            COLOR_YELLOW + COLOR_STYLE_BRIGHT + "WARNING:" + COLOR_RESET_ALL +
            " an error occurred when trying to download game data to '" +
            destination + "'."
        )
        logger_sys.log_message(f"WARNING: An error occurred when downloading game data to '{destination}'.")
        logger_sys.log_message("DEBUG: " + str(error))
        print(COLOR_YELLOW + str(error) + COLOR_RESET_ALL)
        time.sleep(.5)


def temporary_git_file_download(selected_file):
    global file_text_data
    # Create a temporary directory to after
    # clone the repository and select the chosen
    # file and export its data in a string

    temporary_dir = tempfile.mkdtemp()
    logger_sys.log_message(f"INFO: Creating temporary directory at '{temporary_dir}'")
    git.Repo.clone_from('https://github.com/Dungeons-of-Kathallion/Bane-Of-Wargs.wiki.git', temporary_dir, depth=1)

    with open(temporary_dir + '/' + selected_file, 'r') as f:
        file_text_data = f.read()

    return file_text_data


# deinitialize colorama
deinit()
