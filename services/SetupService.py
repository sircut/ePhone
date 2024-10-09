import json
import os

class SetupService:
    def __init__(self):
        self.config_file = 'config.json'
        self.config = self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {"setup_complete": False, "user_name": "", "theme": "light", "wifi_auto_connect": False}

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f)

    def is_setup_complete(self):
        return self.config.get("setup_complete", False)

    def complete_setup(self, user_name, theme, wifi_auto_connect):
        self.config["setup_complete"] = True
        self.config["user_name"] = user_name
        self.config["theme"] = theme
        self.config["wifi_auto_connect"] = wifi_auto_connect
        self.save_config()

    def reset_setup(self):
        self.config["setup_complete"] = False
        self.save_config()

    def get_user_name(self):
        return self.config.get("user_name", "")

    def get_theme(self):
        return self.config.get("theme", "light")

    def get_wifi_auto_connect(self):
        return self.config.get("wifi_auto_connect", False)
