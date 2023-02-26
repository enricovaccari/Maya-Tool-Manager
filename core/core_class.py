
#*********************************************************************************
# content      = identifies all the existing applications in the "scripts"
#              = of your installed Maya package
#
# version      = 1.0.0
# date         = 13-10-2022
# 
# todos        = fill out yaml with all the remaining data
#
# license      =
# author       = Enrico Vaccari <e.vaccari99@gmail.com>
# 
#**********************************************************************************


import os
import sys
import importlib as imp

import maya.cmds as cmds


#**********************************************************************************
# VARIABLES
#**********************************************************************************


SCRIPTS_PATH = cmds.internalVar(usd=True)

EXCEPTIONS   = ["userSetup.py", 'maya_tool_manager', 'Z_TESTS']
TYPE_TARGET   = 'tool_type'
TYPE_TARGETS = ['simple', 'UI-based']

simple_tools   = []
ui_based_tools = []


#**********************************************************************************
# FUNCTIONS
#**********************************************************************************


# LOAD ALL - tools list
def list_tools(folder_path): 
    """ Returns all the tools (directories) stored in the Maya scripts directory

    Args:
        folder_path (str): directory path target

    Returns:
        list: list of all the found items (files & directories)
    """    
    dir_list = os.listdir(folder_path)
    #  works with .encode so no need for raw strings
    
    for exception in EXCEPTIONS:
        if exception in dir_list:
            dir_list.remove(exception)
    
    return dir_list


#**********************************************************************************
# CLASS
#**********************************************************************************


class Tool:
    def __init__(self, name):
        self.name = name
        
        # self._print_infos()

    @property
    def path(self):
       path = SCRIPTS_PATH + self.name
       return path
    
    @property
    def content(self):
        content = os.listdir(self.path)
        return content


#**********************************************************************************


class Validated(Tool):
    def __init__(self, name):
        self.name = name

    @property
    def id_path(self):
        id_path = self.path + '/id'
        return id_path

    @property
    def id_content(self):
        id_content = os.listdir(self.id_path)
        return id_content

    @property
    def type(self):
        for file in self.id_content:
            if TYPE_TARGET in file:
                type = file.replace('tool_type_', '')
                type = type.replace('.txt', '')
    
        return type

    @property
    def thumbnail(self):
        for file in self.id_content:
            print(file)
            if 'jpg' in file or 'jpeg' in file  or 'png' in file:
                file_path = f'{self.id_path}/{file}'
                return file_path
        return None


    def access_tool(self):
        if self.path not in sys.path:
            sys.path.append(self.path)
    
    
    def classify(self):
        if self.type == TYPE_TARGETS[0]:
            simple_tools.append(self.name)
        elif self.type == TYPE_TARGETS[1]:
            ui_based_tools.append(self.name)


#**********************************************************************************
# EXECUTION
#**********************************************************************************

# parent = Tool('tool_01')
# child = Validated('tool_01')
 
# print(parent.name)
# print(parent.path)
# print(parent.content)
# print(child.type)
# print(child.id_content)
# print(child.thumbnail)