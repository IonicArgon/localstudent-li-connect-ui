import sys
from gui import GUI_MainWindow
from gui_help import GUI_Help
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication([])
    help_window = GUI_Help()
    window = GUI_MainWindow(help_window=help_window)
    window.show()

    # temporary for testing
    import threading
    def random_status():
        import random
        import time
        while True:
            window.add_status_text("Status: " + str(random.randint(0, 100)))
            time.sleep(1)
    
    thread = threading.Thread(target=random_status)
    thread.daemon = True
    thread.start()
    sys.exit(app.exec_())
