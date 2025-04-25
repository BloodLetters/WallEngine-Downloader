import os
import json
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QGridLayout, QFrame, QScrollArea, QSizePolicy
)
from PyQt5.QtGui import QPixmap, QMovie, QFont
from PyQt5.QtCore import Qt, QEvent, QSize

class MyWallpaperPage(QWidget):
    MIN_CARD_WIDTH = 240
    MIN_CARD_HEIGHT = 290
    MIN_PREVIEW_WIDTH = 200
    MIN_PREVIEW_HEIGHT = 140
    CARD_SPACING_H = 18
    CARD_SPACING_V = 24
    CARD_MARGIN = 12

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.gif_movies = []
        self.init_ui()
    
    def init_ui(self):
        self.setStyleSheet("""
            QLabel#wptitle {
                color: #88C0D0;
                font-size: 26px;
                font-weight: bold;
                margin-bottom: 12px;
                letter-spacing: 0.5px;
            }
            QLabel#statuslbl {
                color: #888;
                font-size: 16px;
                padding: 22px 0;
            }
            QScrollArea {
                border: none;
                background: transparent;
            }
        """)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(24, 24, 24, 24)
        self.main_layout.setSpacing(10)
        
        self.title_label = QLabel("My Wallpaper")
        self.title_label.setObjectName("wptitle")
        self.main_layout.addWidget(self.title_label)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameStyle(QFrame.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.main_layout.addWidget(self.scroll_area, stretch=1)
        
        self.grid_container = QWidget()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setHorizontalSpacing(self.CARD_SPACING_H)
        self.grid_layout.setVerticalSpacing(self.CARD_SPACING_V)
        self.scroll_area.setWidget(self.grid_container)
        
        self.status_label = QLabel("")
        self.status_label.setObjectName("statuslbl")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.hide()
        self.main_layout.addWidget(self.status_label, alignment=Qt.AlignCenter)

        self.installEventFilter(self)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.populate_wallpapers()

    def showEvent(self, event):
        super().showEvent(event)
        self.populate_wallpapers()

    def eventFilter(self, obj, event):
        if obj is self and event.type() == QEvent.Resize:
            self.populate_wallpapers()
        return super().eventFilter(obj, event)

    def clear_grid(self):
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.gif_movies = []
        self.status_label.hide()

    def get_max_col(self):
        available_width = self.scroll_area.viewport().width()
        card_width = self.MIN_CARD_WIDTH + self.CARD_SPACING_H
        max_col = max(1, available_width // card_width)
        return max_col

    def get_card_size(self):
        max_col = self.get_max_col()
        if max_col < 1:
            max_col = 1
        available_width = self.scroll_area.viewport().width()
        spacing_total = self.CARD_SPACING_H * (max_col - 1)
        card_width = max(self.MIN_CARD_WIDTH, int((available_width - spacing_total) / max_col))
        preview_width = max(self.MIN_PREVIEW_WIDTH, card_width - 40)
        preview_height = int(preview_width * 0.7)
        card_height = max(self.MIN_CARD_HEIGHT, preview_height + 60)
        return card_width, card_height, preview_width, preview_height

    def populate_wallpapers(self):
        self.clear_grid()
        save_location = self.main_window.config.get("save_location", "")
        myprojects_dir = os.path.join(save_location, "projects", "myprojects")
        found_any = False
        row, col = 0, 0

        max_col = self.get_max_col()
        card_width, card_height, preview_width, preview_height = self.get_card_size()

        if not os.path.exists(myprojects_dir) or not os.listdir(myprojects_dir):
            self.status_label.setText("Tidak ada wallpaper tersimpan.")
            self.status_label.show()
            return

        for folder in sorted(os.listdir(myprojects_dir)):
            folder_path = os.path.join(myprojects_dir, folder)
            if not os.path.isdir(folder_path):
                continue
            project_json_path = os.path.join(folder_path, "project.json")
            if not os.path.isfile(project_json_path):
                continue
            try:
                with open(project_json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                preview = data.get("preview")
                title = data.get("title", "No Title")
                preview_path = os.path.join(folder_path, preview)
            except Exception:
                continue

            found_any = True
            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    background: #262b36;
                    border-radius: 13px;
                    border: 2px solid #384157;
                    padding: 8px;
                }
                QFrame:hover {
                    border: 2px solid #88C0D0;
                    background: #293040;
                }
            """)
            card.setFixedSize(card_width, card_height)
            vbox = QVBoxLayout(card)
            vbox.setContentsMargins(10, 14, 10, 10)
            vbox.setSpacing(8)

            preview_label = QLabel()
            preview_label.setFixedSize(preview_width, preview_height)
            preview_label.setAlignment(Qt.AlignCenter)
            preview_label.setStyleSheet("""
                background: #23272E;
                border-radius: 8px;
                border: 1px solid #31384a;
            """)

            if preview and preview.lower().endswith((".gif", ".mp4", ".webm")):
                if preview.lower().endswith(".gif") and os.path.isfile(preview_path):
                    anim = QMovie(preview_path)
                    self.gif_movies.append(anim)
                    preview_label.setMovie(anim)
                    anim.start()
                else:
                    preview_label.setText("(Preview video)\nTidak didukung preview langsung.")
                    preview_label.setStyleSheet(preview_label.styleSheet() + "color:#BBB; font-size:13px;")
            elif os.path.isfile(preview_path):
                pix = QPixmap(preview_path)
                preview_label.setPixmap(
                    pix.scaled(preview_width, preview_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                )
            else:
                preview_label.setText("No Preview")
                preview_label.setStyleSheet(preview_label.styleSheet() + "color:#BBB; font-size:13px;")

            vbox.addWidget(preview_label, alignment=Qt.AlignCenter)

            title_lbl = QLabel(title)
            title_lbl.setFixedWidth(preview_width)
            title_lbl.setStyleSheet("""
                color: #ECEFF4;
                font-size: 16px;
                font-weight: bold;
                background: transparent;
                border-radius: 2px;
                padding: 4px 0 0 0;
            """)
            title_lbl.setAlignment(Qt.AlignCenter)
            title_lbl.setWordWrap(False)
            title_lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            vbox.addWidget(title_lbl, alignment=Qt.AlignCenter)

            self.grid_layout.addWidget(card, row, col)
            col += 1
            if col >= max_col:
                col = 0
                row += 1

        if not found_any:
            self.status_label.setText("Tidak ada wallpaper tersimpan.")
            self.status_label.show()