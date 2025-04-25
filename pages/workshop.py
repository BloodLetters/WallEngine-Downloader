import webbrowser
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QListWidget, QListWidgetItem
from PyQt5.QtGui import QFont, QDesktopServices
from PyQt5.QtCore import Qt, QUrl

class WorkshopPage(QWidget):
    """Page for browsing Steam Workshop"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the workshop page UI"""
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        self.create_header()
        self.create_browser_button()
        self.create_featured_section()
        self.layout.addStretch()
        
    def create_header(self):
        """Create the header section"""
        header = QLabel("Steam Workshop")
        header.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.layout.addWidget(header)
        
        subheader = QLabel("Browse and find wallpapers to download")
        subheader.setFont(QFont("Segoe UI", 10))
        self.layout.addWidget(subheader)
        self.layout.addSpacing(20)
        
    def create_browser_button(self):
        """Create button to open Steam Workshop in browser"""
        browser_button = QPushButton("Open Steam Workshop in Browser")
        browser_button.setMinimumHeight(40)
        browser_button.clicked.connect(self.open_workshop)
        self.layout.addWidget(browser_button)
        self.layout.addSpacing(20)
        
    def create_featured_section(self):
        """Create section for featured workshop items (placeholder)"""
        featured_label = QLabel("Featured Items")
        featured_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.layout.addWidget(featured_label)
        
        featured_info = QLabel("This section would display featured items from the workshop.")
        self.layout.addWidget(featured_info)
        
        
        self.featured_list = QListWidget()
        self.featured_list.setMaximumHeight(200)
        self.layout.addWidget(self.featured_list)
        
        
        placeholder_items = [
            "Featured Wallpaper 1",
            "Featured Wallpaper 2",
            "Featured Wallpaper 3"
        ]
        
        for item_text in placeholder_items:
            item = QListWidgetItem(item_text)
            self.featured_list.addItem(item)
            
    def open_workshop(self):
        """Open Steam Workshop in default browser"""
        workshop_url = "http://steamcommunity.com/workshop/browse/?appid=431960"
        QDesktopServices.openUrl(QUrl(workshop_url))
        
    def apply_theme(self, is_dark_theme):
        """Apply theme to workshop page"""
        
        pass