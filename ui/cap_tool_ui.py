from PySide2 import QtCore
from PySide2.QtWidgets import *
import pymel.core as pm
import maya.OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import shiboken2
import cap_tool

tool_name = "Cap Tool"

def maya_main_window():
    mainWindowPointer = omui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(int(mainWindowPointer), QWidget)

class CapToolUI(MayaQWidgetDockableMixin, QDialog):
    def __init__(self, parent=maya_main_window()):
        super(CapToolUI,self).__init__(parent)

        self.setWindowTitle(tool_name)
        self.setGeometry(100, 100, 300, 200)

        self.create_widgets()
        self.create_layout()
        self.set_window_size()

    def create_widgets(self):
        self.cap_type_group_box = QGroupBox("Cap Type")

        self.fan_button = QPushButton("Fan")
        self.fan_button.clicked.connect(cap_tool.create_fan_cap)

        self.strip_button = QPushButton("Strip")
        self.grid_button = QPushButton("Grid")
        self.optimised_button = QPushButton("Optimised")

        self.ok_button = self.create_generic_button("OK")
        self.ok_button.clicked.connect(self.confirm)

        self.cancel_button = self.create_generic_button("Cancel")
        self.cancel_button.clicked.connect(self.close)
    
    def create_layout(self):
        cap_type_layout = QHBoxLayout()
        cap_type_layout.addWidget(self.fan_button)
        cap_type_layout.addWidget(self.strip_button)
        cap_type_layout.addWidget(self.grid_button)
        cap_type_layout.addWidget(self.optimised_button)

        self.cap_type_group_box.setLayout(cap_type_layout)

        self.ok_close_layout = QHBoxLayout()
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.ok_close_layout.addItem(spacer)
        self.ok_close_layout.addWidget(self.ok_button)
        self.ok_close_layout.addWidget(self.cancel_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.cap_type_group_box)
        main_layout.addLayout(self.ok_close_layout)
        self.setLayout(main_layout)

    def set_window_size(self):
        self.adjustSize()

    def create_generic_button(self, name):
        generic_button = QPushButton(name)
        generic_button.setMinimumSize(70,0)
        generic_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed,)
        return generic_button
    
    def confirm(self):
        #TODO set up ok button functionality
        print("todo")
        self.close()


cap_tool_ui = CapToolUI()

def create_ui():
    cap_tool_ui.show(dockable=True)

if __name__ == "__main__":
    create_ui()
