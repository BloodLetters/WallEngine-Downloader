import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QComboBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class ConfigPage(QWidget):
    """Configuration page for the application"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the configuration page UI"""
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        # Create header
        self.create_header()
        
        # Create save location section
        self.create_save_location_section()
        
        # Create theme selection section
        self.create_theme_section()
        
        # Create save button
        self.create_save_button()
        
        # Create status area
        self.create_status_area()
        
        # Add stretch to push everything to the top
        self.layout.addStretch()
        
        # Load existing configuration
        self.load_config_values()
        
    def create_header(self):
        """Create the header section of the page"""
        header = QLabel("Configuration")
        header.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.layout.addWidget(header)
        self.layout.addSpacing(20)
        
    def create_save_location_section(self):
        """Create the save location configuration section"""
        save_location_label = QLabel("Wallpaper Engine Location")
        save_location_label.setFont(QFont("Segoe UI", 12))
        self.layout.addWidget(save_location_label)
        
        save_location_sublabel = QLabel("Select the path to your Wallpaper Engine folder. It must contain projects/myprojects directory.")
        self.layout.addWidget(save_location_sublabel)
        self.layout.addSpacing(10)
        
        save_location_layout = QHBoxLayout()
        
        self.save_location_edit = QLineEdit()
        self.save_location_edit.setPlaceholderText("Path to Wallpaper Engine folder")
        
        browse_button = QPushButton("Browse")
        browse_button.setFixedWidth(100)
        browse_button.clicked.connect(self.browse_save_location)
        
        save_location_layout.addWidget(self.save_location_edit)
        save_location_layout.addWidget(browse_button)
        
        self.layout.addLayout(save_location_layout)
        
    def create_theme_section(self):
        """Create theme selection section"""
        self.layout.addSpacing(20)
        
        theme_label = QLabel("Theme")
        theme_label.setFont(QFont("Segoe UI", 12))
        self.layout.addWidget(theme_label)
        
        theme_layout = QHBoxLayout()
        
        theme_select_label = QLabel("Select theme:")
        theme_select_label.setFixedWidth(100)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["System", "Dark", "Light"])
        
        theme_layout.addWidget(theme_select_label)
        theme_layout.addWidget(self.theme_combo)
        
        self.layout.addLayout(theme_layout)
        
    def create_save_button(self):
        """Create save configuration button"""
        save_button = QPushButton("Save Configuration")
        save_button.clicked.connect(self.save_config)
        self.layout.addWidget(save_button)
        
    def create_status_area(self):
        """Create status message area"""
        self.layout.addSpacing(20)
        self.directory_status = QLabel("")
        self.layout.addWidget(self.directory_status)

    def load_config_values(self):
        """Load configuration values from the main application config"""
        # Set save location
        self.save_location_edit.setText(self.main_window.config.get("save_location", ""))
        
        # Set theme selection
        theme_mapping = {"system": 0, "dark": 1, "light": 2}
        self.theme_combo.setCurrentIndex(theme_mapping.get(self.main_window.config.get("theme", "system"), 0))
    
    def browse_save_location(self):
        """Open file dialog to browse for Wallpaper Engine directory"""
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)
        if dialog.exec_():
            selected_dir = dialog.selectedFiles()[0]
            self.save_location_edit.setText(selected_dir)
            self.validate_save_location()
    
    def validate_save_location(self):
        """Validate the selected save location directory"""
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
    
    def save_config(self):
        """Save configuration values to the main config"""
        location = self.save_location_edit.text()
        is_valid = self.validate_save_location()
        
        # Update config values
        self.main_window.config["save_location"] = location
        
        # Get theme from combo box
        theme_index = self.theme_combo.currentIndex()
        theme_values = ["system", "dark", "light"]
        self.main_window.config["theme"] = theme_values[theme_index]
        
        # Apply theme to application
        self.main_window.apply_theme(self.main_window.config["theme"])
        
        # Save to file
        self.main_window.save_config()
        
        if is_valid:
            self.directory_status.setText("Configuration saved successfully")
    
    def apply_theme(self, is_dark_theme):
        """Apply theme to the config page"""
        # No specific styling needed for this page beyond what's in the main app
        pass