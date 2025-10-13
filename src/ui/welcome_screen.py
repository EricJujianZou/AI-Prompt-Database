"""
Welcome Screen for First-Time Users

This module provides a tutorial/onboarding dialog that appears on the user's
first launch of PromptAssist, explaining the system tray behavior and 
keyboard shortcuts.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, 
    QCheckBox, QHBoxLayout
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QFont


class WelcomeScreen(QDialog):
    """
    A dialog window shown to first-time users explaining how to use PromptAssist.
    
    Provides information about:
    - System tray icon location
    - Keyboard shortcuts (Ctrl+Space, Ctrl+Shift+Space)
    - How to access the dashboard
    
    Signals:
        dont_show_again: Emitted with True if user checks "Don't show again"
    """
    
    dont_show_again = Signal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the welcome screen UI components."""
        self.setWindowTitle("Welcome to PromptAssist!")
        self.setModal(True)  # Block interaction with main window
        self.setMinimumSize(500, 400)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # --- Welcome Header ---
        header = QLabel("🎉 Welcome to PromptAssist!")
        header_font = QFont()
        header_font.setPointSize(16)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # --- Intro Text ---
        intro_text = QLabel(
            "PromptAssist is now running in your system tray! "
            "Here's what you need to know to get started:"
        )
        intro_text.setWordWrap(True)
        intro_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(intro_text)
        
        layout.addSpacing(10)
        
        # --- Tutorial Content ---
        tutorial_content = [
            ("📍 System Tray", 
             "Look for the PromptAssist icon in your system tray (bottom-right corner "
             "of your screen, near the clock). The app runs quietly in the background."),
            
            
            ("🎛️ Dashboard Access", 
             "Go to your system tray, and right-click the \"E\" icon and select 'Show Dashboard' to manage "
             "your snippets, view history, and customize settings."),
            
            ("📜 History Features",
             "In the History tab, you can:\n"
             "• <b>Double-click</b> any entry to view full details\n"
             "• <b>Right-click</b> entries to copy, save as snippet, or delete\n"
             "• Use the toolbar buttons for quick actions"),
        ]
        
        for title, description in tutorial_content:
            # Section title
            title_label = QLabel(title)
            title_font = QFont()
            title_font.setPointSize(11)
            title_font.setBold(True)
            title_label.setFont(title_font)
            layout.addWidget(title_label)
            
            # Section description
            desc_label = QLabel(description)
            desc_label.setWordWrap(True)
            desc_label.setTextFormat(Qt.TextFormat.RichText)  # Allow HTML formatting
            desc_label.setStyleSheet("padding-left: 20px; color: #666;")
            layout.addWidget(desc_label)
            
            layout.addSpacing(5)
        
        layout.addStretch()  # Push everything up
        
        # --- Bottom Section: Checkbox and Button ---
        bottom_layout = QHBoxLayout()
        
        self.dont_show_checkbox = QCheckBox("Don't show this again")
        bottom_layout.addWidget(self.dont_show_checkbox)
        
        bottom_layout.addStretch()
        
        self.got_it_button = QPushButton("Got it!")
        self.got_it_button.setDefault(True)  # Enter key triggers this
        self.got_it_button.clicked.connect(self._on_got_it_clicked)
        self.got_it_button.setMinimumWidth(100)
        bottom_layout.addWidget(self.got_it_button)
        
        layout.addLayout(bottom_layout)
    
    def _on_got_it_clicked(self):
        """Handle the 'Got it!' button click."""
        # Emit signal if user checked "Don't show again"
        if self.dont_show_checkbox.isChecked():
            self.dont_show_again.emit(True)
        
        self.accept()  # Close the dialog with "accepted" status
