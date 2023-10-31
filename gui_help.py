from PyQt5 import QtWidgets, QtCore, QtGui

class Paragraph(QtWidgets.QLabel):
    def __init__(self, parent=None, text=""):
        super().__init__(parent=parent)

        self.setText(text)
        self.setStyleSheet("font-size: 14px;")
        self.setWordWrap(True)
        self.setAlignment(QtCore.Qt.AlignLeft)
        self.setObjectName("paragraph")

class Header(QtWidgets.QLabel):
    def __init__(self, parent=None, text=""):
        super().__init__(parent=parent)

        self.setText(text)
        self.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.setAlignment(QtCore.Qt.AlignLeft)
        self.setObjectName("header")

class GUI_Help(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LocalStudent LinkedIn Connect - Help")
        self.resize(600, 400)

        self._setup_ui()
    
    def _setup_ui(self):
        # title at top
        self.title = QtWidgets.QLabel(parent=self)
        self.title.setText("Help Page")
        self.title.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setGeometry(0, 0, 600, 50)
        self.title.setObjectName("title")

        self.intro_paragraph = Paragraph(parent=self, text="This is the help page, where you will find information on how to use this application")     
        self.intro_paragraph.setGeometry(25, 50, 550, 350)
        self.recruiter_lite_scrape_header = Header(parent=self, text="Getting the Recruiter Lite URL")
        self.recruiter_lite_scrape_header.setGeometry(25, 100, 550, 50)




