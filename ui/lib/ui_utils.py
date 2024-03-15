from PySide2.QtWidgets import *
import maya_tools.OpenMayaUI as omui
import shiboken2

def maya_main_window():
    mainWindowPointer = omui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(int(mainWindowPointer), QWidget)
