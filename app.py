import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QStackedWidget
from PyQt5.QtGui import QFont, QPalette, QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import QtGui

# Import pages
from pages.downloader import DownloaderPage
from pages.config import ConfigPage
from pages.sidebar import Sidebar
from pages.mywallpaper import MyWallpaperPage

APP_VERSION = "1.0.8"

DEFAULT_CONFIG = {
    "save_location": "",
    "selected_account": "ruiiixx",  # Default acc
    "theme": "dark"  # "dark", "light", or "system"
}

class WallpaperEngineApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = self.load_config()
        self.init_ui()
        self.apply_theme(self.config.get("theme", "system"))
        
    def init_ui(self):
        self.setWindowTitle("WallEngine")
        self.setWindowIcon(QtGui.QIcon("Assets/icon.png"))
        self.setMinimumSize(1000, 700)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create stacked widget for pages
        self.stacked_widget = QStackedWidget()
        
        # Create sidebar
        self.APP_VERSION = APP_VERSION
        self.sidebar = Sidebar(self)
        
        self.downloader_page = DownloaderPage(self)
        self.wallpaper_page = MyWallpaperPage(self)  # <--- Tambahkan ini
        self.config_page = ConfigPage(self)
        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.downloader_page)
        self.stacked_widget.addWidget(self.wallpaper_page)  # <--- Tambahkan ini
        self.stacked_widget.addWidget(self.config_page)

        # Create pages
        self.downloader_page = DownloaderPage(self)
        self.config_page = ConfigPage(self)
        
        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.downloader_page)
        self.stacked_widget.addWidget(self.config_page)
        
        # Add widgets to main layout
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stacked_widget)
        
        # Connect signals
        self.sidebar.page_changed.connect(self.change_page)
        
        # Show downloader page by default
        self.show_downloader_page()
        
    def show_downloader_page(self):
        self.stacked_widget.setCurrentWidget(self.downloader_page)
        self.sidebar.set_active_button("downloader")
        
    def show_config_page(self):
        self.stacked_widget.setCurrentWidget(self.config_page)
        self.sidebar.set_active_button("config")
        self.config_page.validate_save_location()
        
    def change_page(self, page_name):
        if page_name == "downloader":
            self.show_downloader_page()
        elif page_name == "config":
            self.show_config_page()
        elif page_name == "mywallpaper":  # <--- Tambahkan ini
            self.show_wallpaper_page()
        
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
    
    def show_wallpaper_page(self):
        self.stacked_widget.setCurrentWidget(self.wallpaper_page)
        self.sidebar.set_active_button("mywallpaper")

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
        
        # Apply theme to pages
        self.downloader_page.apply_theme(use_dark_theme)
        self.config_page.apply_theme(use_dark_theme)
        self.sidebar.apply_theme(use_dark_theme)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WallpaperEngineApp()
    window.show()
    sys.exit(app.exec_())