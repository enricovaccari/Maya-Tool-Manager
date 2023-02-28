#**********************************************************************************
# content		= popup functions used for different purposes
#               = general warning, check popup, type popup...
#
# version		= 1.0.0
# date			= 20-10-2022
#
# how to		= general_warning(), check_popup(), type_popup()
# dependencies	= ...
# todos         = ...
# 
# license		= (e.g. MIT)
# author		= Enrico Vaccari <e.vaccari99@gmail.com>
#
# © ALL RIGHTS RESERVED
#**********************************************************************************


import sys
import maya.cmds as cmds


#**********************************************************************************
# VARIABLES
#**********************************************************************************


SCRIPTS_PATH    = cmds.internalVar(usd=True)
MTM_PATH        = f'{SCRIPTS_PATH}maya_tool_manager'
YAML_PATH       = f'{MTM_PATH}/lib/extern'

try:
    import yaml
except:
    if YAML_PATH not in sys.path:
        sys.path.append(YAML_PATH)
    import yaml

# access user_config.yaml
yaml_file = MTM_PATH + '/config/user_config.yml'
with open(yaml_file, 'r') as stream:
    user_config = yaml.safe_load(stream)


#**********************************************************************************
# FUNCTIONS
#**********************************************************************************


def general_warning(title, message): 
   result = cmds.confirmDialog(title=title,
                               message=message,
                               button=user_config['general_warning']['button'],
                               icon=user_config['general_warning']['icon'],
                               defaultButton=user_config['general_warning']['defaultButton'],
                               cancelButton=user_config['general_warning']['cancelButton'],
                               dismissString=user_config['general_warning']['dismissString'],
                               messageAlign=user_config['general_warning']['messageAlign'],
                               backgroundColor=user_config['general_warning']['backgroundColor'])


def check_popup(title, message): 
   result = cmds.confirmDialog(title=title,
                               message=message,
                               button=['YES', 'NO', 'HELP'],
                               icon='warning',
                               defaultButton='YES',
                               cancelButton= 'NO',
                               dismissString = 'NO',
                               messageAlign='center',
                               backgroundColor=[0.80, 0.58, 0.00])
   return result

def type_popup(title, message): # set them to None
   result = cmds.confirmDialog(title=title,
                               message=message,
                               button=['SIMPLE', 'UI-BASED', 'CANCEL'],
                               icon='warning',
                               defaultButton='SIMPLE',
                               cancelButton= 'CANCEL',
                               dismissString = 'CANCEL',
                               messageAlign='center',
                               backgroundColor=[0.4, 0.6, 0.2])
   return result


def browse_main_target(tool_path):
   # has to be python file
   # add starting directory in Maya Automatic Texture Plugger
   main_target = cmds.fileDialog2(buttonBoxOrientation=1,
                                  caption='Select Main Target',
                                  dialogStyle=2,
                                  fileFilter='*.py',
                                  fileMode=1,
                                  okCaption='SELECT',
                                  cancelCaption='CANCEL',
                                  startingDirectory=tool_path)
   return main_target