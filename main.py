import sys
from gui import GUI_MainWindow
from gui_help import GUI_Help
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication([])
    help_window = GUI_Help()
    window = GUI_MainWindow(help_window=help_window)
    window.show()
    sys.exit(app.exec_())
