# TODO Refactor import statements
from PySide2.QtWidgets import *
from PySide2 import QtGui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya_tools
from maya_tools.cap_tool import Cap_Type, maya_cap
import ui.lib.ui_utils as utils

import pymel.core as pm

tool_name = "Cap Tool"

# TODO: Display the number of tris/ faces created
import importlib
import sys


def m_reload():
    importlib.reload(maya_tools)
    importlib.reload(maya_tools.cap_tool)


class CapToolUI(MayaQWidgetDockableMixin, QDialog):
    def __init__(self, parent=utils.maya_main_window()):
        ##TODO Switch out depending on Maya or 3ds Max
        super(CapToolUI, self).__init__(parent)

        self.maya_cap = maya_cap
        self.setWindowTitle(tool_name)
        self.setGeometry(100, 100, 300, 200)

        self.create_widgets()
        self.init_callbacks()
        self.create_layout()
        self.set_window_size()

        self.destroyed.connect(self.on_destroyed)

    def create_widgets(self):
        # Make edge selection infobox
        self.make_edge_selection_gb = QGroupBox()

        self.make_edge_selection_lbl = QLabel("Make an edge selection to get started.")
        self.edge_selection_info_icon = QLabel("")
        info_icon = QtGui.QIcon(utils.get_icon_file("maya/info.png"))
        self.edge_selection_info_icon.setPixmap(info_icon.pixmap(32, 32))

        # Cap Type Selection
        # TODO Highlight selected cap
        self.cap_type_gb = QGroupBox("Cap Type")

        self.fan_button = self.create_cap_button(Cap_Type.fan, "", "icon-fan.png")
        self.strip_button = self.create_cap_button(Cap_Type.strip, "", "icon-strip.png")
        self.grid_button = self.create_cap_button(Cap_Type.grid, "", "icon-grid.png")
        self.max_area_button = self.create_cap_button(
            Cap_Type.max_area, "", "icon-max-area.png"
        )

        # Cap Options
        self.cap_options_gb = QGroupBox("Cap Options")
        self.rotate_cap_lb = QLabel("Rotate Cap:")
        self.rotate_cap_sb = QSpinBox()

        # OK Cancel Apply
        self.ok_button = self.create_generic_button("OK", self.confirm)
        self.cancel_button = self.create_generic_button("Cancel", self.cancel)
        self.apply_button = self.create_generic_button("Apply")

    def set_button_states(self):
        self.fan_button.setEnabled(self.maya_cap.validate_selection())
        self.strip_button.setEnabled(self.maya_cap.validate_selection())
        self.grid_button.setEnabled(self.maya_cap.validate_selection())
        self.max_area_button.setEnabled(self.maya_cap.validate_selection())

        self.make_edge_selection_gb.setHidden(self.maya_cap.validate_selection())

    def create_layout(self):
        # Widgets -> Layouts
        # --- Edge Selection Infobox
        make_edge_selection_layout = QHBoxLayout()
        make_edge_selection_layout.addWidget(self.edge_selection_info_icon)
        make_edge_selection_layout.addWidget(self.make_edge_selection_lbl)

        # --- Cap Types
        cap_type_layout = QHBoxLayout()
        cap_type_layout.addWidget(self.fan_button)
        cap_type_layout.addWidget(self.strip_button)
        cap_type_layout.addWidget(self.grid_button)
        cap_type_layout.addWidget(self.max_area_button)

        # --- Cap Options
        cap_options_layout = QHBoxLayout()
        cap_options_layout.addWidget(self.rotate_cap_lb)
        cap_options_layout.addWidget(self.rotate_cap_sb)

        # --- OK CLOSE APPLY
        self.ok_close_layout = QHBoxLayout()
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.ok_close_layout.addItem(spacer)
        self.ok_close_layout.addWidget(self.ok_button)
        self.ok_close_layout.addWidget(self.cancel_button)
        self.ok_close_layout.addWidget(self.apply_button)

        # Group Boxes
        self.make_edge_selection_gb.setLayout(make_edge_selection_layout)
        self.cap_type_gb.setLayout(cap_type_layout)
        self.cap_options_gb.setLayout(cap_options_layout)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.make_edge_selection_gb)
        main_layout.addWidget(self.cap_type_gb)
        main_layout.addWidget(self.cap_options_gb)
        main_layout.addLayout(self.ok_close_layout)
        self.setLayout(main_layout)

    def set_window_size(self):
        self.adjustSize()

    def default_cap_action(self):
        print("No method assigned to cap button")

    def create_generic_button(self, name="button", clicked_method=default_cap_action):
        generic_button = QPushButton(name)
        generic_button.setMinimumSize(70, 0)
        generic_button.setSizePolicy(
            QSizePolicy.Minimum,
            QSizePolicy.Fixed,
        )
        generic_button.clicked.connect(clicked_method)
        return generic_button

    def create_cap_button(
        self, cap_type=Cap_Type.fan, name="cap_button", icon_filename=""
    ):
        cap_button = QPushButton(name)
        cap_button.clicked.connect(lambda: self.maya_cap.create_cap(cap_type))
        cap_button.setEnabled(self.maya_cap.validate_selection())

        if icon_filename != "":
            cap_icon = QtGui.QIcon(utils.get_icon_file(icon_filename))
            cap_button.setIcon(cap_icon)
        return cap_button

    def confirm(self):
        # TODO set up ok button functionality
        print("todo")
        self.close()

    def cancel(self):
        self.maya_cap.revert_state()
        self.close()

    def on_destroyed(self):
        self.deleteLater()

    """ CALLBACKS """

    def init_callbacks(self):
        selection_changed_cb = pm.scriptJob(
            event=["SelectionChanged", self.set_button_states]
        )


cap_tool_ui = CapToolUI()


def create_ui():
    cap_tool_ui.show(dockable=True)


if __name__ == "__main__":
    create_ui()
    m_reload()
