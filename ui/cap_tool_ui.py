from PySide2.QtWidgets import *
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya_tools.cap_tool
from maya_tools.cap_tool import maya_cap
import ui.lib.ui_utils as utils
import importlib
import pymel.core as pm

importlib.reload(maya_tools.cap_tool)
tool_name = "Cap Tool"

#TODO: Display the number of tris/ faces created

class CapToolUI(MayaQWidgetDockableMixin, QDialog):
    def __init__(self, parent=utils.maya_main_window()):
        ##TODO Switch out depending on Maya or 3ds Max
        super(CapToolUI,self).__init__(parent)

        self.setWindowTitle(tool_name)
        self.setGeometry(100, 100, 300, 200)

        self.create_widgets()
        self.init_callbacks()
        self.create_layout()
        self.set_window_size()

        self.destroyed.connect(self.on_destroyed)

    def create_widgets(self):
        self.cap_type_group_box = QGroupBox("Cap Type")

        self.fan_button = QPushButton("Fan")
        self.fan_button.clicked.connect(maya_cap.create_fan_cap)
        self.fan_button.setEnabled(maya_cap.validate_selection())

        self.strip_button = QPushButton("Strip")
        self.strip_button.clicked.connect(maya_cap.create_strip_cap)
        self.strip_button.setEnabled(maya_cap.validate_selection())

        self.grid_button = QPushButton("Grid")
        self.grid_button.setEnabled(maya_cap.validate_selection())

        self.optimised_button = QPushButton("Optimised")
        self.optimised_button.setEnabled(maya_cap.validate_selection())

        #TODO: Add apply button
        self.ok_button = self.create_generic_button("OK")
        self.ok_button.clicked.connect(self.confirm)

        self.cancel_button = self.create_generic_button("Cancel")
        self.cancel_button.clicked.connect(self.close)

    def set_button_states(self):
        self.fan_button.setEnabled(maya_cap.validate_selection())
        self.strip_button.setEnabled(maya_cap.validate_selection())
        self.grid_button.setEnabled(maya_cap.validate_selection())
        self.optimised_button.setEnabled(maya_cap.validate_selection())
    
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

    def on_destroyed(self):
        self.deleteLater()

    """ CALLBACKS """
    def init_callbacks(self):
        selection_changed_cb = pm.scriptJob(event=["SelectionChanged", self.set_button_states])

cap_tool_ui = CapToolUI()

def create_ui():
    cap_tool_ui.show(dockable=True)

if __name__ == "__main__":
    create_ui()
