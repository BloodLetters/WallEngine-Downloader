import sys
import os
import re
import subprocess
import base64
import threading
import webbrowser
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QTextEdit, QLineEdit, QFileDialog, 
                            QTabWidget, QFrame, QStackedWidget, QSplitter, QMessageBox,
                            QComboBox, QDialog, QListWidget, QListWidgetItem)
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette, QPixmap
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QThread

APP_VERSION = "1.0.0"
accounts = {
    'ruiiixx': 'UzY3R0JUQjgzRDNZ',
    'premexilmenledgconis': 'M3BYYkhaSmxEYg==',
    'vAbuDy': 'Qm9vbHE4dmlw',
    'adgjl1182': 'UUVUVU85OTk5OQ==',
    'gobjj16182': 'enVvYmlhbzgyMjI=',
    '787109690': 'SHVjVXhZTVFpZzE1'
}
passwords = {user: base64.b64decode(pw).decode('utf-8') for user, pw in accounts.items()}

# Default configuration
DEFAULT_CONFIG = {
    "save_location": "",
    "selected_account": list(accounts.keys())[0],
    "theme": "dark"  # Can be "dark", "light", or "system"
}

class AccountSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Account")
        self.setMinimumWidth(300)
        self.layout = QVBoxLayout()

        self.account_list = QListWidget()
        for account in accounts.keys():
            item = QListWidgetItem(account)
            self.account_list.addItem(item)
        
        self.layout.addWidget(self.account_list)
        
        self.select_button = QPushButton("Select")
        self.select_button.clicked.connect(self.accept)
        self.layout.addWidget(self.select_button)
        
        self.setLayout(self.layout)
    
    def get_selected_account(self):
        if self.account_list.currentItem():
            return self.account_list.currentItem().text()
        return list(accounts.keys())[0]

class ConsoleOutput(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setStyleSheet("""
            QTextEdit {
                background-color: #1A1E27;
                color: #CDD6F4;
                border: none;
                font-family: 'Consolas', monospace;
                padding: 10px;
                border-radius: 8px;
            }
        """)
        
    def append_text(self, text):
        self.append(text)
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())


class DownloadThread(QThread):
    update_signal = pyqtSignal(str)
    
    def __init__(self, pubfileid, save_location, username):
        super().__init__()
        self.pubfileid = pubfileid
        self.save_location = save_location
        self.username = username
    
    def extract_pubid_from_link(self, link):
        match = re.search(r'\b\d{8,10}\b', link)
        if match:
            return match.group(0)
        return None
    
    def run(self):
        save_dir = os.path.join(self.save_location, "projects", "myprojects", self.pubfileid)
        
        self.update_signal.emit(f"\n--- Downloading {self.pubfileid} ---")
        self.update_signal.emit(f"Username: {self.username}")
        self.update_signal.emit(f"Save to: {save_dir}\n")
        
        dir_option = f"-dir \"{save_dir}\""
        command = f"DepotdownloaderMod\\DepotDownloadermod.exe -app 431960 -pubfile {self.pubfileid} -verify-all -username {self.username} -password {passwords[self.username]} {dir_option}"
        
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            
            for line in process.stdout:
                self.update_signal.emit(line.strip())
            
            process.wait()
            self.update_signal.emit(f"\n--- Download finished for {self.pubfileid} ---\n")
        except Exception as e:
            self.update_signal.emit(f"Error executing command: {e}")


class SidebarButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setMinimumHeight(50)
        self.setFont(QFont("Segoe UI", 10))
        self.setCursor(Qt.PointingHandCursor)

class WallpaperDownloaderGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = self.load_config()
        self.init_ui()
        self.apply_theme(self.config.get("theme", "system"))
        
    def init_ui(self):
        self.setWindowTitle("Wallpaper Engine Downloader")
        self.setMinimumSize(1000, 700)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        sidebar = QWidget()
        sidebar.setFixedWidth(220)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        app_title = QWidget()
        app_title_layout = QHBoxLayout(app_title)
        app_title_layout.setContentsMargins(20, 20, 20, 20)
        
        logo_label = QLabel()
        logo_label.setPixmap(QPixmap("Assets/icon.png").scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        title_label = QLabel("Wallpaper Engine")
        title_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        
        app_title_layout.addWidget(logo_label)
        app_title_layout.addWidget(title_label)
        app_title_layout.addStretch()
        
        sidebar_layout.addWidget(app_title)
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        sidebar_layout.addWidget(separator)
        
        sidebar_layout.addSpacing(20)
        
        self.downloader_btn = SidebarButton("Downloader")
        self.downloader_btn.setChecked(True)
        self.workshop_btn = SidebarButton("Steam Workshop")
        self.config_btn = SidebarButton("Config")
        
        sidebar_layout.addWidget(self.downloader_btn)
        sidebar_layout.addWidget(self.workshop_btn)
        sidebar_layout.addWidget(self.config_btn)
        sidebar_layout.addStretch()
        
        footer = QWidget()
        footer_layout = QVBoxLayout(footer)
        
        version_label = QLabel(f"Version {APP_VERSION}")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setFont(QFont("Segoe UI", 8))
        
        made_with_love = QLabel("Made with ❤️")
        made_with_love.setAlignment(Qt.AlignCenter)
        made_with_love.setFont(QFont("Segoe UI", 8))
        
        footer_layout.addWidget(version_label)
        footer_layout.addWidget(made_with_love)
        
        sidebar_layout.addWidget(footer)
        sidebar_layout.addSpacing(10)
        
        main_layout.addWidget(sidebar)
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)
        
        self.create_downloader_page()
        self.create_config_page()
        
        self.downloader_btn.clicked.connect(self.show_downloader_page)
        self.workshop_btn.clicked.connect(self.open_steam_workshop)
        self.config_btn.clicked.connect(self.show_config_page)
        
        self.show_downloader_page()
        self.load_config_to_ui()
        
    def create_downloader_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        
        header = QLabel("Download Wallpapers")
        header.setFont(QFont("Segoe UI", 16, QFont.Bold))
        layout.addWidget(header)
        
        subheader = QLabel("Paste workshop links below, one per line")
        subheader.setFont(QFont("Segoe UI", 10))
        layout.addWidget(subheader)
        layout.addSpacing(10)
        
        self.links_edit = QTextEdit()
        self.links_edit.setPlaceholderText("Paste Steam Workshop links here (one per line)")
        layout.addWidget(self.links_edit)
        
        account_layout = QHBoxLayout()
        account_label = QLabel("Select account:")
        account_label.setFixedWidth(100)
        self.account_select = QLineEdit()
        self.account_select.setText(self.config.get("selected_account", list(accounts.keys())[0]))
        self.account_select.setReadOnly(True)
        account_button = QPushButton("Change")
        account_button.setFixedWidth(100)
        account_button.clicked.connect(self.show_account_selection)
        account_layout.addWidget(account_label)
        account_layout.addWidget(self.account_select)
        account_layout.addWidget(account_button)
        layout.addLayout(account_layout)
        
        download_button = QPushButton("Download Wallpapers")
        download_button.setMinimumHeight(40)
        download_button.clicked.connect(self.download_wallpapers)
        layout.addWidget(download_button)
        layout.addSpacing(10)
        
        console_label = QLabel("Console Output")
        console_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        layout.addWidget(console_label)
        
        self.console = ConsoleOutput()
        self.console.setMinimumHeight(200)
        layout.addWidget(self.console)
        
        self.stacked_widget.addWidget(page)
        
    def create_config_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        
        header = QLabel("Configuration")
        header.setFont(QFont("Segoe UI", 16, QFont.Bold))
        layout.addWidget(header)
        
        layout.addSpacing(20)
        save_location_label = QLabel("Wallpaper Engine Location")
        save_location_label.setFont(QFont("Segoe UI", 12))
        layout.addWidget(save_location_label)
        
        save_location_sublabel = QLabel("Select the path to your Wallpaper Engine folder. It must contain projects/myprojects directory.")
        layout.addWidget(save_location_sublabel)
        layout.addSpacing(10)
        
        save_location_layout = QHBoxLayout()
        self.save_location_edit = QLineEdit()
        self.save_location_edit.setPlaceholderText("Path to Wallpaper Engine folder")
        browse_button = QPushButton("Browse")
        browse_button.setFixedWidth(100)
        browse_button.clicked.connect(self.browse_save_location)
        save_location_layout.addWidget(self.save_location_edit)
        save_location_layout.addWidget(browse_button)
        layout.addLayout(save_location_layout)
        
        layout.addSpacing(20)
        theme_label = QLabel("Theme")
        theme_label.setFont(QFont("Segoe UI", 12))
        layout.addWidget(theme_label)
        
        theme_layout = QHBoxLayout()
        theme_select_label = QLabel("Select theme:")
        theme_select_label.setFixedWidth(100)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["System", "Dark", "Light"])
        theme_layout.addWidget(theme_select_label)
        theme_layout.addWidget(self.theme_combo)
        layout.addLayout(theme_layout)

        theme_mapping = {"system": 0, "dark": 1, "light": 2}
        self.theme_combo.setCurrentIndex(theme_mapping.get(self.config.get("theme", "system"), 0))
        
        save_button = QPushButton("Save Configuration")
        save_button.clicked.connect(self.save_config_from_ui)
        layout.addWidget(save_button)
        
        layout.addSpacing(20)
        self.directory_status = QLabel("")
        layout.addWidget(self.directory_status)
        
        layout.addStretch()
        
        self.stacked_widget.addWidget(page)
        
    def show_downloader_page(self):
        self.stacked_widget.setCurrentIndex(0)
        self.downloader_btn.setChecked(True)
        self.config_btn.setChecked(False)
        
    def open_steam_workshop(self):
        webbrowser.open("http://steamcommunity.com/workshop/browse/?appid=431960")
        self.downloader_btn.setChecked(False)
        self.workshop_btn.setChecked(True)
        self.config_btn.setChecked(False)
        
    def show_config_page(self):
        self.stacked_widget.setCurrentIndex(1)
        self.downloader_btn.setChecked(False)
        self.config_btn.setChecked(True)
        self.validate_save_location()
        
    def load_config(self):
        try:
            if os.path.exists("config.json"):
                with open("config.json", "r") as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
        return DEFAULT_CONFIG.copy()
    
    def save_config(self):
        try:
            with open("config.json", "w") as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def load_config_to_ui(self):
        self.save_location_edit.setText(self.config.get("save_location", ""))
        self.account_select.setText(self.config.get("selected_account", list(accounts.keys())[0]))
        
        theme_mapping = {"system": 0, "dark": 1, "light": 2}
        self.theme_combo.setCurrentIndex(theme_mapping.get(self.config.get("theme", "system"), 0))
    
    def save_config_from_ui(self):
        location = self.save_location_edit.text()
        is_valid = self.validate_save_location()
        
        self.config["save_location"] = location
        self.config["selected_account"] = self.account_select.text()
        
        theme_index = self.theme_combo.currentIndex()
        theme_values = ["system", "dark", "light"]
        self.config["theme"] = theme_values[theme_index]
        
        self.apply_theme(self.config["theme"])
        self.save_config()
        
        if is_valid:
            self.directory_status.setText("Configuration saved successfully")
    
    def browse_save_location(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)
        if dialog.exec_():
            selected_dir = dialog.selectedFiles()[0]
            self.save_location_edit.setText(selected_dir)
            self.validate_save_location()
    
    def validate_save_location(self):
        location = self.save_location_edit.text()
        
        if not location:
            self.directory_status.setText("Please select Wallpaper Engine folder")
            return False
        
        if not os.path.isdir(location):
            self.directory_status.setText("Selected directory does not exist")
            return False
        
        projects_dir = os.path.join(location, "projects")
        if not os.path.isdir(projects_dir):
            self.directory_status.setText("Directory doesn't contain 'projects' folder. Invalid Wallpaper Engine directory.")
            return False
        
        myprojects_dir = os.path.join(projects_dir, "myprojects")
        if not os.path.isdir(myprojects_dir):
            self.directory_status.setText("Missing 'myprojects' directory. Creating it now...")
            try:
                os.makedirs(myprojects_dir, exist_ok=True)
                self.directory_status.setText("Created 'myprojects' directory successfully")
                return True
            except Exception as e:
                self.directory_status.setText(f"Error creating directory: {e}")
                return False
        else:
            self.directory_status.setText("Valid Wallpaper Engine directory detected")
            return True
    
    def show_account_selection(self):
        dialog = AccountSelectionDialog(self)
        if dialog.exec_():
            selected_account = dialog.get_selected_account()
            self.account_select.setText(selected_account)
            self.config["selected_account"] = selected_account
            self.save_config()
    
    def extract_pubid_from_link(self, link):
        match = re.search(r'\b\d{8,10}\b', link)
        if match:
            return match.group(0)
        return None
    
    def download_wallpapers(self):
        save_location = self.save_location_edit.text()
        
        # Validate location before downloading
        if not save_location:
            QMessageBox.warning(self, "Invalid Configuration", "Save location not set. Please configure it in the Config tab.")
            return
        
        if not os.path.isdir(save_location):
            QMessageBox.warning(self, "Invalid Configuration", "Save location directory does not exist.")
            return
        
        projects_dir = os.path.join(save_location, "projects")
        if not os.path.isdir(projects_dir):
            QMessageBox.warning(self, "Invalid Configuration", "Directory doesn't contain 'projects' folder. Invalid Wallpaper Engine directory.")
            return
        
        myprojects_dir = os.path.join(projects_dir, "myprojects")
        if not os.path.isdir(myprojects_dir):
            try:
                os.makedirs(myprojects_dir, exist_ok=True)
                self.console.append_text("Created 'myprojects' directory successfully")
            except Exception as e:
                QMessageBox.warning(self, "Directory Error", f"Error creating 'myprojects' directory: {e}")
                return
        
        username = self.account_select.text()
        links_text = self.links_edit.toPlainText().strip()
        
        if not links_text:
            QMessageBox.warning(self, "No Links", "No workshop links provided.")
            return
        
        links = links_text.split('\n')
        self.console.append_text(f"Processing {len(links)} link(s)...")
        
        for link in links:
            link = link.strip()
            if not link:
                continue
                
            pubid = self.extract_pubid_from_link(link)
            if pubid:
                self.download_thread = DownloadThread(pubid, save_location, username)
                self.download_thread.update_signal.connect(self.console.append_text)
                self.download_thread.start()
            else:
                self.console.append_text(f"Invalid link or ID: {link}")
    
    def apply_theme(self, theme_name):
        """Apply the selected theme to the application"""
        
        use_dark_theme = True
        if theme_name == "system":
            app = QApplication.instance()
            palette = app.palette()
            bg_color = palette.color(QPalette.Window)
            use_dark_theme = bg_color.lightness() < 128
        elif theme_name == "dark":
            use_dark_theme = True
        elif theme_name == "light":
            use_dark_theme = False
        
        if use_dark_theme:
            self.setStyleSheet("""
                QMainWindow, QWidget {
                    background-color: #2E3440;
                    color: #ECEFF4;
                }
                QLabel {
                    color: #ECEFF4;
                }
                QLineEdit, QTextEdit, QComboBox {
                    background-color: #3B4252;
                    color: #ECEFF4;
                    border: none;
                    padding: 8px;
                    border-radius: 4px;
                }
                QPushButton {
                    background-color: #5E81AC;
                    color: #ECEFF4;
                    border: none;
                    padding: 8px 15px;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #81A1C1;
                }
                QPushButton:pressed {
                    background-color: #88C0D0;
                }
                QComboBox {
                    background-color: #3B4252;
                    selection-background-color: #5E81AC;
                }
                QComboBox QAbstractItemView {
                    background-color: #3B4252;
                    selection-background-color: #5E81AC;
                    color: #ECEFF4;
                }
            """)
            
            sidebar_style = """
                background-color: #2E3440;
                border-right: 1px solid #434C5E;
            """
            
            self.downloader_btn.setStyleSheet("""
                QPushButton {
                    border: none;
                    text-align: left;
                    padding-left: 20px;
                    color: #ECEFF4;
                    background-color: transparent;
                    border-radius: 0px;
                }
                QPushButton:hover {
                    background-color: #3B4252;
                }
                QPushButton:checked {
                    background-color: #3B4252;
                    border-left: 3px solid #88C0D0;
                }
            """)
            self.workshop_btn.setStyleSheet(self.downloader_btn.styleSheet())
            self.config_btn.setStyleSheet(self.downloader_btn.styleSheet())
            
            self.console.setStyleSheet("""
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
                QMainWindow, QWidget {
                    background-color: #F5F5F5;
                    color: #333333;
                }
                QLabel {
                    color: #333333;
                }
                QLineEdit, QTextEdit, QComboBox {
                    background-color: #FFFFFF;
                    color: #333333;
                    border: 1px solid #DDDDDD;
                    padding: 8px;
                    border-radius: 4px;
                }
                QPushButton {
                    background-color: #81A1C1;
                    color: #FFFFFF;
                    border: none;
                    padding: 8px 15px;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #5E81AC;
                }
                QPushButton:pressed {
                    background-color: #4C566A;
                }
                QComboBox {
                    background-color: #FFFFFF;
                    selection-background-color: #81A1C1;
                }
                QComboBox QAbstractItemView {
                    background-color: #FFFFFF;
                    selection-background-color: #81A1C1;
                    color: #333333;
                }
            """)

            sidebar_style = """
                background-color: #EEEEEE;
                border-right: 1px solid #DDDDDD;
            """
            
            self.downloader_btn.setStyleSheet("""
                QPushButton {
                    border: none;
                    text-align: left;
                    padding-left: 20px;
                    color: #333333;
                    background-color: transparent;
                    border-radius: 0px;
                }
                QPushButton:hover {
                    background-color: #E0E0E0;
                }
                QPushButton:checked {
                    background-color: #E0E0E0;
                    border-left: 3px solid #81A1C1;
                }
            """)
            self.workshop_btn.setStyleSheet(self.downloader_btn.styleSheet())
            self.config_btn.setStyleSheet(self.downloader_btn.styleSheet())
            
            self.console.setStyleSheet("""
                QTextEdit {
                    background-color: #F8F8F8;
                    color: #333333;
                    border: 1px solid #DDDDDD;
                    font-family: 'Consolas', monospace;
                    padding: 10px;
                    border-radius: 8px;
                }
            """)
        
        for child in self.centralWidget().children():
            if isinstance(child, QWidget) and child.width() == 220:
                child.setStyleSheet(sidebar_style)
                break


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WallpaperDownloaderGUI()
    window.show()
    sys.exit(app.exec_())