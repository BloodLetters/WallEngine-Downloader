import base64
from PyQt5.QtWidgets import QTextEdit, QPushButton, QDialog, QVBoxLayout, QListWidget, QListWidgetItem
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5 import QtGui

# Account data with base64 encoded passwords
ACCOUNTS = {
    'ruiiixx': 'UzY3R0JUQjgzRDNZ',
    'premexilmenledgconis': 'M3BYYkhaSmxEYg==',
    'vAbuDy': 'Qm9vbHE4dmlw',
    'adgjl1182': 'UUVUVU85OTk5OQ==',
    'gobjj16182': 'enVvYmlhbzgyMjI=',
    '787109690': 'SHVjVXhZTVFpZzE1'
}

# Decode passwords for use
PASSWORDS = {user: base64.b64decode(pw).decode('utf-8') for user, pw in ACCOUNTS.items()}

class ConsoleOutput(QTextEdit):
    """Custom styled console output widget"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        
    def append_text(self, text):
        """Append text to console and scroll to bottom"""
        self.append(text)
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
        
    def apply_theme(self, is_dark_theme):
        """Apply theme-specific styling to console"""
        if is_dark_theme:
            self.setStyleSheet("""
                QTextEdit {
                    background-color: #232731;
                    color: #ECEFF4;
                    border: none;
                    font-family: 'Consolas', monospace;
                    padding: 10px;
                    border-radius: 8px;
                }
            """)
        else:
            self.setStyleSheet("""
                QTextEdit {
                    background-color: #F8F8F8;
                    color: #333333;
                    border: 1px solid #DDDDDD;
                    font-family: 'Consolas', monospace;
                    padding: 10px;
                    border-radius: 8px;
                }
            """)

class SidebarButton(QPushButton):
    """Custom styled button for sidebar"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setMinimumHeight(50)
        self.setFont(QFont("Segoe UI", 10))
        self.setCursor(Qt.PointingHandCursor)

class AccountSelectionDialog(QDialog):
    """Dialog for selecting an account from the available options"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Account")
        self.setWindowIcon(QtGui.QIcon("Assets/icon.png"))
        self.setMinimumWidth(300)
        self.layout = QVBoxLayout()

        self.account_list = QListWidget()
        for account in ACCOUNTS.keys():
            item = QListWidgetItem(account)
            self.account_list.addItem(item)
        
        self.layout.addWidget(self.account_list)
        self.select_button = QPushButton("Select")
        self.select_button.clicked.connect(self.accept)
        self.layout.addWidget(self.select_button)
        
        self.setLayout(self.layout)
    
    def get_selected_account(self):
        """Return the selected account username"""
        if self.account_list.currentItem():
            return self.account_list.currentItem().text()
        return list(ACCOUNTS.keys())[0]