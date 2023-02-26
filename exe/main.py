#**********************************************************************************
# content		= MTM main script 
#
# version		= 1.0.0
# date			= 01-12-2022
#
# how to		= ui.start()
# dependencies	= Maya 2022, Qt, Python 3
# todos         = //
#                
#
# license		= MIT
# author		= Enrico Vaccari <e.vaccari99@gmail.com>
#
# © ALL RIGHTS RESERVED
#**********************************************************************************


import os
import sys
import webbrowser
import importlib as imp

import maya.cmds as cmds


#**********************************************************************************
# VARIABLES
#**********************************************************************************


SCRIPTS_PATH    = cmds.internalVar(usd=True)
MTM_PATH        = f'{SCRIPTS_PATH}maya_tool_manager'
APP_PATH        = f'{MTM_PATH}/app'

if APP_PATH not in sys.path:
    sys.path.append(APP_PATH)

import MTM_ui as ui
imp.reload(ui)
    

#**********************************************************************************
# START
#**********************************************************************************

ui.start()
