import sys
from PyQt5.QtWidgets import QApplication, QWizard, QWizardPage, QLabel, QLineEdit, QVBoxLayout, QComboBox, QCheckBox
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt

class SetupWizard(QWizard):
    def __init__(self, setup_service):
        super().__init__()
        self.setup_service = setup_service
        self.setWindowTitle("ePhone Setup Wizard")
        self.setWizardStyle(QWizard.ModernStyle)

        # Load pixel font
        font_id = QFontDatabase.addApplicationFont("fonts/PressStart2P-Regular.ttf")
        if font_id == -1:
            print("Failed to load Press Start 2P font")
        self.pixel_font = QFont("Press Start 2P", 10)

        self.addPage(WelcomePage(self.pixel_font))
        self.addPage(UserInfoPage(self.pixel_font))
        self.addPage(PreferencesPage(self.pixel_font))
        self.addPage(CompletionPage(self.pixel_font))

        self.finished.connect(self.on_finished)

    def on_finished(self):
        if self.result() == QWizard.Accepted:
            user_name = self.field("user_name")
            theme = "dark" if self.field("dark_mode") else "light"
            wifi_auto_connect = self.field("wifi_auto_connect")
            self.setup_service.complete_setup(user_name, theme, wifi_auto_connect)

class WelcomePage(QWizardPage):
    def __init__(self, pixel_font):
        super().__init__()
        self.setTitle("Welcome to ePhone Setup")
        layout = QVBoxLayout()
        label = QLabel("This wizard will guide you through setting up your ePhone. Click Next to continue.")
        label.setFont(pixel_font)
        label.setWordWrap(True)
        layout.addWidget(label)
        self.setLayout(layout)

class UserInfoPage(QWizardPage):
    def __init__(self, pixel_font):
        super().__init__()
        self.setTitle("User Information")
        layout = QVBoxLayout()

        name_label = QLabel("Enter your name:")
        name_label.setFont(pixel_font)
        layout.addWidget(name_label)

        name_input = QLineEdit()
        name_input.setFont(pixel_font)
        layout.addWidget(name_input)
        self.registerField("user_name*", name_input)

        self.setLayout(layout)

class PreferencesPage(QWizardPage):
    def __init__(self, pixel_font):
        super().__init__()
        self.setTitle("Preferences")
        layout = QVBoxLayout()

        theme_label = QLabel("Choose your theme:")
        theme_label.setFont(pixel_font)
        layout.addWidget(theme_label)

        self.dark_mode_checkbox = QCheckBox("Dark Mode")
        self.dark_mode_checkbox.setFont(pixel_font)
        layout.addWidget(self.dark_mode_checkbox)
        self.registerField("dark_mode", self.dark_mode_checkbox)

        wifi_label = QLabel("WiFi Settings:")
        wifi_label.setFont(pixel_font)
        layout.addWidget(wifi_label)

        self.wifi_auto_connect = QCheckBox("Automatically connect to known networks")
        self.wifi_auto_connect.setFont(pixel_font)
        layout.addWidget(self.wifi_auto_connect)
        self.registerField("wifi_auto_connect", self.wifi_auto_connect)

        self.setLayout(layout)

class CompletionPage(QWizardPage):
    def __init__(self, pixel_font):
        super().__init__()
        self.setTitle("Setup Complete")
        layout = QVBoxLayout()
        label = QLabel("Congratulations! Your ePhone is now set up and ready to use.")
        label.setFont(pixel_font)
        label.setWordWrap(True)
        layout.addWidget(label)
        self.setLayout(layout)

def run_setup_wizard(setup_service):
    wizard = SetupWizard(setup_service)
    result = wizard.exec_()
    return result == QWizard.Accepted
