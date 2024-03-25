import pymel.core as pm
import ui.cap_tool_ui as cap_tool_ui

class InnestheticMenu:
    def __init__(self):
        self.menu_name = "Innesthetic"
        self.cap_tool_menu_item = {"label": "ALL_CAPS", "command": self.launch_cap_tool}

        if pm.menu(self.menu_name, exists=True):
            pm.deleteUI(self.menu_name)

        self.menu = pm.menu(self.menu_name, label=self.menu_name, parent="MayaWindow")
        pm.menuItem(label = self.cap_tool_menu_item["label"], command = pm.Callback(self.cap_tool_menu_item["command"]))

    def launch_cap_tool(self):
        cap_tool_ui.create_ui()

def create_menu():
    innesthetic_menu = InnestheticMenu()

if __name__ == "__main__":
    from importlib import reload
    reload(cap_tool_ui)
    create_menu()

