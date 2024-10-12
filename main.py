# Copyright (c) 2024 emSircut
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import sys
import argparse
import platform
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTextEdit, QStackedWidget, QListWidget, QScrollArea, QDesktopWidget, QMessageBox, QLineEdit
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QUrl
from PyQt5.QtGui import QColor, QFont, QFontDatabase, QKeySequence
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QShortcut
from PyQt5.QtWebEngineWidgets import QWebEngineView
from services.SetupService import SetupService
from wizards.SetupWizard import run_setup_wizard
from services.WifiService import WifiService, SimulatedWifiService
import ctypes

class MainWindow(QWidget):
    dark_mode_changed = pyqtSignal(bool)

    def __init__(self, dev_mode=False):
        super().__init__()
        self.setup_service = SetupService()
        self.is_raspberry_pi = platform.machine().startswith('aarch64')
        self.wifi_service = WifiService() if self.is_raspberry_pi else SimulatedWifiService()
        self.dev_mode = dev_mode

        if not self.setup_service.is_setup_complete():
            if not self.run_setup_wizard():
                sys.exit()

        self.dark_mode = self.setup_service.get_theme() == "dark"
        self.initUI()

    def run_setup_wizard(self):
        return run_setup_wizard(self.setup_service)

    def initUI(self):
        # Load Press Start 2P font
        font_id = QFontDatabase.addApplicationFont("fonts/PressStart2P-Regular.ttf")
        if font_id == -1:
            print("Failed to load Press Start 2P font")
        
        self.pixel_font = QFont("Press Start 2P", 10)  # Adjust font size as needed

        self.setWindowTitle('ePhone GUI')
        self.setStyleSheet("background-color: #2E2E2E; color: #FFFFFF;")  # Dark background with white text
        
        # Set window to full screen
        self.showFullScreen()

        main_layout = QHBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(main_layout)

        # Navigation bar
        nav_bar = QVBoxLayout()
        nav_bar.setSpacing(10)
        nav_bar.setContentsMargins(0, 0, 0, 0)

        # Add buttons to the navigation bar
        nav_buttons = ['HOME', 'WIFI', 'WEB', 'SETTINGS', 'ABOUT']
        for button_text in nav_buttons:
            button = QPushButton(button_text)
            button.setFont(self.pixel_font)
            button_size = self.calculate_button_size()
            button.setFixedSize(button_size[0], button_size[1])
            self.update_button_style(button)
            self.add_shadow_effect(button)
            nav_bar.addWidget(button)

        nav_bar.addStretch()

        # Add the navigation bar to the main layout
        main_layout.addLayout(nav_bar)

        # Add a vertical line as a separator
        separator = QWidget()
        separator.setFixedWidth(1)
        separator.setStyleSheet("background-color: #444444;")  # Darker separator
        main_layout.addWidget(separator)

        # Content area
        self.content_area = QStackedWidget()
        main_layout.addWidget(self.content_area)

        # Add pages to the content area
        self.add_home_page()
        self.add_wifi_page()
        self.add_web_page()
        self.add_settings_page()
        self.add_about_page()

        # Set the initial page
        self.content_area.setCurrentIndex(0)

        # Connect buttons to switch pages
        for i, button in enumerate(nav_buttons):
            nav_bar.itemAt(i).widget().clicked.connect(lambda checked, index=i: self.switch_page(index))

        # Add shortcut to quit and terminate process
        self.quit_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        self.quit_shortcut.activated.connect(self.quit_application)

        # Add developer exit option and terminal log
        if self.dev_mode:
            self.add_dev_exit_option()

    def switch_page(self, index):
        if index == 0:  # HOME button
            self.content_area.setCurrentIndex(0)  # Set to HOME page (index 0)
        else:
            self.content_area.setCurrentIndex(index)

    def calculate_button_size(self):
        screen = QDesktopWidget().screenNumber(QDesktopWidget().cursor().pos())
        screen_size = QDesktopWidget().screenGeometry(screen).size()
        
        if self.is_raspberry_pi:
            # For HyperPixel 4.0" (assuming 800x480 resolution)
            return (int(screen_size.width() * 0.1), int(screen_size.height() * 0.0625))
        else:
            # For Windows PC (adjust percentages as needed)
            return (int(screen_size.width() * 0.08), int(screen_size.height() * 0.05))

    def update_button_style(self, button):
        style = """
            QPushButton {
                background-color: #3A3A3A;  /* Dark button background */
                color: #FFFFFF;  /* White text */
                border: 2px solid #007BFF;  /* Blue border */
                border-radius: 8px;  /* Rounded corners */
                padding: 10px;  /* Padding for better touch targets */
                font-size: 12px;  /* Font size */
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4A4A4A;  /* Lighter on hover */
                border-color: #0056b3;  /* Darker blue on hover */
            }
            QPushButton:pressed {
                background-color: #222222;  /* Darker when pressed */
                border-color: #003d80;  /* Even darker blue when pressed */
            }
        """
        button.setStyleSheet(style)

    def add_shadow_effect(self, widget):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(5)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(QPoint(2, 2))
        widget.setGraphicsEffect(shadow)

    def add_home_page(self):
        home_page = QWidget()
        layout = QVBoxLayout(home_page)

        welcome_label = QLabel(f"Welcome, {self.setup_service.get_user_name()}!")
        welcome_label.setFont(self.pixel_font)
        welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_label)

        info_label = QLabel("Your ePhone is ready to use.")
        info_label.setFont(self.pixel_font)
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)

        # Add more widgets or information to the home page as needed

        if self.dev_mode:
            restart_setup_button = QPushButton("Restart Setup")
            restart_setup_button.clicked.connect(self.restart_setup)
            layout.addWidget(restart_setup_button)

        self.content_area.addWidget(home_page)

    def restart_setup(self):
        self.setup_service.reset_setup()
        if self.run_setup_wizard():
            self.dark_mode = self.setup_service.get_theme() == "dark"
            self.update_styles()
            self.content_area.removeWidget(self.content_area.widget(0))
            self.add_home_page()
            self.content_area.setCurrentIndex(0)

    def add_wifi_page(self):
        wifi_page = QWidget()
        layout = QVBoxLayout(wifi_page)

        if not self.is_raspberry_pi:
            disclaimer = QLabel("DISCLAIMER: This is a simulated WiFi environment.\nActual WiFi service is not available on this device.")
            disclaimer.setStyleSheet("color: red; font-weight: bold;")
            disclaimer.setAlignment(Qt.AlignCenter)
            layout.addWidget(disclaimer)

        # Current network display
        current_network_label = QLabel("Current Network:")
        current_network_label.setFont(self.pixel_font)
        layout.addWidget(current_network_label)

        self.current_network_display = QLabel()
        self.current_network_display.setFont(self.pixel_font)
        layout.addWidget(self.current_network_display)

        # Available networks list
        available_networks_label = QLabel("Available Networks:")
        available_networks_label.setFont(self.pixel_font)
        layout.addWidget(available_networks_label)

        self.network_list = QListWidget()
        self.network_list.setFont(self.pixel_font)
        layout.addWidget(self.network_list)

        # Refresh button
        refresh_button = QPushButton("Refresh Networks")
        refresh_button.setFont(self.pixel_font)
        refresh_button.clicked.connect(self.refresh_networks)
        layout.addWidget(refresh_button)

        # Connect button
        connect_button = QPushButton("Connect to Selected Network")
        connect_button.setFont(self.pixel_font)
        connect_button.clicked.connect(self.connect_to_network)
        layout.addWidget(connect_button)

        self.content_area.addWidget(wifi_page)

        # Initial network refresh
        self.refresh_networks()

    def refresh_networks(self):
        self.network_list.clear()
        networks = self.wifi_service.get_available_networks()
        self.network_list.addItems(networks)
        current_network = self.wifi_service.get_current_network()
        self.current_network_display.setText(current_network if current_network else "Not connected")

    def connect_to_network(self):
        selected_network = self.network_list.currentItem()
        if selected_network:
            ssid = selected_network.text()
            # In a real scenario, you'd prompt for a password here
            password = "dummy_password"
            if self.wifi_service.connect_to_network(ssid, password):
                self.current_network_display.setText(ssid)
                QMessageBox.information(self, "Connection Successful", f"Connected to {ssid}")
            else:
                QMessageBox.warning(self, "Connection Failed", f"Failed to connect to {ssid}")
        else:
            QMessageBox.warning(self, "No Network Selected", "Please select a network to connect")

    def add_web_page(self):
        web_page = QWidget()
        layout = QVBoxLayout(web_page)

        # URL input and Go button in horizontal layout
        url_layout = QHBoxLayout()
        
        url_input = QLineEdit()
        url_input.setPlaceholderText("Enter URL")
        url_input.setFont(self.pixel_font)
        url_layout.addWidget(url_input)

        go_button = QPushButton("Go")
        go_button.setFont(self.pixel_font)
        url_layout.addWidget(go_button)

        layout.addLayout(url_layout)

        # QWebEngineView widget
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

        # Load initial URL
        self.web_view.setUrl(QUrl("https://www.google.com"))

        # Connect Go button to load URL
        go_button.clicked.connect(lambda: self.load_url(url_input.text()))

        self.content_area.addWidget(web_page)

    def load_url(self, url):
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url
        self.web_view.setUrl(QUrl(url))

    def add_settings_page(self):
        settings_page = QWidget()
        layout = QVBoxLayout(settings_page)

        # Dark Mode Toggle
        dark_mode_label = QLabel("Toggle Dark Mode")
        dark_mode_label.setFont(self.pixel_font)
        layout.addWidget(dark_mode_label)

        self.dark_mode_button = QPushButton("Dark Mode" if not self.dark_mode else "Light Mode")
        self.dark_mode_button.setFont(self.pixel_font)
        self.dark_mode_button.clicked.connect(self.toggle_dark_mode)
        self.update_button_style(self.dark_mode_button)
        layout.addWidget(self.dark_mode_button)

        # Update button text when dark mode changes
        self.dark_mode_changed.connect(self.update_dark_mode_button_text)

        self.content_area.addWidget(settings_page)

    def add_about_page(self):
        about_page = QWidget()
        layout = QVBoxLayout(about_page)
        label = QLabel("ePhone GUI\nVersion 1.0\nDeveloped by emSircut\n- andy was here -")
        label.setFont(self.pixel_font)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.content_area.addWidget(about_page)

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.update_styles()
        self.dark_mode_changed.emit(self.dark_mode)

    def update_styles(self):
        # Update main window background
        self.setStyleSheet(f"background-color: {'#2E2E2E' if self.dark_mode else 'white'}; color: {'#FFFFFF' if self.dark_mode else '#000000'};")
        
        # Update all buttons
        for button in self.findChildren(QPushButton):
            self.update_button_style(button)
        
        # Update QListWidget (network list) style
        self.network_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {'#3A3A3A' if self.dark_mode else '#FFFFFF'};
                color: {'#FFFFFF' if self.dark_mode else '#000000'};
                border: 1px solid {'#007BFF' if self.dark_mode else '#CCCCCC'};
                border-radius: 5px;  /* Rounded corners */
            }}
            QListWidget::item:selected {{
                background-color: {'#555555' if self.dark_mode else '#DDDDDD'};
            }}
        """)
        
        # Update labels
        for label in self.findChildren(QLabel):
            label.setStyleSheet(f"color: {'#FFFFFF' if self.dark_mode else '#000000'};")

    def update_dark_mode_button_text(self, is_dark_mode):
        self.dark_mode_button.setText("Light Mode" if is_dark_mode else "Dark Mode")
        self.update_button_style(self.dark_mode_button)

    def quit_application(self):
        QApplication.quit()

    def add_dev_exit_option(self):
        # Add a hidden button for exiting (only visible in dev mode)
        exit_button = QPushButton("DEV EXIT", self)
        exit_button.setFont(self.pixel_font)
        button_size = self.calculate_button_size()
        exit_button.setFixedSize(button_size[0], button_size[1])
        self.update_button_style(exit_button)
        exit_button.move(10, 10)  # Position it in the top-left corner
        exit_button.clicked.connect(self.confirm_exit)

        # Add a keyboard shortcut for exiting (Ctrl+Shift+Q)
        self.exit_shortcut = QShortcut(QKeySequence("Ctrl+Shift+Q"), self)
        self.exit_shortcut.activated.connect(self.confirm_exit)

    def confirm_exit(self):
        reply = QMessageBox.question(self, 'Exit Confirmation',
                                     "Are you sure you want to exit the application?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            QApplication.quit()

    def closeEvent(self, event):
        cef.Shutdown()
        event.accept()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dev-mode', action='store_true', help='Enable developer mode')
    args = parser.parse_args()

    app = QApplication(sys.argv)
    
    # This attribute must be set before creating the application.
    ctypes.windll.user32.SetProcessDPIAware()

    window = MainWindow(dev_mode=args.dev_mode)
    window.show()
    

    
    sys.exit(app.exec_())