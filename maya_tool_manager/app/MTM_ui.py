#**********************************************************************************
# content		= User Interface for Maya Tool Manager (MTM UI)
#
# version		= 1.0.0
# date			= 21-11-2022
#
# how to		= start()
# dependencies	= Maya 2022, Qt, Python 3
# todos         = - optimise code even more
#                 - improve reset button
#                 - add useful popups
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
EXE_PATH        = f'{MTM_PATH}/exe'
UTILITIES_PATH  = f'{MTM_PATH}/utilities'
VAL_TOOLS_PATH  = f'{MTM_PATH}/validate/temp'
YAML_PATH       = f'{MTM_PATH}/lib/extern'
APP_PATH        = f'{MTM_PATH}/app'
UI_PATH         = f'{APP_PATH}/ui'
IMG_PATH        = f'{UI_PATH}/img'
LIB_PATH        = f'{MTM_PATH}/lib'
EXTERN_PATH     = f'{LIB_PATH}/extern'


# access MTM directory
if MTM_PATH not in sys.path:
    sys.path.append(MTM_PATH)


# core class import
from core import core_class as cc
imp.reload(cc)


# tool check import
from validate import tool_check as tc
imp.reload(tc)


# support tools import
from utilities import support_tools as st
imp.reload(st)
# Qt import


try:
    from Qt import QtWidgets, QtGui, QtCore, QtCompat
except:
    if EXTERN_PATH not in sys.path:
        sys.path.append(EXTERN_PATH)
        from Qt import QtWidgets, QtGui, QtCore, QtCompat


#**********************************************************************************
# CLASS
#**********************************************************************************


class MayaToolManager():

    # enable hiDPi
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    # QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    def __init__(self):
        
        #**********************************************************************************
        # LOADING UI 
        # absolute .ui file path
        ui_path = f'{UI_PATH}/MTM.ui'

        # loads UI with absolute path
        self.wgMTM = QtCompat.loadUi(ui_path)

        #**********************************************************************************
        # RECONNECTING ICONS
        # window
        self.wgMTM.setWindowIcon(QtGui.QPixmap(f'{IMG_PATH}/Maya_Icon.png'))

        # collapsable section (1)
        self.btnLoadValDownArrowImage = f'{IMG_PATH}/Down_Arrow.png'
        self.wgMTM.btnLoadValDownArrow.setIcon(QtGui.QPixmap(self.btnLoadValDownArrowImage))

        # collapsable section (2)
        self.btnMenusShelvesConfigDownArrowImage = f'{IMG_PATH}/Down_Arrow.png'
        self.wgMTM.btnMenusShelvesConfigDownArrow.setIcon(QtGui.QPixmap(self.btnMenusShelvesConfigDownArrowImage))

        # collapsable section (3)
        self.btnMenusShelvesCreateDownArrowImage = f'{IMG_PATH}/Down_Arrow.png'
        self.wgMTM.btnMenusShelvesCreateDownArrow.setIcon(QtGui.QPixmap(self.btnMenusShelvesCreateDownArrowImage))

        # footer
        self.wgMTM.btnEmail.setIcon(QtGui.QPixmap(f'{IMG_PATH}/Email.png'))
        self.wgMTM.btnHelp.setIcon(QtGui.QPixmap(f'{IMG_PATH}/Question_Mark.png'))

        #**********************************************************************************
        # SETTING UI TO DEFAULT
        self.press_btnReset()

        #**********************************************************************************
        # SIGNALS
        # core buttons
        self.wgMTM.btnReset.clicked.connect(self.press_btnReset)
        
        self.wgMTM.btnLoad.clicked.connect(self.press_btnLoad)
        self.wgMTM.btnValidate.clicked.connect(self.press_btnValidate)
 
        self.wgMTM.btnDefConfig.clicked.connect(self.press_btnDefConfig)
        self.wgMTM.btnStatusSimple.clicked.connect(self.press_btnStatusSimple)
        self.wgMTM.btnStatusUI.clicked.connect(self.press_btnStatusUI)

        self.wgMTM.btnCreateMenus.clicked.connect(self.press_btnCreateMenus)
        self.wgMTM.btnCreateShelves.clicked.connect(self.press_btnCreateShelves)

        self.wgMTM.btnApply.clicked.connect(self.press_btnApply)
        self.wgMTM.btnCreate.clicked.connect(self.press_btnCreate)

        # collapsable layouts
        self.wgMTM.btnLoadValDownArrow.clicked.connect(self.press_btnLoadValDownArrow)
        self.wgMTM.btnMenusShelvesConfigDownArrow.clicked.connect(self.press_btnMenusShelvesConfigDownArrow)
        self.wgMTM.btnMenusShelvesCreateDownArrow.clicked.connect(self.press_btnMenusShelvesCreateDownArrow)

        #**********************************************************************************
        # SHOWING UI
        self.wgMTM.show()


    #**********************************************************************************
    # CLASS FUNCTIONS
    def press_btnReset(self):
        """ Resets UI to default
        """        
        # changes icons to - down arrows -
        self.btnLoadValDownArrowImage = f'{IMG_PATH}/Down_Arrow.png'  
        self.btnMenusShelvesConfigDownArrowImage = f'{IMG_PATH}/Down_Arrow.png'
        self.btnMenusShelvesCreateDownArrowImage = f'{IMG_PATH}/Down_Arrow.png'
   
        # collapses sections 
        self.press_btnLoadValDownArrow()
        self.press_btnMenusShelvesConfigDownArrow()
        self.press_btnMenusShelvesCreateDownArrow()
    
        
        # resizes Ui to minimum
        self.wgMTM.resize(400,200)

        # disables specific buttons
        self.wgMTM.lblLoad.setText('- Loaded Tools - ')
        self.wgMTM.lblLoad.setStyleSheet('color: white;background-color: rgb(93, 93, 93)')

        self.wgMTM.btnValidate.setEnabled(False)
        self.wgMTM.btnValidate.setStyleSheet('color: rgb(160, 160, 160)')

        self.wgMTM.lblValidate.setText('- Validated Tools - ')
        self.wgMTM.lblValidate.setStyleSheet('color: white;background-color: rgb(93, 93, 93)')
        
        self.wgMTM.btnDefConfig.setEnabled(False)
        self.wgMTM.btnDefConfig.setStyleSheet('color: rgb(160, 160, 160)')

        self.wgMTM.btnStatusSimple.setEnabled(False)
        self.wgMTM.btnStatusSimple.setStyleSheet('color: rgb(160, 160, 160)')

        self.wgMTM.btnStatusUI.setEnabled(False)
        self.wgMTM.btnStatusUI.setStyleSheet('color: rgb(160, 160, 160)')

        self.wgMTM.btnCreateMenus.setEnabled(False)
        self.wgMTM.btnCreateMenus.setStyleSheet('color: rgb(160, 160, 160)')

        self.wgMTM.btnCreateShelves.setEnabled(False)
        self.wgMTM.btnCreateShelves.setStyleSheet('color: rgb(160, 160, 160)')

        self.wgMTM.btnCreate.setEnabled(False)
        self.wgMTM.btnCreate.setStyleSheet('color: rgb(160, 160, 160)')

        self.wgMTM.btnApply.setEnabled(False)
        self.wgMTM.btnApply.setStyleSheet('color: rgb(160, 160, 160)')


    def press_btnLoad(self):
        """ Loads all available tools in the maya scripts dir
        """        
        self.tools   = cc.list_tools(SCRIPTS_PATH)
        tools_amount = len(self.tools)
        
        # sets label Load and button Validate
        self.wgMTM.lblLoad.setText(f'- {tools_amount} Tools Loaded - ')
        self.wgMTM.lblLoad.setStyleSheet('background-color: rgb(93, 93, 93)')
        
        if tools_amount == 0:
            self.wgMTM.lblLoad.setStyleSheet('color: rgb(255, 0, 0);background-color: rgb(93, 93, 93)')
        else:
            self.wgMTM.lblLoad.setStyleSheet('color: rgb(143, 199, 37);background-color: rgb(93, 93, 93)')
            self.wgMTM.btnValidate.setEnabled(True)
            self.wgMTM.btnValidate.setStyleSheet("")


    def press_btnValidate(self):
        """ Validates the loaded tools
        """

        # fills the validated tools dictionary (iteratively)
        tc.validated_tools = {}
        for tool_name in self.tools:

            tool = cc.Tool(tool_name) # object initialization
            
            tool_path    = tool.path
            tool_content = tool.content

            id_check = tc.id_check(tool_path)
            main_check, main_target = tc.main_script_check(tool_path)
            check_sum = tc.check_sum(id_check, main_check)
            tc.append_if_valid(tool_name, tool_path, main_target, check_sum)
        
        # validated tools
        self.validated_tools = tc.validated_tools
        validated_tools_amount = len(self.validated_tools)

        # sets label Validate
        self.wgMTM.lblValidate.setText(f'- {validated_tools_amount} Tools Validated - ')

        # changes other buttons state
        if validated_tools_amount == 0:
            self.wgMTM.lblValidate.setStyleSheet('color: rgb(255, 0, 0); background-color: rgb(93, 93, 93)')
        else:
            self.wgMTM.lblValidate.setStyleSheet('color: rgb(143, 199, 37); background-color: rgb(93, 93, 93)')
            self.wgMTM.btnDefConfig.setEnabled(True)
            self.wgMTM.btnDefConfig.setStyleSheet('') # otherwise it overwrites it3

    def press_btnDefConfig(self):
        """ Sets default configuration for validated tools
        """        
        #**********************************************************************************
        # VALIDATED LISTS INITIALIZATION
        cc.simple_tools   = []
        cc.ui_based_tools = []

        #**********************************************************************************
        # CLASSIFYING TOOLS
        for validated in self.validated_tools:
            validated_tool = cc.Validated(validated)

            # accesses tool
            validated_tool.access_tool()

            # gets tool type 
            type = validated_tool.type
            self.validated_tools[validated][1] = type
            
            # gets thumbnail
            thumbnail_path = validated_tool.thumbnail
            print(thumbnail_path)
            self.validated_tools[validated][3] = thumbnail_path
            
            # classifies tool
            validated_tool.classify()

        simple_amount   = len(cc.simple_tools)
        ui_based_amount = len(cc.ui_based_tools)

        # changes other buttons state
        if simple_amount != 0 or ui_based_amount != 0:
            self.wgMTM.btnStatusSimple.setEnabled(True)
            self.wgMTM.btnStatusSimple.setStyleSheet('')

            self.wgMTM.btnStatusUI.setEnabled(True)
            self.wgMTM.btnStatusUI.setStyleSheet('')

        #**********************************************************************************
        # SIMPLE CHECKBOXES
        # deletes - simple - checkboxes if they exist
        for counter in reversed(range(self.wgMTM.verLaySimpleTools_3.count())):
            widget = self.wgMTM.verLaySimpleTools_3.itemAt(counter).widget()

            if widget is not None: 
                widget.setParent(None)

        # creates - simple - tools labels
        self.lblSimpleDefConfig = QtWidgets.QLabel(f'{simple_amount} Tools Loaded')
        
        if simple_amount == 0:
            self.lblSimpleDefConfig.setStyleSheet('color: red')
        else:
            self.lblSimpleDefConfig.setStyleSheet('color: rgb(143, 199, 37);border-width: 0px;font: italic')
        
        self.lblSimpleDefConfig.setMinimumHeight(20)
        self.lblSimpleDefConfig.setMaximumHeight(20)

        # dual alignment
        self.lblSimpleDefConfig.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.wgMTM.verLaySimpleTools_3.addWidget(self.lblSimpleDefConfig)
        
        # creates - simple - checkboxes
        for simple_validated in cc.simple_tools:
            self.cbSimple = QtWidgets.QCheckBox(simple_validated)
            self.cbSimple.setStyleSheet("color: white; border-width: 0px")                               
            self.cbSimple.setChecked(True)
            self.cbSimple.setMinimumHeight(20)
            self.cbSimple.setMaximumHeight(20)
            
            self.wgMTM.verLaySimpleTools_3.addWidget(self.cbSimple, alignment=QtCore.Qt.AlignTop)
      
        #**********************************************************************************
        # UI-BASED CHECKBOXES
        # deletes - ui-based - checkboxes if they exist
        for counter in reversed(range(self.wgMTM.verLayUITools_3.count())):
            widget = self.wgMTM.verLayUITools_3.itemAt(counter).widget()

            if widget is not None: 
                widget.setParent(None)

        # creates - ui-based - tools labels
        self.lblUIDefConfig = QtWidgets.QLabel(f'{ui_based_amount} Tools Loaded')
        
        if ui_based_amount == 0:
            self.lblUIDefConfig.setStyleSheet('color: red')
        else:
            self.lblUIDefConfig.setStyleSheet('color: rgb(143, 199, 37);border-width: 0px;font: italic')
        
        self.lblUIDefConfig.setMinimumHeight(20)
        self.lblUIDefConfig.setMaximumHeight(20)

        # dual alignment
        self.lblUIDefConfig.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.wgMTM.verLayUITools_3.addWidget(self.lblUIDefConfig)
        
        # creates - ui-based - checkboxes
        for ui_based_validated in cc.ui_based_tools:
            self.cbUIBased = QtWidgets.QCheckBox(ui_based_validated)
            self.cbUIBased.setStyleSheet("color: white; border-width: 0px")                               
            self.cbUIBased.setChecked(True)
            self.cbUIBased.setMinimumHeight(20)
            self.cbUIBased.setMaximumHeight(20)
            self.wgMTM.verLayUITools_3.addWidget(self.cbUIBased, alignment=QtCore.Qt.AlignTop)
        
        #**********************************************************************************
        # RESIZING CHECKBOX WIDGETS BASED ON TOOL AMOUNT
        difference = abs(simple_amount - ui_based_amount)
        multiplier = max(simple_amount, ui_based_amount)
        wgSize = 50 + multiplier * 20

        self.wgMTM.wgSimpleTools.setMinimumHeight(wgSize)
        self.wgMTM.wgSimpleTools.setMaximumHeight(wgSize)
        self.wgMTM.wgUITools.setMinimumHeight(wgSize)
        self.wgMTM.wgUITools.setMaximumHeight(wgSize)
        
        #**********************************************************************************
        # SMART CHECKBOX INTERACTIVE LAYOUT
        difference = abs(simple_amount - ui_based_amount)
        
        if simple_amount > ui_based_amount:
            for counter in range(difference):
                self.cbUISpacer = QtWidgets.QLabel('')
                self.cbUISpacer.setEnabled(False)
                self.cbUISpacer.setStyleSheet("border-width: 0px") 
                self.cbUISpacer.setMinimumHeight(20)
                self.cbUISpacer.setMaximumHeight(20)
                self.wgMTM.verLayUITools_3.addWidget(self.cbUISpacer, alignment=QtCore.Qt.AlignTop)
        
        if simple_amount < ui_based_amount:
            for counter in range(difference):
                self.cbSimpleSpacer = QtWidgets.QLabel('')
                self.cbSimpleSpacer.setEnabled(False)
                self.cbSimpleSpacer.setStyleSheet("border-width: 0px") 
                self.cbSimpleSpacer.setMinimumHeight(20)
                self.cbSimpleSpacer.setMaximumHeight(20)
                self.wgMTM.verLaySimpleTools_3.addWidget(self.cbSimpleSpacer, alignment=QtCore.Qt.AlignTop)


    def press_btnStatusSimple(self):
        """ Sets status (ACTIVE/PASSIVE) of - simple - tools
        """
        if self.wgMTM.btnStatusSimple.text() == 'STATUS (Simple): - PASSIVE -':
            self.wgMTM.btnStatusSimple.setStyleSheet('background-color: rgb(143, 199, 37)')
            self.wgMTM.btnStatusSimple.setText('STATUS (Simple): - ACTIVE -')
        elif self.wgMTM.btnStatusSimple.text() == 'STATUS (Simple): - ACTIVE -':
            self.wgMTM.btnStatusSimple.setStyleSheet('')
            self.wgMTM.btnStatusSimple.setText('STATUS (Simple): - PASSIVE -')

        if self.wgMTM.btnStatusSimple.text() == 'STATUS (Simple): - ACTIVE -' or  self.wgMTM.btnStatusUI.text() == 'STATUS (UI-based): - ACTIVE -':
            self.wgMTM.btnCreateMenus.setEnabled(True)
            self.wgMTM.btnCreateMenus.setStyleSheet('')
            self.wgMTM.btnCreateShelves.setEnabled(True)
            self.wgMTM.btnCreateShelves.setStyleSheet('')
        else:
            self.wgMTM.btnCreateMenus.setEnabled(False)
            self.wgMTM.btnCreateMenus.setStyleSheet('color: rgb(160, 160, 160)')
            self.wgMTM.btnCreateShelves.setEnabled(False)
            self.wgMTM.btnCreateShelves.setStyleSheet('color: rgb(160, 160, 160)')
    

    def press_btnStatusUI(self):
        """ Sets status (ACTIVE/PASSIVE) of - ui-based - tools
        """
        if self.wgMTM.btnStatusUI.text() == 'Status (UI-based): - PASSIVE -':
            self.wgMTM.btnStatusUI.setStyleSheet('background-color: rgb(143, 199, 37)')
            self.wgMTM.btnStatusUI.setText('STATUS (UI-based): - ACTIVE -')
        elif self.wgMTM.btnStatusUI.text() == 'STATUS (UI-based): - ACTIVE -':
            self.wgMTM.btnStatusUI.setStyleSheet('')
            self.wgMTM.btnStatusUI.setText('Status (UI-based): - PASSIVE -')

        if self.wgMTM.btnStatusSimple.text() == 'STATUS (Simple): - ACTIVE -' or  self.wgMTM.btnStatusUI.text() == 'STATUS (UI-based): - ACTIVE -':
            self.wgMTM.btnCreateMenus.setEnabled(True)
            self.wgMTM.btnCreateMenus.setStyleSheet('')
            self.wgMTM.btnCreateShelves.setEnabled(True)
            self.wgMTM.btnCreateShelves.setStyleSheet('')
        else:
            self.wgMTM.btnCreateMenus.setEnabled(False)
            self.wgMTM.btnCreateMenus.setStyleSheet('color: rgb(160, 160, 160)')
            self.wgMTM.btnCreateShelves.setEnabled(False)
            self.wgMTM.btnCreateShelves.setStyleSheet('color: rgb(160, 160, 160)')
    

    def press_btnCreateMenus(self):
        """ Changes menus creation state
        """
        if self.wgMTM.btnCreateMenus.text() == 'Create Menu(s): - PASSIVE -':
            self.wgMTM.btnCreateMenus.setStyleSheet('background-color: rgb(143, 199, 37)')
            self.wgMTM.btnCreateMenus.setText('Create Menu(s): - ACTIVE -')

        elif self.wgMTM.btnCreateMenus.text() == 'Create Menu(s): - ACTIVE -':
            self.wgMTM.btnCreateMenus.setStyleSheet('')
            self.wgMTM.btnCreateMenus.setText('Create Menu(s): - PASSIVE -')

        if self.wgMTM.btnCreateMenus.text() == 'Create Menu(s): - ACTIVE -' or  self.wgMTM.btnCreateShelves.text() == 'Create Shelf(ves): - ACTIVE -':
            self.wgMTM.btnApply.setEnabled(True)
            self.wgMTM.btnApply.setStyleSheet('')
            self.wgMTM.btnCreate.setEnabled(True)
            self.wgMTM.btnCreate.setStyleSheet('')
        else:
            self.wgMTM.btnApply.setEnabled(False)
            self.wgMTM.btnApply.setStyleSheet('color: rgb(160, 160, 160)')
            self.wgMTM.btnCreate.setEnabled(False)
            self.wgMTM.btnCreate.setStyleSheet('color: rgb(160, 160, 160)')
    
    def press_btnCreateShelves(self):
        """ Changes shelves creation state
        """
        if self.wgMTM.btnCreateShelves.text() == 'Create Shelf(ves): - PASSIVE -':
            self.wgMTM.btnCreateShelves.setStyleSheet('background-color: rgb(143, 199, 37)')
            self.wgMTM.btnCreateShelves.setText('Create Shelf(ves): - ACTIVE -')
        elif self.wgMTM.btnCreateShelves.text() == 'Create Shelf(ves): - ACTIVE -':
            self.wgMTM.btnCreateShelves.setStyleSheet('')
            self.wgMTM.btnCreateShelves.setText('Create Shelf(ves): - PASSIVE -')

        if self.wgMTM.btnCreateMenus.text() == 'Create Menu(s): - ACTIVE -' or  self.wgMTM.btnCreateShelves.text() == 'Create Shelf(ves): - ACTIVE -':
            self.wgMTM.btnApply.setEnabled(True)
            self.wgMTM.btnApply.setStyleSheet('')
            self.wgMTM.btnCreate.setEnabled(True)
            self.wgMTM.btnCreate.setStyleSheet('')
        else:
            self.wgMTM.btnApply.setEnabled(False)
            self.wgMTM.btnApply.setStyleSheet('color: rgb(160, 160, 160)')
            self.wgMTM.btnCreate.setEnabled(False)
            self.wgMTM.btnCreate.setStyleSheet('color: rgb(160, 160, 160)')
    
    def press_btnApply(self):
        """ Triggers menus/shelves creation
        """       
        #**********************************************************************************
        # CHECKED TOOLS LISTS INITIALIZATION
        self.checked_simple_tools   = []
        self.checked_ui_based_tools = []
        
        #**********************************************************************************
        # GETTING LIST OF CHECKED - SIMPLE - TOOLS
        for counter in range(self.wgMTM.verLaySimpleTools_3.count()):
            chBox   = self.wgMTM.verLaySimpleTools_3.itemAt(counter).widget()
            cb_type = chBox.__class__.__name__
            if cb_type == 'QCheckBox':
                if chBox.isChecked():
                    self.checked_simple_tools.append(chBox.text())

        #**********************************************************************************
        # GETTING LIST OF CHECKED - UI-BASED - TOOLS
        for counter in range(self.wgMTM.verLayUITools_3.count()):
            chBox   = self.wgMTM.verLayUITools_3.itemAt(counter).widget()
            cb_type = chBox.__class__.__name__
            if cb_type == 'QCheckBox':
                if chBox.isChecked():
                    self.checked_ui_based_tools.append(chBox.text())

        if self.wgMTM.btnCreateMenus.text() == 'Create Menu(s): - PASSIVE -' and self.wgMTM.btnCreateShelves.text() == 'Create Shelf(ves): - PASSIVE -':
            print(0) # popup

        else:
            # creates - simple - tools menu
            if self.wgMTM.btnStatusSimple.text() == 'STATUS (Simple): - ACTIVE -' and self.wgMTM.btnCreateMenus.text() == 'Create Menu(s): - ACTIVE -':
                root_name = self.wgMTM.lineEditRootName.text()
                if root_name == '- Insert Root Name -' or root_name == '0':
                    root_name = 'EV'
                
                # initializes - simple - tools menu
                menu_name = f'{root_name}_Simple_Tools_M'
                st.custom_menu(menu_name)

                # appends MTM to - simple - tools menu
                MTM_main = f'{EXE_PATH}/main.py'
                command  = f"import runpy;runpy.run_path(path_name='{MTM_main}')"

                cmds.menuItem(parent=f'MayaWindow|{root_name}_Simple_Tools_M', 
                              label='MTM',
                              command=command)

                # appends items to - simple - tools menu
                if len(self.checked_simple_tools) != 0:
                    for tool in self.checked_simple_tools:
                        tool_path = self.validated_tools[tool][0]
                        main      = self.validated_tools[tool][2]
                        command   = f"import runpy;runpy.run_path(path_name='{main}')"
    
                        cmds.menuItem(parent=f'MayaWindow|{root_name}_Simple_Tools_M', 
                                      label=tool,
                                      command=command)

                # appends HELP to - simple - tools menu
                command  = f"import webbrowser;webbrowser.open('https://github.com/enricovaccari/evaccari_assignments/wiki#introduction')"

                cmds.menuItem(parent=f'MayaWindow|{root_name}_Simple_Tools_M', 
                              label='HELP',
                              command=command)

            # creates - ui-based - menu
            if self.wgMTM.btnStatusUI.text() == 'STATUS (UI-based): - ACTIVE -' and self.wgMTM.btnCreateMenus.text() == 'Create Menu(s): - ACTIVE -':
                root_name = self.wgMTM.lineEditRootName.text()
                if root_name == '- Insert Root Name -' or root_name == '0':
                    root_name = 'EV'
                
                # initializes - ui-based - tools menu
                menu_name = f'{root_name}_UI_Tools_M'
                st.custom_menu(menu_name)

                # appends MTM to - ui-based - tools menu
                MTM_main = f'{EXE_PATH}/main.py'
                command  = f"import runpy;runpy.run_path(path_name='{MTM_main}')"

                cmds.menuItem(parent=f'MayaWindow|{root_name}_UI_Tools_M', 
                              label='MTM',
                              command=command)

                # appends items to - ui-based - tools menu
                if len(self.checked_ui_based_tools) != 0:
                    for tool in self.checked_ui_based_tools:
                        tool_path = self.validated_tools[tool][0]
                        main      = self.validated_tools[tool][2]
                        command   = f"import runpy;runpy.run_path(path_name='{main}')"

                        cmds.menuItem(parent=f'MayaWindow|{root_name}_UI_Tools_M', 
                                      label=tool,
                                      command=command)
                
                # appends HELP to - ui-based - tools menu
                command  = f"import webbrowser;webbrowser.open('https://github.com/enricovaccari/evaccari_assignments/wiki#introduction')"

                cmds.menuItem(parent=f'MayaWindow|{root_name}_UI_Tools_M', 
                              label='HELP',
                              command=command)

            # creates - simple - tools shelf
            if self.wgMTM.btnStatusSimple.text() == 'STATUS (Simple): - ACTIVE -' and self.wgMTM.btnCreateShelves.text() == 'Create Shelf(ves): - ACTIVE -':
                root_name = self.wgMTM.lineEditRootName.text()
                print(root_name)
                if root_name == '- Insert Root Name -' or root_name == '0':
                    root_name = 'EV'
                
                # initializes - simple - tools shelf
                shelf_name    = f'{root_name}_Simple_Tools_S'
                shelf_layout  = st.custom_shelf(shelf_name)
                
                # appends MTM to - simple - tools shelf
                MTM_main  = f'{EXE_PATH}/main.py'
                thumbnail = f'{IMG_PATH}/MTM_Thumbnail.png'
                command   = f"import runpy;runpy.run_path(path_name='{MTM_main}')"

                cmds.shelfButton(parent=shelf_layout, 
                                 annotation='MTM',
                                 image1=thumbnail,
                                 command=command)

                # appends separator to - simple - tools shelf
                thumbnail = f'{IMG_PATH}/ShelfSeparator.png'


                cmds.shelfButton(parent=shelf_layout, 
                                 annotation='ShelfSeparator',
                                 image1=thumbnail)

                # appends items to - simple - tools shelf
                if len(self.checked_simple_tools) != 0:
                    for tool in self.checked_simple_tools:
                        tool_path = self.validated_tools[tool][0]
                        main      = self.validated_tools[tool][2]
                        thumbnail = self.validated_tools[tool][3]
                        command = f"import runpy;runpy.run_path(path_name='{main}')"

                        cmds.shelfButton(parent=shelf_layout,
                                         annotation=tool,
                                         image1=thumbnail,
                                         command=command)

                # appends separator to - simple - tools shelf
                thumbnail = f'{IMG_PATH}/ShelfSeparator.png'

                cmds.shelfButton(parent=shelf_layout, 
                                 annotation='ShelfSeparator',
                                 image1=thumbnail)

                # appends HELP to - simple - tools shelf
                thumbnail = f'{IMG_PATH}/Help_Thumbnail.png'
                command  = f"import webbrowser;webbrowser.open('https://github.com/enricovaccari/evaccari_assignments/wiki#introduction')"

                cmds.shelfButton(parent=shelf_layout, 
                                 annotation='HELP',
                                 image1=thumbnail,
                                 command=command)

            # creates - ui-based - tools shelf
            if self.wgMTM.btnStatusUI.text() == 'STATUS (UI-based): - ACTIVE -' and self.wgMTM.btnCreateShelves.text() == 'Create Shelf(ves): - ACTIVE -':
                root_name = self.wgMTM.lineEditRootName.text()
                if root_name == '- Insert Root Name -' or root_name == '0':
                    root_name = 'EV'
                
                # initializes - ui-based - tools shelf
                shelf_name    = f'{root_name}_UI_Tools_S'
                shelf_layout  = st.custom_shelf(shelf_name)

                # appends MTM to - ui-based - tools shelf
                MTM_main  = f'{EXE_PATH}/main.py'
                thumbnail = f'{IMG_PATH}/MTM_Thumbnail.png'
                command   = f"import runpy;runpy.run_path(path_name='{MTM_main}')"

                cmds.shelfButton(parent=shelf_layout, 
                                 annotation='MTM',
                                 image1=thumbnail,
                                 command=command)

                # appends separator to - ui-based - tools shelf
                thumbnail = f'{IMG_PATH}/ShelfSeparator.png'


                cmds.shelfButton(parent=shelf_layout, 
                                 annotation='ShelfSeparator',
                                 image1=thumbnail)

                # appends items to - ui-based - tools shelf
                if len(self.checked_ui_based_tools) != 0:
                    for tool in self.checked_ui_based_tools:
                        tool_path = self.validated_tools[tool][0]
                        main      = self.validated_tools[tool][2]
                        thumbnail = self.validated_tools[tool][3]

                        command = f"import runpy;runpy.run_path(path_name='{main}')"
                        cmds.shelfButton(parent=shelf_layout,
                                         annotation=tool,
                                         image1=thumbnail,
                                         command=command)
    
                # appends separator to - ui-based - tools shelf
                thumbnail = f'{IMG_PATH}/ShelfSeparator.png'

                cmds.shelfButton(parent=shelf_layout, 
                                 annotation='ShelfSeparator',
                                 image1=thumbnail)

                # appends HELP to - ui-based - tools shelf
                thumbnail = f'{IMG_PATH}/Help_Thumbnail.png'
                command  = f"import webbrowser;webbrowser.open('https://github.com/enricovaccari/evaccari_assignments/wiki#introduction')"

                cmds.shelfButton(parent=shelf_layout, 
                                 annotation='HELP',
                                 image1=thumbnail,
                                 command=command)


    def press_btnCreate(self):
        """ Triggers menus/shelves creation and closes the UI
        """  
        self.press_btnApply()
        self.wgMTM.close()


    def press_btnLoadValDownArrow(self):
        """ Collapses/Expands the - Loading & Validation - section
        """        
        if self.btnLoadValDownArrowImage == f'{IMG_PATH}/Down_Arrow.png':
            self.btnLoadValDownArrowImage = f'{IMG_PATH}/Right_Arrow.png'
            self.wgMTM.btnLoadValDownArrow.setIcon(QtGui.QPixmap(self.btnLoadValDownArrowImage))
            
            # hiding widgets, buttons, labels
            self.wgMTM.btnLoad.hide()
            self.wgMTM.lblLoad.hide()
            self.wgMTM.btnValidate.hide()
            self.wgMTM.lblValidate.hide()
            self.wgMTM.lineEditRootName.hide()

        elif self.btnLoadValDownArrowImage == f'{IMG_PATH}/Right_Arrow.png':
            self.btnLoadValDownArrowImage = f'{IMG_PATH}/Down_Arrow.png'
            self.wgMTM.btnLoadValDownArrow.setIcon(QtGui.QPixmap(self.btnLoadValDownArrowImage))
            
            # showing widgets, buttons, labels
            self.wgMTM.btnLoad.show()
            self.wgMTM.lblLoad.show()
            self.wgMTM.btnValidate.show()
            self.wgMTM.lblValidate.show()
            self.wgMTM.lineEditRootName.show()

        self.smart_resize()


    def press_btnMenusShelvesConfigDownArrow(self):
        """ Collapses/Expands the - Menus & Shelves Configuration - section
        """  
        if self.btnMenusShelvesConfigDownArrowImage == f'{IMG_PATH}/Down_Arrow.png':
            self.btnMenusShelvesConfigDownArrowImage = f'{IMG_PATH}/Right_Arrow.png'
            self.wgMTM.btnMenusShelvesConfigDownArrow.setIcon(QtGui.QPixmap(self.btnMenusShelvesConfigDownArrowImage))
           
            # hiding widgets, buttons, labels
            self.wgMTM.btnDefConfig.hide()
            self.wgMTM.wgSimpleTools.hide()
            self.wgMTM.wgUITools.hide()
            self.wgMTM.btnStatusSimple.hide()
            self.wgMTM.btnStatusUI.hide()

        elif self.btnMenusShelvesConfigDownArrowImage == f'{IMG_PATH}/Right_Arrow.png':
            self.btnMenusShelvesConfigDownArrowImage = f'{IMG_PATH}/Down_Arrow.png'
            self.wgMTM.btnMenusShelvesConfigDownArrow.setIcon(QtGui.QPixmap(self.btnMenusShelvesConfigDownArrowImage))
            
            # showing widgets, buttons, labels
            self.wgMTM.btnDefConfig.show()
            self.wgMTM.wgSimpleTools.show()
            self.wgMTM.wgUITools.show()
            self.wgMTM.btnStatusSimple.show()
            self.wgMTM.btnStatusUI.show()

        self.smart_resize()


    def press_btnMenusShelvesCreateDownArrow(self):
        """ Collapses/Expands the - Menus & Shelves Creation - section
        """  
        if self.btnMenusShelvesCreateDownArrowImage == f'{IMG_PATH}/Down_Arrow.png':
            self.btnMenusShelvesCreateDownArrowImage = f'{IMG_PATH}/Right_Arrow.png'
            self.wgMTM.btnMenusShelvesCreateDownArrow.setIcon(QtGui.QPixmap(self.btnMenusShelvesCreateDownArrowImage))
           
            # hiding widgets, buttons, labels
            self.wgMTM.btnCreateMenus.hide()
            self.wgMTM.btnCreateShelves.hide()

        elif self.btnMenusShelvesCreateDownArrowImage == f'{IMG_PATH}/Right_Arrow.png':
            self.btnMenusShelvesCreateDownArrowImage = f'{IMG_PATH}/Down_Arrow.png'
            self.wgMTM.btnMenusShelvesCreateDownArrow.setIcon(QtGui.QPixmap(self.btnMenusShelvesCreateDownArrowImage))
            
            # showing widgets, buttons, labels
            self.wgMTM.btnCreateMenus.show()
            self.wgMTM.btnCreateShelves.show()
            
        self.smart_resize()


    def smart_resize(self):
        """ Resizes the UI when all sections are in their collapsed state
        """        
        self.wgMTM.resize(self.wgMTM.sizeHint())

        if self.btnLoadValDownArrowImage == f'{IMG_PATH}/Right_Arrow.png':
            pass
        else: 
            return
        if self.btnMenusShelvesConfigDownArrowImage == f'{IMG_PATH}/Right_Arrow.png':
            pass
        else:
            return
        if self.btnMenusShelvesCreateDownArrowImage == f'{IMG_PATH}/Right_Arrow.png':
            pass
        else:
            return

        self.wgMTM.resize(400,200)
         
            
def create():
    app = QtWidgets.QApplication(sys.argv)
    main_widget = MayaToolManager()
    sys.exit(app.exec_())

# DCC start
def start():
    global main_widget
    main_widget = MayaToolManager()


#**********************************************************************************
# DELETING MENUS IN MAYA
# st.delete_custom_menu('EV_Simple_Tools')
# st.delete_custom_menu('EV_UI_Tools')
# st.delete_custom_menu('_UI_Tools')


#**********************************************************************************
# START
#**********************************************************************************

start() # in DCC (Maya)



