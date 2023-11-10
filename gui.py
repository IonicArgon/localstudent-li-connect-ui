import webbrowser
from PyQt5 import QtCore, QtWidgets

class GUI_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(GUI_MainWindow, self).__init__()
        self.setGeometry(50, 50, 900, 700)
        self.setWindowTitle("LocalStudent LinkedIn Connect")

        self.link = None
        self.recruiter_name = None
        self.header_file = None
        self.cookie_file = None
        self.recruiterlite_header_file = None
        self.recruiterlite_cookie_file = None
        self.message_file = None
        self.has_started = False
        self.can_start = 0
        self.can_count = 25
        self.can_end = 100
        self.connect_count = 10
        self.json_data = None

        self._setup_ui()

    def _setup_ui(self):
        # create title at top of window
        self.title = QtWidgets.QLabel(self)
        self.title.setGeometry(QtCore.QRect(0, 0, 900, 50))
        self.title.setText("LocalStudent LinkedIn Connect")
        self.title.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName("title")

        # label for link to recruiter lite search
        # one line edit under label for user to enter search link
        # justified to left, 25 px away from edge of window
        self.link_label = QtWidgets.QLabel(self)
        self.link_label.setGeometry(QtCore.QRect(25, 50, 175, 50))
        self.link_label.setText("Recruiter Lite Search Link")
        self.link_label.setStyleSheet("font-size: 15px;")
        self.link_label.setAlignment(QtCore.Qt.AlignLeft)
        self.link_label.setObjectName("link-label")
        self.link_line_edit = QtWidgets.QLineEdit(self)
        self.link_line_edit.setGeometry(QtCore.QRect(25, 75, 175, 25))
        self.link_line_edit.setObjectName("link-line-edit")
        self.link_line_edit.returnPressed.connect(self._on_link_line_edit_enter)

        # label for recruiter first name
        # one line edit under label for user to enter recruiter name
        # justified to left, 25 px away from edge of window
        self.recruiter_name_label = QtWidgets.QLabel(self)
        self.recruiter_name_label.setGeometry(QtCore.QRect(25, 100, 175, 50))
        self.recruiter_name_label.setText("Recruiter First Name")
        self.recruiter_name_label.setStyleSheet("font-size: 15px;")
        self.recruiter_name_label.setAlignment(QtCore.Qt.AlignLeft)
        self.recruiter_name_label.setObjectName("recruiter-name-label")
        self.recruiter_name_line_edit = QtWidgets.QLineEdit(self)
        self.recruiter_name_line_edit.setGeometry(QtCore.QRect(25, 125, 175, 25))
        self.recruiter_name_line_edit.setObjectName("recruiter-name-line-edit")
        self.recruiter_name_line_edit.returnPressed.connect(self._on_recruiter_name_line_edit_enter)

        # label for header file
        # file dialog under label for user to select header file
        # justified to left, 25 px away from edge of window
        # only .json files can be selected
        # uneditable one line edit under file dialog to show selected file
        # button on the left to one line edit to open file dialog
        folder_icon_provider = QtWidgets.QFileIconProvider()
        folder_icon = folder_icon_provider.icon(QtWidgets.QFileIconProvider.Folder)

        self.header_file_label = QtWidgets.QLabel(self)
        self.header_file_label.setGeometry(QtCore.QRect(25, 150, 175, 50))
        self.header_file_label.setText("Header File")
        self.header_file_label.setStyleSheet("font-size: 15px;")
        self.header_file_label.setAlignment(QtCore.Qt.AlignLeft)
        self.header_file_label.setObjectName("header-file-label")
        self.header_file_dialog = QtWidgets.QFileDialog(self)
        self.header_file_dialog.setGeometry(QtCore.QRect(25, 175, 175, 25))
        self.header_file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        self.header_file_dialog.setNameFilter("JSON (*.json)")
        self.header_file_dialog.fileSelected.connect(self._on_header_file_dialog_file_selected)
        self.header_file_line_edit = QtWidgets.QLineEdit(self)
        self.header_file_line_edit.setGeometry(QtCore.QRect(65, 175, 135, 25))
        self.header_file_line_edit.setReadOnly(True)
        self.header_file_line_edit.setObjectName("header-file-line-edit")
        self.header_file_button = QtWidgets.QPushButton(self)
        self.header_file_button.setGeometry(QtCore.QRect(25, 175, 30, 25))
        self.header_file_button.setIcon(folder_icon)
        self.header_file_button.clicked.connect(self._on_header_file_button_clicked)

        # same above but for cookie file
        self.cookie_file_label = QtWidgets.QLabel(self)
        self.cookie_file_label.setGeometry(QtCore.QRect(25, 200, 175, 50))
        self.cookie_file_label.setText("Cookie File")
        self.cookie_file_label.setStyleSheet("font-size: 15px;")
        self.cookie_file_label.setAlignment(QtCore.Qt.AlignLeft)
        self.cookie_file_label.setObjectName("cookie-file-label")
        self.cookie_file_dialog = QtWidgets.QFileDialog(self)
        self.cookie_file_dialog.setGeometry(QtCore.QRect(25, 225, 175, 25))
        self.cookie_file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        self.cookie_file_dialog.setNameFilter("JSON (*.json)")
        self.cookie_file_dialog.fileSelected.connect(self._on_cookie_file_dialog_file_selected)
        self.cookie_file_line_edit = QtWidgets.QLineEdit(self)
        self.cookie_file_line_edit.setGeometry(QtCore.QRect(65, 225, 135, 25))
        self.cookie_file_line_edit.setReadOnly(True)
        self.cookie_file_line_edit.setObjectName("cookie-file-line-edit")
        self.cookie_file_button = QtWidgets.QPushButton(self)
        self.cookie_file_button.setGeometry(QtCore.QRect(25, 225, 30, 25))
        self.cookie_file_button.setIcon(folder_icon)
        self.cookie_file_button.clicked.connect(self._on_cookie_file_button_clicked)

        # same above but for recruiter lite header file
        self.recruiterlite_header_file_label = QtWidgets.QLabel(self)
        self.recruiterlite_header_file_label.setGeometry(QtCore.QRect(25, 250, 175, 50))
        self.recruiterlite_header_file_label.setText("Recruiter Lite Header File")
        self.recruiterlite_header_file_label.setStyleSheet("font-size: 15px;")
        self.recruiterlite_header_file_label.setAlignment(QtCore.Qt.AlignLeft)
        self.recruiterlite_header_file_label.setObjectName("recruiterlite-header-file-label")
        self.recruiterlite_header_file_dialog = QtWidgets.QFileDialog(self)
        self.recruiterlite_header_file_dialog.setGeometry(QtCore.QRect(25, 275, 175, 25))
        self.recruiterlite_header_file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        self.recruiterlite_header_file_dialog.setNameFilter("JSON (*.json)")
        self.recruiterlite_header_file_dialog.fileSelected.connect(self._on_recruiterlite_header_file_dialog_file_selected)
        self.recruiterlite_header_file_line_edit = QtWidgets.QLineEdit(self)
        self.recruiterlite_header_file_line_edit.setGeometry(QtCore.QRect(65, 275, 135, 25))
        self.recruiterlite_header_file_line_edit.setReadOnly(True)
        self.recruiterlite_header_file_line_edit.setObjectName("recruiterlite-header-file-line-edit")
        self.recruiterlite_header_file_button = QtWidgets.QPushButton(self)
        self.recruiterlite_header_file_button.setGeometry(QtCore.QRect(25, 275, 30, 25))
        self.recruiterlite_header_file_button.setIcon(folder_icon)
        self.recruiterlite_header_file_button.clicked.connect(self._on_recruiterlite_header_file_button_clicked)

        # same above but for recruiter lite cookie file
        self.recruiterlite_cookie_file_label = QtWidgets.QLabel(self)
        self.recruiterlite_cookie_file_label.setGeometry(QtCore.QRect(25, 300, 175, 50))
        self.recruiterlite_cookie_file_label.setText("Recruiter Lite Cookie File")
        self.recruiterlite_cookie_file_label.setStyleSheet("font-size: 15px;")
        self.recruiterlite_cookie_file_label.setAlignment(QtCore.Qt.AlignLeft)
        self.recruiterlite_cookie_file_label.setObjectName("recruiterlite-cookie-file-label")
        self.recruiterlite_cookie_file_dialog = QtWidgets.QFileDialog(self)
        self.recruiterlite_cookie_file_dialog.setGeometry(QtCore.QRect(25, 325, 175, 25))
        self.recruiterlite_cookie_file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        self.recruiterlite_cookie_file_dialog.setNameFilter("JSON (*.json)")
        self.recruiterlite_cookie_file_dialog.fileSelected.connect(self._on_recruiterlite_cookie_file_dialog_file_selected)
        self.recruiterlite_cookie_file_line_edit = QtWidgets.QLineEdit(self)
        self.recruiterlite_cookie_file_line_edit.setGeometry(QtCore.QRect(65, 325, 135, 25))
        self.recruiterlite_cookie_file_line_edit.setReadOnly(True)
        self.recruiterlite_cookie_file_line_edit.setObjectName("recruiterlite-cookie-file-line-edit")
        self.recruiterlite_cookie_file_button = QtWidgets.QPushButton(self)
        self.recruiterlite_cookie_file_button.setGeometry(QtCore.QRect(25, 325, 30, 25))
        self.recruiterlite_cookie_file_button.setIcon(folder_icon)
        self.recruiterlite_cookie_file_button.clicked.connect(self._on_recruiterlite_cookie_file_button_clicked)

        # same above but for message file
        self.message_file_label = QtWidgets.QLabel(self)
        self.message_file_label.setGeometry(QtCore.QRect(25, 350, 175, 50))
        self.message_file_label.setText("Message File")
        self.message_file_label.setStyleSheet("font-size: 15px;")
        self.message_file_label.setAlignment(QtCore.Qt.AlignLeft)
        self.message_file_label.setObjectName("message-file-label")
        self.message_file_dialog = QtWidgets.QFileDialog(self)
        self.message_file_dialog.setGeometry(QtCore.QRect(25, 375, 175, 25))
        self.message_file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        self.message_file_dialog.setNameFilter("Text (*.txt)")
        self.message_file_dialog.fileSelected.connect(self._on_message_file_dialog_file_selected)
        self.message_file_line_edit = QtWidgets.QLineEdit(self)
        self.message_file_line_edit.setGeometry(QtCore.QRect(65, 375, 135, 25))
        self.message_file_line_edit.setReadOnly(True)
        self.message_file_line_edit.setObjectName("message-file-line-edit")
        self.message_file_button = QtWidgets.QPushButton(self)
        self.message_file_button.setGeometry(QtCore.QRect(25, 375, 30, 25))
        self.message_file_button.setIcon(folder_icon)
        self.message_file_button.clicked.connect(self._on_message_file_button_clicked)

        # field for can start, default 0
        self.can_start_label = QtWidgets.QLabel(self)
        self.can_start_label.setGeometry(QtCore.QRect(25, 400, 175, 50))
        self.can_start_label.setText("Candidate to Start At")
        self.can_start_label.setStyleSheet("font-size: 15px;")
        self.can_start_label.setAlignment(QtCore.Qt.AlignLeft)
        self.can_start_label.setObjectName("can-start-label")
        self.can_start_line_edit = QtWidgets.QLineEdit(self)
        self.can_start_line_edit.setGeometry(QtCore.QRect(25, 425, 175, 25))
        self.can_start_line_edit.setText("0")
        self.can_start_line_edit.setObjectName("can-start-line-edit")
        self.can_start_line_edit.returnPressed.connect(self._on_can_start_line_edit_enter)

        # same above but for can count, default 25
        self.can_count_label = QtWidgets.QLabel(self)
        self.can_count_label.setGeometry(QtCore.QRect(25, 450, 175, 50))
        self.can_count_label.setText("Candidates per Page")
        self.can_count_label.setStyleSheet("font-size: 15px;")
        self.can_count_label.setAlignment(QtCore.Qt.AlignLeft)
        self.can_count_label.setObjectName("can-count-label")
        self.can_count_line_edit = QtWidgets.QLineEdit(self)
        self.can_count_line_edit.setGeometry(QtCore.QRect(25, 475, 175, 25))
        self.can_count_line_edit.setText("25")
        self.can_count_line_edit.setObjectName("can-count-line-edit")
        self.can_count_line_edit.returnPressed.connect(self._on_can_count_line_edit_enter)

        # same above but for can end, default 100
        self.can_end_label = QtWidgets.QLabel(self)
        self.can_end_label.setGeometry(QtCore.QRect(25, 500, 175, 50))
        self.can_end_label.setText("Candidate to End At")
        self.can_end_label.setStyleSheet("font-size: 15px;")
        self.can_end_label.setAlignment(QtCore.Qt.AlignLeft)
        self.can_end_label.setObjectName("can-end-label")
        self.can_end_line_edit = QtWidgets.QLineEdit(self)
        self.can_end_line_edit.setGeometry(QtCore.QRect(25, 525, 175, 25))
        self.can_end_line_edit.setText("100")
        self.can_end_line_edit.setObjectName("can-end-line-edit")
        self.can_end_line_edit.returnPressed.connect(self._on_can_end_line_edit_enter)
        self.can_count_line_edit.setObjectName("can-count-line-edit")
        self.can_count_line_edit.returnPressed.connect(self._on_can_count_line_edit_enter)

        # field for how many connection to send in this batch
        # 25 px away from left edge, below everything currently
        # default 10
        self.connect_count_label = QtWidgets.QLabel(self)
        self.connect_count_label.setGeometry(QtCore.QRect(25, 550, 175, 50))
        self.connect_count_label.setText("Connections to Send")
        self.connect_count_label.setStyleSheet("font-size: 15px;")
        self.connect_count_label.setAlignment(QtCore.Qt.AlignLeft)
        self.connect_count_label.setObjectName("connect-count-label")
        self.connect_count_line_edit = QtWidgets.QLineEdit(self)
        self.connect_count_line_edit.setGeometry(QtCore.QRect(25, 575, 175, 25))
        self.connect_count_line_edit.setText("10")
        self.connect_count_line_edit.setObjectName("connect-count-line-edit")
        self.connect_count_line_edit.returnPressed.connect(self._on_connect_count_line_edit_enter)


        # help button opens help window, underneath all the fields
        self.help_button = QtWidgets.QPushButton(self)
        self.help_button.setGeometry(QtCore.QRect(25, 610, 175, 25))
        self.help_button.setText("Help")
        self.help_button.setStyleSheet("font-size: 15px;")
        self.help_button.setObjectName("help-button")
        self.help_button.clicked.connect(self._on_help_button_clicked)


        # 25 px away from everything else, big text box for status updates
        # underneath, button to start sending requests
        self.status_text_box = QtWidgets.QTextEdit(self)
        self.status_text_box.setGeometry(QtCore.QRect(225, 75, 625, 525))
        self.status_text_box.setReadOnly(True)
        self.status_text_box.setObjectName("status-text-box")
        self.start_button = QtWidgets.QPushButton(self)
        self.start_button.setGeometry(QtCore.QRect(225, 610, 625, 25))
        self.start_button.setText("Start")
        self.start_button.setStyleSheet("font-size: 15px;")
        self.start_button.setObjectName("start-button")
        self.start_button.clicked.connect(self._on_start_button_clicked)

        QtCore.QMetaObject.connectSlotsByName(self)

    def _truncate(self, text, length):
        if len(text) > length:
            return text[:length] + "..."
        return text

    def _on_link_line_edit_enter(self):
        link = self.link_line_edit.text()
        alert = QtWidgets.QMessageBox()
        if link == "":
            alert.setText("Please enter a link.")
            alert.setWindowTitle("Error - No Link")
            alert.setIcon(QtWidgets.QMessageBox.Warning)
            alert.exec_()
        elif "https://www.linkedin.com/talent/search/api" not in link:
            alert.setText("Please enter a valid link.")
            alert.setWindowTitle("Error - Invalid Link")
            alert.setIcon(QtWidgets.QMessageBox.Warning)
            alert.exec_()
        else:
            self.link = link
            self.add_status_text(f"Got link: {self._truncate(self.link, 50)}")
            print(f"Got link: {self._truncate(self.link, 100)}")

    def _on_recruiter_name_line_edit_enter(self):
        recruiter_name = self.recruiter_name_line_edit.text()
        alert = QtWidgets.QMessageBox()
        if recruiter_name == "":
            alert.setText("Please enter a name.")
            alert.setWindowTitle("Error - No Name")
            alert.setIcon(QtWidgets.QMessageBox.Warning)
            alert.exec_()
        else:
            self.recruiter_name = recruiter_name
            self.add_status_text(f"Got recruiter name: {self.recruiter_name}")
            print(f"Got recruiter name: {self.recruiter_name}")

    def _on_header_file_dialog_file_selected(self):
        header_file = self.header_file_dialog.selectedFiles()[0]
        alert = QtWidgets.QMessageBox()
        if header_file == "":
            alert.setText("Please select a file.")
            alert.setWindowTitle("Error - No File")
            alert.setIcon(QtWidgets.QMessageBox.Warning)
            alert.exec_()
        else:
            self.header_file = header_file
            self.header_file_line_edit.setText(self.header_file)
            self.add_status_text(f"Got header file: {self._truncate(self.header_file, 50)}")
            print(f"Got header file: {self.header_file}")

    def _on_header_file_button_clicked(self):
        self.header_file_dialog.open()

    def _on_cookie_file_dialog_file_selected(self):
        cookie_file = self.cookie_file_dialog.selectedFiles()[0]
        alert = QtWidgets.QMessageBox()
        if cookie_file == "":
            alert.setText("Please select a file.")
            alert.setWindowTitle("Error - No File")
            alert.setIcon(QtWidgets.QMessageBox.Warning)
            alert.exec_()
        else:
            self.cookie_file = cookie_file
            self.cookie_file_line_edit.setText(self.cookie_file)
            self.add_status_text(f"Got cookie file: {self._truncate(self.cookie_file, 50)}")
            print(f"Got cookie file: {self.cookie_file}")

    def _on_cookie_file_button_clicked(self):
        self.cookie_file_dialog.open()

    def _on_recruiterlite_header_file_dialog_file_selected(self):
        recruiterlite_header_file = self.recruiterlite_header_file_dialog.selectedFiles()[0]
        alert = QtWidgets.QMessageBox()
        if recruiterlite_header_file == "":
            alert.setText("Please select a file.")
            alert.setWindowTitle("Error - No File")
            alert.setIcon(QtWidgets.QMessageBox.Warning)
            alert.exec_()
        else:
            self.recruiterlite_header_file = recruiterlite_header_file
            self.recruiterlite_header_file_line_edit.setText(self.recruiterlite_header_file)
            self.add_status_text(f"Got recruiter lite header file: {self._truncate(self.recruiterlite_header_file, 50)}")
            print(f"Got recruiter lite header file: {self.recruiterlite_header_file}")

    def _on_recruiterlite_header_file_button_clicked(self):
        self.recruiterlite_header_file_dialog.open()

    def _on_recruiterlite_cookie_file_dialog_file_selected(self):
        recruiterlite_cookie_file = self.recruiterlite_cookie_file_dialog.selectedFiles()[0]
        alert = QtWidgets.QMessageBox()
        if recruiterlite_cookie_file == "":
            alert.setText("Please select a file.")
            alert.setWindowTitle("Error - No File")
            alert.setIcon(QtWidgets.QMessageBox.Warning)
            alert.exec_()
        else:
            self.recruiterlite_cookie_file = recruiterlite_cookie_file
            self.recruiterlite_cookie_file_line_edit.setText(self.recruiterlite_cookie_file)
            self.add_status_text(f"Got recruiter lite cookie file: {self._truncate(self.recruiterlite_cookie_file, 50)}")
            print(f"Got recruiter lite cookie file: {self.recruiterlite_cookie_file}")

    def _on_recruiterlite_cookie_file_button_clicked(self):
        self.recruiterlite_cookie_file_dialog.open()

    def _on_message_file_dialog_file_selected(self):
        message_file = self.message_file_dialog.selectedFiles()[0]
        alert = QtWidgets.QMessageBox()
        if message_file == "":
            alert.setText("Please select a file.")
            alert.setWindowTitle("Error - No File")
            alert.setIcon(QtWidgets.QMessageBox.Warning)
            alert.exec_()
        else:
            file_content = None
            with open(message_file, "r") as f:
                file_content = f.read()

            if file_content == "":
                alert.setText("Empty message.")
                alert.setWindowTitle("Error - Empty Message")
                alert.setIcon(QtWidgets.QMessageBox.Warning)
                alert.exec_()
            elif file_content.count("{recruiter_name}") != 1:
                alert.setText("Message must contain {recruiter_name} exactly once.")
                alert.setWindowTitle("Error - Invalid Message")
                alert.setIcon(QtWidgets.QMessageBox.Warning)
                alert.exec_()
            elif file_content.count("{lead_name}") != 1:
                alert.setText("Message must contain {lead_name} exactly once.")
                alert.setWindowTitle("Error - Invalid Message")
                alert.setIcon(QtWidgets.QMessageBox.Warning)
                alert.exec_()
            else:
                self.message_file = message_file
                self.message_file_line_edit.setText(self.message_file)
                self.add_status_text(f"Got message file: {self._truncate(self.message_file, 50)}")
                print(f"Got message file: {self.message_file}")

    def _on_message_file_button_clicked(self):
        self.message_file_dialog.open()

    def _on_can_start_line_edit_enter(self):
        can_start = self.can_start_line_edit.text()
        alert = QtWidgets.QMessageBox()
        if can_start == "":
            alert.setText("Please enter a number.")
            alert.setWindowTitle("Error - No Number")
            alert.setIcon(QtWidgets.QMessageBox.Warning)
            alert.exec_()
            self.can_start = None
        elif not can_start.isnumeric():
            alert.setText("Please enter a valid number.")
            alert.setWindowTitle("Error - Invalid Number")
            alert.setIcon(QtWidgets.QMessageBox.Warning)
            alert.exec_()
            self.can_start = None
        else:
            self.can_start = int(can_start)
            self.add_status_text(f"Got start candidate index: {self.can_start}")
            print(f"Got can start: {self.can_start}")

    def _on_can_count_line_edit_enter(self):
        can_count = self.can_count_line_edit.text()
        alert = QtWidgets.QMessageBox()
        if can_count == "":
            alert.setText("Please enter a number.")
            alert.setWindowTitle("Error - No Number")
            alert.setIcon(QtWidgets.QMessageBox.Warning)
            alert.exec_()
            self.can_count = None
        elif not can_count.isnumeric():
            alert.setText("Please enter a valid number.")
            alert.setWindowTitle("Error - Invalid Number")
            alert.setIcon(QtWidgets.QMessageBox.Warning)
            alert.exec_()
            self.can_count = None
        elif can_count == "0":
            alert.setText("Please enter a number greater than 0.")
            alert.setWindowTitle("Error - Invalid Number")
            alert.setIcon(QtWidgets.QMessageBox.Warning)
            alert.exec_()
            self.can_count = None
        else:
            self.can_count = int(can_count)
            self.add_status_text(f"Got candidates per page: {self.can_count}")
            print(f"Got can count: {self.can_count}")

    def _on_can_end_line_edit_enter(self):
        can_end = self.can_end_line_edit.text()
        alert = QtWidgets.QMessageBox()
        if can_end == "":
            alert.setText("Please enter a number.")
            alert.setWindowTitle("Error - No Number")
            alert.setIcon(QtWidgets.QMessageBox.Warning)
            alert.exec_()
            self.can_end = None
        elif not can_end.isnumeric():
            alert.setText("Please enter a valid number.")
            alert.setWindowTitle("Error - Invalid Number")
            alert.setIcon(QtWidgets.QMessageBox.Warning)
            alert.exec_()
            self.can_end = None
        elif can_end == "0":
            alert.setText("Please enter a number greater than 0.")
            alert.setWindowTitle("Error - Invalid Number")
            alert.setIcon(QtWidgets.QMessageBox.Warning)
            alert.exec_()
            self.can_end = None
        elif int(can_end) < self.can_start:
            alert.setText("Please enter a number greater than the start candidate.")
            alert.setWindowTitle("Error - Invalid Number")
            alert.setIcon(QtWidgets.QMessageBox.Warning)
            alert.exec_()
            self.can_end = None
        else:
            self.can_end = int(can_end)
            self.add_status_text(f"Got max number of candidates: {self.can_end}")
            print(f"Got can end: {self.can_end}")

    def _on_connect_count_line_edit_enter(self):
        connect_count = self.connect_count_line_edit.text()
        alert = QtWidgets.QMessageBox()
        if connect_count == "":
            alert.setText("Please enter a number.")
            alert.setWindowTitle("Error - No Number")
            alert.setIcon(QtWidgets.QMessageBox.Warning)
            alert.exec_()
            self.connect_count = None
        elif not connect_count.isnumeric():
            alert.setText("Please enter a valid number.")
            alert.setWindowTitle("Error - Invalid Number")
            alert.setIcon(QtWidgets.QMessageBox.Warning)
            alert.exec_()
            self.connect_count = None
        elif connect_count == "0":
            alert.setText("Please enter a number greater than 0.")
            alert.setWindowTitle("Error - Invalid Number")
            alert.setIcon(QtWidgets.QMessageBox.Warning)
            alert.exec_()
            self.connect_count = None
        else:
            new_connect_count = int(connect_count) + self.json_data["connections_sent_this_week"]
            if (new_connect_count > 100):
                alert.setText("Sending more than 100 connections this week could get you banned. Are you sure you want to continue?")
                alert.setWindowTitle("Warning - Sending More Than 100 Connections")
                alert.setIcon(QtWidgets.QMessageBox.Warning)
                alert.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                alert.setDefaultButton(QtWidgets.QMessageBox.No)
                response = alert.exec_()
                if response == QtWidgets.QMessageBox.No:
                    self.connect_count = None
                    return
            elif (int(connect_count) > 20):
                alert.setText("Sending more than 20 connections in a day could get you banned. Are you sure you want to continue?")
                alert.setWindowTitle("Warning - Sending More Than 20 Connections")
                alert.setIcon(QtWidgets.QMessageBox.Warning)
                alert.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                alert.setDefaultButton(QtWidgets.QMessageBox.No)
                response = alert.exec_()
                if response == QtWidgets.QMessageBox.No:
                    self.connect_count = None
                    return

            self.connect_count = int(connect_count)
            self.add_status_text(f"Got connections to send: {self.connect_count}")
            print(f"Got connect count: {self.connect_count}")

    def _on_help_button_clicked(self):
        webbrowser.open("https://gist.github.com/IonicArgon/3964896e92e81d260d933a681df08fcc")

    def _on_start_button_clicked(self):
        # check if all fields are filled
        alert = QtWidgets.QMessageBox()
        if self.link == None:
            alert.setText("Please enter a link.")
            alert.setWindowTitle("Error - No Link")
            alert.setIcon(QtWidgets.QMessageBox.Warning)
            alert.exec_()
            return
        elif self.recruiter_name == None:
            alert.setText("Please enter a name.")
            alert.setWindowTitle("Error - No Name")
            alert.setIcon(QtWidgets.QMessageBox.Warning)
            alert.exec_()
            return
        elif self.header_file == None:
            alert.setText("Please select a header file.")
            alert.setWindowTitle("Error - No Header File")
            alert.setIcon(QtWidgets.QMessageBox.Warning)
            alert.exec_()
            return
        elif self.cookie_file == None:
            alert.setText("Please select a cookie file.")
            alert.setWindowTitle("Error - No Cookie File")
            alert.setIcon(QtWidgets.QMessageBox.Warning)
            alert.exec_()
            return
        elif self.recruiterlite_header_file == None:
            alert.setText("Please select a recruiter lite header file.")
            alert.setWindowTitle("Error - No Recruiter Lite Header File")
            alert.setIcon(QtWidgets.QMessageBox.Warning)
            alert.exec_()
            return
        elif self.recruiterlite_cookie_file == None:
            alert.setText("Please select a recruiter lite cookie file.")
            alert.setWindowTitle("Error - No Recruiter Lite Cookie File")
            alert.setIcon(QtWidgets.QMessageBox.Warning)
            alert.exec_()
            return
        elif self.message_file == None:
            alert.setText("Please select a message file.")
            alert.setWindowTitle("Error - No Message File")
            alert.setIcon(QtWidgets.QMessageBox.Warning)
            alert.exec_()
            return
        elif self.can_start == None:
            alert.setText("Please enter a candidate to start at.")
            alert.setWindowTitle("Error - No Candidate to Start At")
            alert.setIcon(QtWidgets.QMessageBox.Warning)
            alert.exec_()
            return
        elif self.can_count == None:
            alert.setText("Please enter a number of candidates per page.")
            alert.setWindowTitle("Error - No Candidates per Page")
            alert.setIcon(QtWidgets.QMessageBox.Warning)
            alert.exec_()
            return
        elif self.can_end == None:
            alert.setText("Please enter a candidate to end at.")
            alert.setWindowTitle("Error - No Candidate to End At")
            alert.setIcon(QtWidgets.QMessageBox.Warning)
            alert.exec_()
            return
        

        if (self.has_started == False):
            self.start_button.setText("Stop")
            self.has_started = True
            self._update_status_text_box("Starting...")
            print("Received start signal.")
        else:
            self.start_button.setText("Start")
            self.has_started = False
            self._update_status_text_box("Stopping...")
            print("Received stop signal.")

    def _update_status_text_box(self, text):
        text = text + "\n"
        self.status_text_box.insertPlainText(text)
        self.status_text_box.verticalScrollBar().setValue(self.status_text_box.verticalScrollBar().maximum())

    # public
    def get_link(self):
        return self.link
    
    def get_recruiter_name(self):
        return self.recruiter_name
    
    def get_header_file(self):
        return self.header_file
    
    def get_cookie_file(self):
        return self.cookie_file
    
    def get_recruiterlite_header_file(self):
        return self.recruiterlite_header_file
    
    def get_recruiterlite_cookie_file(self):
        return self.recruiterlite_cookie_file
    
    def get_message_file(self):
        return self.message_file
    
    def get_can_start(self):
        return self.can_start
    
    def get_can_count(self):
        return self.can_count
    
    def get_can_end(self):
        return self.can_end
    
    def get_connect_count(self):
        return self.connect_count
    
    def get_has_started(self):
        return self.has_started
    
    def add_status_text(self, text):
        self._update_status_text_box(text)

    def clear_status_text(self):
        self.status_text = []
        self.status_text_box.clear()

    def set_json_data(self, json_data):
        self.json_data = json_data

    def reset_start_button(self):
        self.start_button.setText("Start")
        self.has_started = False

    def fill_previous_data(self, **kwargs) -> None:
        self.add_status_text("Filling previous data...")

        if kwargs["recruiter_name"]:
            self.recruiter_name = kwargs["recruiter_name"]
            self.recruiter_name_line_edit.setText(self.recruiter_name)
            self.add_status_text(f"\tGot recruiter name: {self.recruiter_name}")
            print(f"Got recruiter name: {self.recruiter_name}")
        
        if kwargs["recruiterlite_header_file"]:
            self.recruiterlite_header_file = kwargs["recruiterlite_header_file"]
            self.recruiterlite_header_file_line_edit.setText(self.recruiterlite_header_file)
            self.add_status_text(f"\tGot recruiter lite header file: {self._truncate(self.recruiterlite_header_file, 50)}")
            print(f"Got recruiter lite header file: {self.recruiterlite_header_file}")

        if kwargs["recruiterlite_cookie_file"]:
            self.recruiterlite_cookie_file = kwargs["recruiterlite_cookie_file"]
            self.recruiterlite_cookie_file_line_edit.setText(self.recruiterlite_cookie_file)
            self.add_status_text(f"\tGot recruiter lite cookie file: {self._truncate(self.recruiterlite_cookie_file, 50)}")
            print(f"Got recruiter lite cookie file: {self.recruiterlite_cookie_file}")

        if kwargs["header_file"]:
            self.header_file = kwargs["header_file"]
            self.header_file_line_edit.setText(self.header_file)
            self.add_status_text(f"\tGot header file: {self._truncate(self.header_file, 50)}")
            print(f"Got header file: {self.header_file}")

        if kwargs["cookie_file"]:
            self.cookie_file = kwargs["cookie_file"]
            self.cookie_file_line_edit.setText(self.cookie_file)
            self.add_status_text(f"\tGot cookie file: {self._truncate(self.cookie_file, 50)}")
            print(f"Got cookie file: {self.cookie_file}")

        if kwargs["message_file"]:
            self.message_file = kwargs["message_file"]
            self.message_file_line_edit.setText(self.message_file)
            self.add_status_text(f"\tGot message file: {self._truncate(self.message_file, 50)}")
            print(f"Got message file: {self.message_file}")
