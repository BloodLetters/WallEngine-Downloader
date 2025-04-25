import webbrowser
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal
from pages.shared_components import SidebarButton

class Sidebar(QWidget):
    """Sidebar for navigation between application pages"""
    # Signal to notify when page should be changed
    page_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the sidebar UI"""
        self.setFixedWidth(220)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # Create app title section
        self.create_app_title()
        
        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(separator)
        
        self.layout.addSpacing(20)
        
        # Create navigation buttons
        self.create_nav_buttons()
        
        self.layout.addStretch()
        
        # Create footer
        self.create_footer()
        
    def create_app_title(self):
        """Create the app title section at the top of the sidebar"""
        app_title = QWidget()
        app_title_layout = QHBoxLayout(app_title)
        app_title_layout.setContentsMargins(20, 20, 20, 20)
        
        # Add logo
        logo_label = QLabel()
        logo_label.setPixmap(QPixmap("Assets/icon.png").scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        # Add title text
        title_label = QLabel("Wallpaper Engine")
        title_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        
        app_title_layout.addWidget(logo_label)
        app_title_layout.addWidget(title_label)
        app_title_layout.addStretch()
        
        self.layout.addWidget(app_title)
        
    def create_nav_buttons(self):
        """Create navigation buttons for sidebar"""
        self.downloader_btn = SidebarButton("Downloader")
        self.workshop_btn = SidebarButton("Steam Workshop")
        self.config_btn = SidebarButton("Config")
        
        # Connect button signals
        self.downloader_btn.clicked.connect(lambda: self.page_changed.emit("downloader"))
        self.workshop_btn.clicked.connect(self.open_steam_workshop)
        self.config_btn.clicked.connect(lambda: self.page_changed.emit("config"))
        
        # Add buttons to layout
        self.layout.addWidget(self.downloader_btn)
        self.layout.addWidget(self.workshop_btn)
        self.layout.addWidget(self.config_btn)
        
    def create_footer(self):
        """Create footer section at the bottom of the sidebar"""
        footer = QWidget()
        footer_layout = QVBoxLayout(footer)
        
        # Version info label
        version_label = QLabel(f"Version {self.main_window.APP_VERSION}")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setFont(QFont("Segoe UI", 8))
        
        # Made with love label
        made_with_love = QLabel("Made with ❤️")
        made_with_love.setAlignment(Qt.AlignCenter)
        made_with_love.setFont(QFont("Segoe UI", 8))
        
        footer_layout.addWidget(version_label)
        footer_layout.addWidget(made_with_love)
        
        self.layout.addWidget(footer)
        self.layout.addSpacing(10)
        
    def set_active_button(self, button_name):
        """Set the active button in the sidebar"""
        self.downloader_btn.setChecked(button_name == "downloader")
        self.workshop_btn.setChecked(button_name == "workshop")
        self.config_btn.setChecked(button_name == "config")
        
    def open_steam_workshop(self):
        """Open Steam Workshop in the default browser"""
        webbrowser.open("http://steamcommunity.com/workshop/browse/?appid=431960")
        self.set_active_button("workshop")
        
    def apply_theme(self, is_dark_theme):
        """Apply theme to sidebar"""
        if is_dark_theme:
            self.setStyleSheet("""
                background-color: #2E3440;
                border-right: 1px solid #434C5E;
            """)
            
            button_style = """
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
            """
        else:
            self.setStyleSheet("""
                background-color: #EEEEEE;
                border-right: 1px solid #DDDDDD;
            """)
            
            button_style = """
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
            """
        
        # Apply style to all buttons
        self.downloader_btn.setStyleSheet(button_style)
        self.workshop_btn.setStyleSheet(button_style)
        self.config_btn.setStyleSheet(button_style)