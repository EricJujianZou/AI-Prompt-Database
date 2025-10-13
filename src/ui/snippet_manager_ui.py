from PySide6.QtWidgets import (
    QApplication, QWidget, QListWidget, QTextEdit, QVBoxLayout, 
    QPushButton, QInputDialog, QMessageBox, QHBoxLayout, QStackedWidget, QLabel,
    QFormLayout, QComboBox, QCheckBox, QPlainTextEdit, QTableWidget, QHeaderView,
    QTableWidgetItem, QAbstractItemView, QDialog, QDialogButtonBox, QMenu
)
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt, Slot
import os

from ..storage.snippet_storage import SnippetStorage
from ..storage.settings_storage import SettingsStorage
from ..storage.history_storage import HistoryStorage
from .frameless_window import FramelessWindow
from ..core.resource_handler import get_path_for_resource


class HistoryDetailDialog(QDialog):
    """Dialog to show full history entry details."""
    
    def __init__(self, timestamp: str, query: str, result: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("History Entry Details")
        self.resize(700, 500)
        
        layout = QVBoxLayout(self)
        
        # Timestamp
        timestamp_label = QLabel(f"<b>Timestamp:</b> {timestamp}")
        layout.addWidget(timestamp_label)
        
        # Query section
        query_label = QLabel("<b>Original Query:</b>")
        layout.addWidget(query_label)
        
        self.query_text = QPlainTextEdit()
        self.query_text.setPlainText(query)
        self.query_text.setReadOnly(True)
        self.query_text.setMaximumHeight(120)
        layout.addWidget(self.query_text)
        
        # Copy query button
        copy_query_btn = QPushButton("Copy Query")
        copy_query_btn.clicked.connect(lambda: self._copy_to_clipboard(query))
        layout.addWidget(copy_query_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        
        # Result section
        result_label = QLabel("<b>Augmented Prompt:</b>")
        layout.addWidget(result_label)
        
        self.result_text = QPlainTextEdit()
        self.result_text.setPlainText(result)
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)
        
        # Copy result button
        copy_result_btn = QPushButton("Copy Augmented Prompt")
        copy_result_btn.clicked.connect(lambda: self._copy_to_clipboard(result))
        layout.addWidget(copy_result_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        
        # Dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(self.close)
        layout.addWidget(button_box)
    
    def _copy_to_clipboard(self, text: str):
        """Copy text to clipboard and show confirmation."""
        QApplication.clipboard().setText(text)
        QMessageBox.information(self, "Copied", "Text copied to clipboard!")


class SnippetUI(QWidget):
    def __init__(self, storage: SnippetStorage, settings: SettingsStorage, history: HistoryStorage, parent=None):
        super().__init__(parent)
        self.storage = storage
        self.settings = settings
        self.history = history
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle("PromptAssist Dashboard")
        self.resize(800, 600)

        main_layout = QHBoxLayout(self)

        # --- Left Navigation Pane ---
        self.nav_list = QListWidget()
        self.nav_list.addItem("Snippets")
        #self.nav_list.addItem("Settings")
        self.nav_list.addItem("History")
        self.nav_list.setMaximumWidth(150)
        main_layout.addWidget(self.nav_list)

        # --- Main Content Area ---
        self.pages = QStackedWidget()
        main_layout.addWidget(self.pages)

        # Create the different pages for the content area
        self.snippet_page = self._create_snippet_page()
        #self.settings_page = self._create_settings_page()
        self.history_page = self._create_history_page()

        # Add pages to the stacked widget
        self.pages.addWidget(self.snippet_page)
        #self.pages.addWidget(self.settings_page)
        self.pages.addWidget(self.history_page)

        # Connect navigation list to the stacked widget
        self.nav_list.currentRowChanged.connect(self.pages.setCurrentIndex)
        self.nav_list.currentRowChanged.connect(self._on_page_changed)
        
        # Load history immediately on startup (Issue #1 fix)
        self.refresh_history_table()

    def _create_snippet_page(self):
        """Creates the widget for the 'Snippets' page."""
        page = QWidget()
        layout = QVBoxLayout(page)

        self.snippet_list_widget = QListWidget()
        self._refresh_list()
        layout.addWidget(self.snippet_list_widget)

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        btn_layout = QHBoxLayout()

        self.save_button = QPushButton("Save")
        self.save_button.setObjectName("saveButton")
        self.save_button.setIcon(QIcon.fromTheme("document-save"))
        self.save_button.clicked.connect(self._save_snippet)
        btn_layout.addWidget(self.save_button)

        self.new_button = QPushButton("Create New Snippet")
        self.new_button.setObjectName("newButton")
        self.new_button.setIcon(QIcon.fromTheme("document-new"))
        self.new_button.clicked.connect(self._new_snippet)
        btn_layout.addWidget(self.new_button)

        self.del_button = QPushButton("Delete a Snippet")
        self.del_button.setObjectName("deleteButton")
        self.del_button.setIcon(QIcon.fromTheme("edit-delete"))
        self.del_button.clicked.connect(self._del_snippet)
        btn_layout.addWidget(self.del_button)

        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        self.snippet_list_widget.itemClicked.connect(self._load_snippet)
        
        return page

    def _create_settings_page(self):
        """Creates the widget for the 'Settings' page."""
        page = QWidget()
        layout = QFormLayout(page)
        layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        # --- Theme Selection ---
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])
        # Ensure the value from settings is treated as a string
        self.theme_combo.setCurrentText(str(self.settings.get("theme", "Dark")))
        self.theme_combo.currentTextChanged.connect(self._on_setting_changed)
        layout.addRow("Theme:", self.theme_combo)

        # --- Blacklisted Apps ---
        self.blacklist_edit = QPlainTextEdit()
        blacklist = self.settings.get("blacklisted_apps", [])
        # Ensure blacklist is a list before joining
        if isinstance(blacklist, list):
            self.blacklist_edit.setPlainText("\n".join(blacklist))
        self.blacklist_edit.setPlaceholderText("One app name per line, e.g., my_game.exe")
        self.blacklist_edit.textChanged.connect(self._on_setting_changed)
        layout.addRow("Blacklisted Apps:", self.blacklist_edit)
        
        return page

    def _on_setting_changed(self):
        """Generic slot to save any setting that has been changed."""
        sender = self.sender()
        # Check the type of the sender to safely access its methods
        if isinstance(sender, QComboBox) and sender == self.theme_combo:
            self.settings.set("theme", sender.currentText())
            QMessageBox.information(self, "Theme Changed", "Theme will be applied on next restart.")
        elif isinstance(sender, QPlainTextEdit) and sender == self.blacklist_edit:
            apps = sender.toPlainText().strip().split('\n')
            self.settings.set("blacklisted_apps", [app.strip() for app in apps if app.strip()])

    def _create_history_page(self):
        """Creates the widget for the 'History' page."""
        page = QWidget()
        layout = QVBoxLayout(page)

        # --- Toolbar with action buttons ---
        toolbar = QHBoxLayout()
        
        self.copy_result_btn = QPushButton("Copy Result")
        self.copy_result_btn.clicked.connect(self._copy_history_result)
        self.copy_result_btn.setEnabled(False)  # Disabled until row selected
        toolbar.addWidget(self.copy_result_btn)
        
        self.save_snippet_btn = QPushButton("Save as Snippet")
        self.save_snippet_btn.clicked.connect(self._save_history_as_snippet)
        self.save_snippet_btn.setEnabled(False)
        toolbar.addWidget(self.save_snippet_btn)
        
        self.delete_entry_btn = QPushButton("Delete Entry")
        self.delete_entry_btn.clicked.connect(self._delete_history_entry)
        self.delete_entry_btn.setEnabled(False)
        toolbar.addWidget(self.delete_entry_btn)
        
        toolbar.addStretch()  # Push buttons to the left
        
        self.clear_history_button = QPushButton("Clear All History")
        self.clear_history_button.clicked.connect(self._clear_history)
        toolbar.addWidget(self.clear_history_button)
        
        layout.addLayout(toolbar)

        # --- Table for History ---
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(3)
        self.history_table.setHorizontalHeaderLabels(["Timestamp", "Query", "Result"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.history_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        # Issue #2 fix: Better row highlighting
        self.history_table.setStyleSheet("""
            QTableWidget::item:selected {
                background-color: #0078D4;
                color: white;
            }
            QTableWidget::item:hover {
                background-color: #3A3A3A;
            }
        """)
        
        # Enable tooltips for truncated text (Issue #3 - hover preview)
        self.history_table.setMouseTracking(True)
        
        # Double-click to open detail dialog (Issue #3)
        self.history_table.doubleClicked.connect(self._show_history_detail)
        
        # Selection changed signal to enable/disable toolbar buttons
        self.history_table.itemSelectionChanged.connect(self._on_history_selection_changed)
        
        # Enable custom context menu (Issue #4 - right-click menu)
        self.history_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.history_table.customContextMenuRequested.connect(self._show_history_context_menu)

        layout.addWidget(self.history_table)

        return page

    def _on_page_changed(self, index):
        """Slot to refresh data when a page becomes visible."""
        # Index 2 corresponds to the History page
        if index == 2:
            self.refresh_history_table()

    def refresh_history_table(self):
        """
        Public method to reload all entries from history storage into the table.
        Can be called externally (e.g., from Application) when new entries are added.
        """
        self.history_table.setRowCount(0) # Clear table
        history_entries = self.history.get_all()
        self.history_table.setRowCount(len(history_entries))

        for row, entry in enumerate(history_entries):
            timestamp_text = entry.get("timestamp", "")
            query_text = entry.get("query", "")
            result_text = entry.get("result", "")
            
            # Create table items
            timestamp_item = QTableWidgetItem(timestamp_text)
            query_item = QTableWidgetItem(query_text)
            result_item = QTableWidgetItem(result_text)
            
            # Add tooltips for hover preview (first 200 chars)
            query_preview = query_text[:200] + "..." if len(query_text) > 200 else query_text
            result_preview = result_text[:200] + "..." if len(result_text) > 200 else result_text
            
            query_item.setToolTip(query_preview)
            result_item.setToolTip(result_preview)
            
            self.history_table.setItem(row, 0, timestamp_item)
            self.history_table.setItem(row, 1, query_item)
            self.history_table.setItem(row, 2, result_item)

    def _copy_history_result(self):
        """Copies the result from the selected history row to the clipboard."""
        selected_items = self.history_table.selectedItems()
        if not selected_items:
            return
        
        row = selected_items[0].row()
        result_item = self.history_table.item(row, 2)
        if result_item:
            QApplication.clipboard().setText(result_item.text())
            QMessageBox.information(self, "Copied", "Result copied to clipboard.")

    def _save_history_as_snippet(self):
        """Saves the selected history item as a new snippet."""
        selected_items = self.history_table.selectedItems()
        if not selected_items:
            return
        
        row = selected_items[0].row()
        result_item = self.history_table.item(row, 2)
        if not result_item:
            return

        command, ok = QInputDialog.getText(self, "New Snippet", "Enter command for the new snippet (e.g. ::mysnippet):")
        if ok and command:
            self.storage.save(command, result_item.text())
            self._refresh_list()  # Refresh the snippet list UI
            QMessageBox.information(self, "Snippet Saved", f"Saved as new snippet with command: {command}")

    def _clear_history(self):
        """Asks for confirmation and clears the history."""
        confirm = QMessageBox.question(
            self, "Clear History",
            "Are you sure you want to delete all history entries? This cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            self.history.clear()
            self.refresh_history_table()
            QMessageBox.information(self, "History Cleared", "All history has been deleted.")

    def _delete_history_entry(self):
        """Deletes the selected history entry."""
        selected_items = self.history_table.selectedItems()
        if not selected_items:
            return
        
        row = selected_items[0].row()
        
        confirm = QMessageBox.question(
            self, "Delete Entry",
            "Are you sure you want to delete this history entry?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            # Get all entries, remove the selected one, and save back
            history_entries = self.history.get_all()
            if 0 <= row < len(history_entries):
                del history_entries[row]
                # Clear and re-add all entries
                self.history.clear()
                for entry in history_entries:
                    self.history.add_entry(
                        query=entry.get("query", ""),
                        result=entry.get("result", "")
                    )
                self.refresh_history_table()
                QMessageBox.information(self, "Entry Deleted", "History entry has been deleted.")

    def _on_history_selection_changed(self):
        """Enable/disable toolbar buttons based on selection."""
        has_selection = len(self.history_table.selectedItems()) > 0
        self.copy_result_btn.setEnabled(has_selection)
        self.save_snippet_btn.setEnabled(has_selection)
        self.delete_entry_btn.setEnabled(has_selection)

    def _show_history_context_menu(self, position):
        """Shows the right-click context menu for history table."""
        # Only show menu if a row is selected
        if not self.history_table.selectedItems():
            return
        
        menu = QMenu(self)
        
        copy_action = QAction("Copy Result", self)
        copy_action.triggered.connect(self._copy_history_result)
        menu.addAction(copy_action)
        
        save_action = QAction("Save as Snippet", self)
        save_action.triggered.connect(self._save_history_as_snippet)
        menu.addAction(save_action)
        
        menu.addSeparator()
        
        delete_action = QAction("Delete Entry", self)
        delete_action.triggered.connect(self._delete_history_entry)
        menu.addAction(delete_action)
        
        # Show menu at cursor position
        menu.exec(self.history_table.viewport().mapToGlobal(position))

    def _show_history_detail(self, index):
        """Opens a dialog showing full history entry details on double-click."""
        row = index.row()
        
        timestamp_item = self.history_table.item(row, 0)
        query_item = self.history_table.item(row, 1)
        result_item = self.history_table.item(row, 2)
        
        if not all([timestamp_item, query_item, result_item]):
            return
        
        dialog = HistoryDetailDialog(
            timestamp=timestamp_item.text(),
            query=query_item.text(),
            result=result_item.text(),
            parent=self
        )
        dialog.exec()

    def _refresh_list(self):
        self.snippet_list_widget.clear()
        for cmd in self.storage.snippets:
            self.snippet_list_widget.addItem(cmd)

    @Slot() 
    def _load_snippet(self, item):
        cmd = item.text()
        self.text_edit.setPlainText(self.storage.snippets[cmd])
    
    @Slot()
    def _save_snippet(self):
        selected_item = self.snippet_list_widget.currentItem()
        if selected_item:
            cmd = selected_item.text()
            new_text = self.text_edit.toPlainText()
            self.storage.save(cmd, new_text)
        else:
            QMessageBox.warning(self, "No snippet selected", "Please select a snippet to save")

    @Slot()
    def _new_snippet(self):
        command, ok = QInputDialog.getText(self, "New Snippet", "Enter command (e.g. ::email)")
        if ok and command: 
            text, ok = QInputDialog.getText(self, "New Snippet", "Enter snippet text: ")
            if ok and text:
                self.storage.save(command, text)
                self._refresh_list()

    @Slot()
    def _del_snippet(self):
        selected_item = self.snippet_list_widget.currentItem()
        if selected_item:
            cmd = selected_item.text()
            confirm = QMessageBox.question(
                self, "Delete Snippet",
                f"Are you sure you want to delete {cmd}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirm == QMessageBox.StandardButton.Yes:
                self.storage.delete(cmd)
                self._refresh_list()
        else:
            QMessageBox.warning(self, "No snippet selected", "Please select a snippet to delete")

def load_stylesheet(file_path):
    try:
        with open(file_path, "r") as f:
            return f.read()
    except Exception as e:
        print(f"Error loading stylesheet: {e}")
        return ""
        
if __name__ == "__main__":
    app = QApplication([])
    
    style_path = get_path_for_resource("style.qss")
    stylesheet = load_stylesheet(style_path)
    app.setStyleSheet(stylesheet)

    storage = SnippetStorage()
    settings = SettingsStorage()
    history = HistoryStorage()
    # The SnippetUI is now the content, wrapped by our new FramelessWindow
    dashboard_content = SnippetUI(storage, settings, history)
    window = FramelessWindow(dashboard_content)
    window.show()
    app.exec()

