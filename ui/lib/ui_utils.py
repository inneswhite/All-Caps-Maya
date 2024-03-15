from PySide2.QtWidgets import *
import maya.OpenMayaUI as omui
import shiboken2
import os
import sys
import ui 

def maya_main_window():
    """Return a shiboken2 wrap instance for the main Maya window

    Returns:
        wrapInstance: Maya main window
    """    
    mainWindowPointer = omui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(int(mainWindowPointer), QWidget)

def get_abs_icon_dir():
    """Returns:
        str: absolute path to icons directory
    """    
    ui_path = os.path.dirname(ui.__file__)
    icon_dir = os.path.join(ui_path, "resources\\icons")
    return icon_dir

def get_icon_file(file_name: str):
    """Returns the full absolute path to an icon file

    Args:
        file_name (str): the name of the icon file

    Returns:
        str: full path for icon file
    """    
    rel_icon_path = os.path.join(get_abs_icon_dir(), file_name)
    return rel_icon_path
