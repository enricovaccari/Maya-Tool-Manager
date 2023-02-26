#**********************************************************************************
# content		= includes supprts functions for various operation
#               = e.g. decorators, display data etc...
#
# version		= 1.0.0
# date			= 12-11-2022
#
# how to		= ...
# dependencies	= ...
# todos         = ...
# 
# license		= (e.g. MIT)
# author		= Enrico Vaccari <e.vaccari99@gmail.com>
#
# © ALL RIGHTS RESERVED
#**********************************************************************************

import os
import sys
import importlib as imp
# import webbrowser as wb 

import maya.cmds as cmds



#**********************************************************************************
# VARIABLES
#**********************************************************************************

SCRIPTS_PATH    = cmds.internalVar(usd=True)
MTM_PATH        = f'{SCRIPTS_PATH}maya_tool_manager'
UTILITIES_PATH  = f'{MTM_PATH}/utilities'

if UTILITIES_PATH not in sys.path:
    sys.path.append(UTILITIES_PATH)

import popup_functions as pf

try:
    imp.reload(pf)
except:
    reload(pf)

try:
    import yaml
except:
    YAML_PATH = f'{MTM_PATH}/lib/extern'
    if YAML_PATH not in sys.path:
        sys.path.append(YAML_PATH)
    import yaml


#**********************************************************************************
# FUNCTIONS
#**********************************************************************************

# decorator
def print_process(func):
    def wrapper(*args, **kwargs):
        
        print(f'\nSTART - {func.__name__}')
        start_time = time.time()
        
        if args: # if funct takes args
            func(args)
        else:
            func() # if funct takes no args

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f'END - {round(elapsed_time, 1)}\n')
                        
    return wrapper

# def init_yaml(path):
#    if not os.path.exists(path):
#       user_data = []
#       with open(path, 'w') as outfile:
#          yaml.dump(user_data, outfile, default_flow_style=False, allow_unicode=True)

# init_yaml('C:\Users\Vaccari\Documents\maya\2022\scripts\maya_tool_manager\validate\temp\test.yml')


def display_loaded(dir_list):
    tools_number = len(dir_list)
    if tools_number == 0:
      title = ''
      pf.general_warning(title, message)
    else:
        return f'-{tools_number} Loaded'

def display_validated(dir_list):
    tools_number = len(dir_list)
    if tools_number == 0:
        return f'{SCRIPTS_PATH} is currently empty'
    else:
        return f'-{tools_number} Loaded'


def custom_menu(name):
    delete_custom_menu(name)

    menu = cmds.menu(name, parent='MayaWindow',
                     label=name, helpMenu=True, tearOff=True)
    print(menu)
    

def delete_custom_menu(name):
    if cmds.menu(name, query=True, exists=True):
        cmds.deleteUI(name, menu=True)


def custom_shelf(name):
    delete_custom_shelf(name)

    shelf_layout = cmds.shelfLayout(name, parent="ShelfLayout")
    return shelf_layout


def delete_custom_shelf(name):
    if cmds.shelfLayout(name, exists=True):
        cmds.deleteUI(name)


# cmds.shelfButton(parent=name,
#                      annotation='evaccari_automatic_texture_plugger',
#                      image1=APP_DIR + '/OTHERS/ICONS/evaccari_automatic_texture_plugger_thumbnail.png',
#                      command='smfct.reload_modules();import UI_functions as ui;ui.create_UI()')

