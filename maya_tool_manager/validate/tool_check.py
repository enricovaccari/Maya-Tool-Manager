#**********************************************************************************
# content		= checks if tool has id/tool_type
#               = writes out data in yaml file (temp)
#
# version		= 1.0.0
# date			= 27-10-2022
#
# how to		= id_check(tool_path)
#                 main_script_check(tool_path)
#                 check_sum(id_check, main_check)
#                 append_if_valid(tool_name, tool_path, main_target, check_sum)
#
# dependencies	= Maya 2022, Qt, Python 3
# todos         = - optimise code
# 
# license		= MIT
# author		= Enrico Vaccari <e.vaccari99@gmail.com>
#
# © ALL RIGHTS RESERVED
#**********************************************************************************

import os
import sys
import importlib as imp
import webbrowser as wb 

import maya.cmds as cmds


#**********************************************************************************
# VARIABLES
#**********************************************************************************


SCRIPTS_PATH    = cmds.internalVar(usd=True)
MTM_PATH        = f'{SCRIPTS_PATH}maya_tool_manager'
UTILITIES_PATH  = f'{MTM_PATH}/utilities'
VAL_TOOLS_PATH  = f'{MTM_PATH}/validate/temp'
YAML_PATH       = f'{MTM_PATH}/lib/extern'

ID_TARGETS      = 'tool_type'

validated_tools = {}

if UTILITIES_PATH not in sys.path:
    sys.path.append(UTILITIES_PATH)

import popup_functions as pf


imp.reload(pf)


try:
    import yaml
except:
    if YAML_PATH not in sys.path:
        sys.path.append(YAML_PATH)
    import yaml

yaml_file = MTM_PATH + '/config/user_config.yml'
with open(yaml_file, 'r') as stream:
    user_config = yaml.safe_load(stream)


#**********************************************************************************
# FUNCTIONS
#**********************************************************************************


# VALIDATE (1) - id dir/tool_type
def id_check(tool_path):
    """ Checks if tool has id directory/tool_type

    Args:
        tool_path (str): full tool path

    Returns:
        int: returns 0 if tool does NOT pass the check, 1 if it does 
    """   

    #******************************************************************************
    # INITIALIZATION
    id_path    = tool_path + '/id'
    tool_name  = os.path.splitext(os.path.basename(tool_path))[0]

    #******************************************************************************
    # checks if id directory for given tool exists
    if not os.path.isdir(id_path):
        title   = 'ID CHECK POPUP WINDOW (missing directory)'
        message = f'WAIT! The following tool: {tool_name} has currently no <id> directory. Do you want to create one? If not, this tool will be skipped.' 
        result  = pf.check_popup(title, message)
        
        if result == 'YES':
            os.mkdir(id_path)
        elif result == 'NO':
            return 0
        elif result == 'HELP':
            print('HELP')
            wb.open('https://github.com/enricovaccari/evaccari_assignments/wiki')
            return 0
        
    #******************************************************************************
    # if id directory exists
    id_content = os.listdir(id_path)
    id_content = sorted(id_content)
    check_name = False
    check_type = False

    for file in id_content:
        # checks if tool_type.txt file exist
        if ID_TARGETS in file:
            check_type = True
    
    #******************************************************************************
    # if tool_type does NOT exist (create one?)
    title   = 'ID CHECK POPUP WINDOW (missing file)'

    if check_type == False:
        message = f'WAIT! The following tool: {tool_name} has currently no <tool_type.txt> file. Do you want to create one? If not, this tool will be skipped.' 
        result  = pf.check_popup(title, message)
        
        if result == 'YES':
            title = 'TOOL TYPE WINDOW (choose)'
            message = f'What is the type of {tool_name}?'
            chosen_type = pf.type_popup(title, message)
            
            if chosen_type == 'SIMPLE':
                file_name = 'tool_type_simple.txt'
                file_path = f'{id_path}/{file_name}'
                with open(file_path, 'w') as outfile:
                    pass
            elif chosen_type == 'UI-BASED':
                file_name = 'tool_type_UI-based.txt'
                file_path = f'{id_path}/{file_name}'
                with open(file_path, 'w') as outfile:
                    pass

            elif chosen_type == 'CANCEL':
                return 0

        elif result == 'NO':
            return 0
        elif result == 'HELP':
            print('HELP')
            # wb.open('insert link of Wiki')
            return 0
    
    return 1


# VALIDATE (2) - main script
def main_script_check(tool_path):
    """
    Checks if tool has main.py file

    Args:
        tool_path (str): full tool path

    Returns:
        list: [0 if tool does NOT pass the check / 1 if it does + main file path]
    """  

    #******************************************************************************
    # INIT
    check        = 1
    tool_name    = os.path.splitext(os.path.basename(tool_path))[0]
    tool_content = os.listdir(tool_path)
    
    #******************************************************************************
    # if main module does not exist
    main_target = f'{tool_path}/main.py'
    if "main.py" not in tool_content:
        title   = 'MAIN SCRIPT WINDOW (missing file)'
        message = f'WAIT! The following tool: {tool_name} has currently no <main.py> file. Do you want to select a target file acting as a main? If not, this tool will be skipped' 
        result  = pf.check_popup(title, message)
        
        if result == 'YES':
            main_target = pf.browse_main_target(tool_path)[0]
        elif result == 'NO':
            return 0, None
        elif result == 'HELP':
            wb.open('https://github.com/enricovaccari/evaccari_assignments/wiki')
            return 0, None


    return 1, main_target

def check_sum(id_check, main_check):
    check_sum = id_check + main_check
    return check_sum

# VALIDATE (3) - append to validates
def append_if_valid(tool_name, tool_path, main_target, check_sum):
    if check_sum == 2:
        validated_tools[tool_name] = [tool_path, None, main_target, None] # tool_path, type, main file path, thumbnail path
    # else returns None
    return


#**********************************************************************************
# EXECUTION
#**********************************************************************************


# id_check(tool_path)
# main_script_check(tool_path)
# check_sum(id_check, main_check)
# append_if_valid(tool_name, tool_path, main_target, check_sum)