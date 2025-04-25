import os
import re
import subprocess
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from pages.shared_components import ConsoleOutput, AccountSelectionDialog, PASSWORDS

class DownloadThread(QThread):
    """Thread for downloading wallpapers without freezing the UI"""
    update_signal = pyqtSignal(str)
    
    def __init__(self, wallpaper_id, save_location, username):
        super().__init__()
        self.wallpaper_id = wallpaper_id
        self.save_location = save_location
        self.username = username
    
    def extract_id_from_link(self, link):
        """Extract the wallpaper ID from a workshop link"""
        match = re.search(r'\b\d{8,10}\b', link)
        if match:
            return match.group(0)
        return None
    
    def run(self):
        """Run the download process"""
        save_dir = os.path.join(self.save_location, "projects", "myprojects", self.wallpaper_id)
        
        self.update_signal.emit(f"\n--- Downloading {self.wallpaper_id} ---")
        self.update_signal.emit(f"Username: {self.username}")
        self.update_signal.emit(f"Save to: {save_dir}\n")
        
        dir_option = f"-dir \"{save_dir}\""
        command = f"DepotdownloaderMod\\DepotDownloadermod.exe -app 431960 -pubfile {self.wallpaper_id} -verify-all -username {self.username} -password {PASSWORDS[self.username]} {dir_option}"
        
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            for line in process.stdout:
                self.update_signal.emit(line.strip())
            process.wait()
            self.update_signal.emit(f"\n--- Download finished for {self.wallpaper_id} ---\n")
        except Exception as e:
            self.update_signal.emit(f"Error executing command: {e}")

class DownloaderPage(QWidget):
    """Page for downloading wallpapers from Steam Workshop"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the downloader page UI"""
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        self.create_header()
        self.create_links_input()
        self.create_account_selector()
        self.create_download_button()
        self.create_console_output()
        
    def create_header(self):
        """Create the header section of the page"""
        header = QLabel("Download Wallpapers")
        header.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.layout.addWidget(header)
        
        subheader = QLabel("Paste workshop links below, one per line")
        subheader.setFont(QFont("Segoe UI", 10))
        self.layout.addWidget(subheader)
        self.layout.addSpacing(10)
        
    def create_links_input(self):
        """Create text input for workshop links"""
        self.links_edit = QTextEdit()
        self.links_edit.setPlaceholderText("Paste Steam Workshop links here (one per line)")
        self.layout.addWidget(self.links_edit)
        
    def create_account_selector(self):
        """Create account selection area"""
        account_layout = QHBoxLayout()
        
        account_label = QLabel("Select account:")
        account_label.setFixedWidth(100)
        
        self.account_select = QLineEdit()
        self.account_select.setText(self.main_window.config.get("selected_account", "ruiiixx"))
        self.account_select.setReadOnly(True)
        
        account_button = QPushButton("Change")
        account_button.setFixedWidth(100)
        account_button.clicked.connect(self.show_account_selection)
        
        account_layout.addWidget(account_label)
        account_layout.addWidget(self.account_select)
        account_layout.addWidget(account_button)
        
        self.layout.addLayout(account_layout)
        
    def create_download_button(self):
        """Create download button"""
        download_button = QPushButton("Download Wallpapers")
        download_button.setMinimumHeight(40)
        download_button.clicked.connect(self.download_wallpapers)
        self.layout.addWidget(download_button)
        self.layout.addSpacing(10)
        
    def create_console_output(self):
        """Create console output area"""
        console_label = QLabel("Console Output")
        console_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.layout.addWidget(console_label)
        
        self.console = ConsoleOutput()
        self.console.setMinimumHeight(200)
        self.layout.addWidget(self.console)
        
    def show_account_selection(self):
        """Show the account selection dialog"""
        dialog = AccountSelectionDialog(self)
        if dialog.exec_():
            selected_account = dialog.get_selected_account()
            self.account_select.setText(selected_account)
            self.main_window.config["selected_account"] = selected_account
            self.main_window.save_config()
    
    def extract_id_from_link(self, link):
        """Extract the wallpaper ID from a workshop link"""
        match = re.search(r'\b\d{8,10}\b', link)
        if match:
            return match.group(0)
        return None
    
    def download_wallpapers(self):
        """Start the wallpaper download process"""
        save_location = self.main_window.config.get("save_location", "")
        
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
                
            wallpaper_id = self.extract_id_from_link(link)
            if wallpaper_id:
                self.download_thread = DownloadThread(wallpaper_id, save_location, username)
                self.download_thread.update_signal.connect(self.console.append_text)
                self.download_thread.start()
            else:
                self.console.append_text(f"Invalid link or ID: {link}")
                
    def apply_theme(self, is_dark_theme):
        """Apply theme to the page"""
        self.console.apply_theme(is_dark_theme)