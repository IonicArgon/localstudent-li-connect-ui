from PyQt5 import QtCore, QtWidgets

class GUI_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, help_window):
        super(GUI_MainWindow, self).__init__()
        self.setGeometry(50, 50, 700, 500)
        self.setWindowTitle("LocalStudent LinkedIn Connect")

        self.help_window = help_window
        self.link = None
        self.recruiter_name = None
        self.header_file = None
        self.cookie_file = None
        self.message_file = None
        self.has_started = False

        self._setup_ui()

    def _setup_ui(self):
        # create title at top of window
        self.title = QtWidgets.QLabel(self)
        self.title.setGeometry(QtCore.QRect(0, 0, 700, 50))
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

        # same above but for message file
        self.message_file_label = QtWidgets.QLabel(self)
        self.message_file_label.setGeometry(QtCore.QRect(25, 250, 175, 50))
        self.message_file_label.setText("Message File")
        self.message_file_label.setStyleSheet("font-size: 15px;")
        self.message_file_label.setAlignment(QtCore.Qt.AlignLeft)
        self.message_file_label.setObjectName("message-file-label")
        self.message_file_dialog = QtWidgets.QFileDialog(self)
        self.message_file_dialog.setGeometry(QtCore.QRect(25, 275, 175, 25))
        self.message_file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        self.message_file_dialog.setNameFilter("Text (*.txt)")
        self.message_file_dialog.fileSelected.connect(self._on_message_file_dialog_file_selected)
        self.message_file_line_edit = QtWidgets.QLineEdit(self)
        self.message_file_line_edit.setGeometry(QtCore.QRect(65, 275, 135, 25))
        self.message_file_line_edit.setReadOnly(True)
        self.message_file_line_edit.setObjectName("message-file-line-edit")
        self.message_file_button = QtWidgets.QPushButton(self)
        self.message_file_button.setGeometry(QtCore.QRect(25, 275, 30, 25))
        self.message_file_button.setIcon(folder_icon)
        self.message_file_button.clicked.connect(self._on_message_file_button_clicked)

        # button to show help window
        # justified to left, 25 px away from edge of window
        self.help_button = QtWidgets.QPushButton(self)
        self.help_button.setGeometry(QtCore.QRect(25, 325, 175, 25))
        self.help_button.setText("Help")
        self.help_button.setObjectName("help-button")
        self.help_button.setStyleSheet("font-size: 15px;")
        self.help_button.clicked.connect(self.help_window.show)

        # 25 px away from everything else, big text box for status updates
        # underneath, button to start sending requests
        self.status_text_box = QtWidgets.QTextEdit(self)
        self.status_text_box.setGeometry(QtCore.QRect(225, 75, 450, 240))
        self.status_text_box.setReadOnly(True)
        self.status_text_box.setObjectName("status-text-box")
        self.start_button = QtWidgets.QPushButton(self)
        self.start_button.setGeometry(QtCore.QRect(225, 325, 450, 25))
        self.start_button.setText("Start")
        self.start_button.setStyleSheet("font-size: 15px;")
        self.start_button.setObjectName("start-button")
        self.start_button.clicked.connect(self._on_start_button_clicked)

        QtCore.QMetaObject.connectSlotsByName(self)

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
            print(f"Got link: {self.link}")

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
            print(f"Got cookie file: {self.cookie_file}")

    def _on_cookie_file_button_clicked(self):
        self.cookie_file_dialog.open()

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
                print(f"Got message file: {self.message_file}")

    def _on_message_file_button_clicked(self):
        self.message_file_dialog.open()

    def _on_start_button_clicked(self):
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
    
    def get_message_file(self):
        return self.message_file
    
    def get_has_started(self):
        return self.has_started
    
    def add_status_text(self, text):
        self._update_status_text_box(text)

    def clear_status_text(self):
        self.status_text = []
        self.status_text_box.clear()
    