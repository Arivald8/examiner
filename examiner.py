import sys, subprocess

from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import (QLineEdit, QPushButton,
    QVBoxLayout, QLabel)

"""

For this application to work as intended, Task Manager must
be disabled in the CTRL + ALT + DEL menu. 

To disable Task Manager navigate to:
--> Local Group Policy Editor 
--> User Configuration
--> Administrative Templates 
--> System 
--> Ctrl + Alt + Del Options
--> Remove Task Manager.

"""

class Examiner(QtWidgets.QWidget):
    """ 
    This widget allows to lock a computer by terminating the explorer process.
    Once explorer is terminated, a password must be provided to then bring the GUI back.
    The widget allow provides buttons to launch other applications as needed. 
    """
    def __init__(self):
        super().__init__()

        self.lock = QtWidgets.QPushButton("Lock")
        self.unlock = QtWidgets.QPushButton("Unlock")

        self.word = QtWidgets.QPushButton("Word")
        self.player = QtWidgets.QPushButton("Media Player")

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.lock)
        layout.addWidget(self.unlock)
        layout.addWidget(self.word)
        layout.addWidget(self.player)

        self.setLayout(layout)
        
        self.lock.clicked.connect(self.terminator)
        self.unlock.clicked.connect(self.unlocker)
        self.word.clicked.connect(self.word_launch)
        self.player.clicked.connect(self.player_launch)

    def terminator(self):
        subprocess.call("powershell.exe taskkill /F /IM explorer.exe", shell=True)
        examiner.close()
        authenticator.show()

    def unlocker(self):
        subprocess.call("powershell.exe Start-Process explorer.exe", shell=True)

    def word_launch(self):
        subprocess.call("powershell.exe Start-Process WINWORD.EXE", shell=True)

    def player_launch(self):
        subprocess.call("powershell.exe Start-Process wmplayer.exe", shell=True)


class Authenticator(QtWidgets.QWidget):
    """ 
    Authenticator widget dispalys a password prompt and validates against user input.
    This validation is necessary for unlocking the computer once it has been locked.
    """
    def __init__(self, admin_password, parent=None):
        super(Authenticator, self).__init__(parent)

        self.admin_password = admin_password

        self.password_label = QLabel("Password: ", alignment=QtCore.Qt.AlignCenter)
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.button = QPushButton("Unlock")

        layout = QVBoxLayout()
        layout.addWidget(self.password_label)
        layout.addWidget(self.password)
        layout.addWidget(self.button)

        self.setLayout(layout)

        self.button.clicked.connect(self.validate_password)

    def validate_password(self):
        if self.password.text() == self.admin_password:
            self.password.clear()
            examiner.show()
            authenticator.close()


class Setter(QtWidgets.QWidget):
    """ Password setter widget. Allows exam admins to set a session password."""

    def __init__(self, parent=None):
        super(Setter, self).__init__(parent)

        self.new_password_label = QLabel("Set a new password: ", alignment=QtCore.Qt.AlignCenter)
        self.new_password = QLineEdit()
        self.new_password.setEchoMode(QLineEdit.Password)

        self.pass_confirm_label = QLabel("Confirm password: ", alignment=QtCore.Qt.AlignCenter)
        self.pass_confirm = QLineEdit()
        self.pass_confirm.setEchoMode(QLineEdit.Password)

        self.button = QPushButton("Set Password")

        layout = QVBoxLayout()
        layout.addWidget(self.new_password_label)
        layout.addWidget(self.new_password)
        layout.addWidget(self.pass_confirm_label)
        layout.addWidget(self.pass_confirm)
        layout.addWidget(self.button)

        self.setLayout(layout)

        self.button.clicked.connect(self.set_pass)

    def set_pass(self):
        if self.new_password.text() == self.pass_confirm.text():
            authenticator.admin_password = self.pass_confirm.text()
            self.new_password.clear()
            self.pass_confirm.clear()
            authenticator.show()
            pass_config.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    pass_config = Setter()
    pass_config.resize(300, 100)
    pass_config.setWindowTitle('Examiner')
    pass_config.show()

    authenticator = Authenticator(pass_config.new_password.text())
    authenticator.resize(300, 100)
    authenticator.setWindowTitle('Examiner')

    examiner = Examiner()
    examiner.resize(300, 100)
    examiner.setWindowTitle('Examiner')

    sys.exit(app.exec())