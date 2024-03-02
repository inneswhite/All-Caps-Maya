from PySide2.QtWidgets import QMessageBox
import ui.lib.ui_utils as utils

class Dialog(QMessageBox):
    def __init__(self, parent=utils.maya_main_window()):
        super(Dialog, self).__init__(parent)

dialog = Dialog()

def info(message):
    dialog.setIcon(QMessageBox.Information)
    dialog.setText(message)
    dialog.show()

def warning(message):
    dialog.setIcon(QMessageBox.Warning)
    dialog.setText(message)
    dialog.show()

def critical(message):
    dialog.setIcon(QMessageBox.Critical)
    dialog.setText(message)
    dialog.show()


# if main, likely debugging.
if __name__ == "__main__":
    info("Running UI file as main.")