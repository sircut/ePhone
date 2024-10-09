# Copyright (c) 2024 emSircut
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import subprocess
import time
import platform
import re
import random

class WifiService:
    def __init__(self):
        self.is_raspberry_pi = platform.machine().startswith('aarch64')

    def connect_to_network(self, ssid, password):
        try:
            if self.is_raspberry_pi:
                return self._connect_to_network_raspberry_pi(ssid, password)
            else:
                print("This device is not a 64-bit Raspberry Pi.")
                return False
        except Exception as e:
            print(f"Error connecting to WiFi: {str(e)}")
            return False

    def _connect_to_network_raspberry_pi(self, ssid, password):
        try:
            # Check if already connected
            result = subprocess.run(['iwgetid', '-r'], capture_output=True, text=True)
            if result.stdout.strip() == ssid:
                print(f"Already connected to {ssid}")
                return True

            # Create wpa_supplicant.conf file
            wpa_supplicant_conf = f"""
            ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
            update_config=1
            country=US

            network={{
                ssid="{ssid}"
                psk="{password}"
                key_mgmt=WPA-PSK
            }}
            """
            with open('/tmp/wpa_supplicant.conf', 'w') as f:
                f.write(wpa_supplicant_conf)

            # Move the configuration file to the correct location
            subprocess.run(['sudo', 'mv', '/tmp/wpa_supplicant.conf', '/etc/wpa_supplicant/wpa_supplicant.conf'], check=True)

            # Restart the wireless interface
            subprocess.run(['sudo', 'ifconfig', 'wlan0', 'down'], check=True)
            subprocess.run(['sudo', 'ifconfig', 'wlan0', 'up'], check=True)

            # Reconfigure wpa_supplicant
            subprocess.run(['sudo', 'wpa_cli', '-i', 'wlan0', 'reconfigure'], check=True)

            # Wait for connection
            for _ in range(30):  # Wait up to 30 seconds
                result = subprocess.run(['iwgetid', '-r'], capture_output=True, text=True)
                if result.stdout.strip() == ssid:
                    print(f"Successfully connected to {ssid}")
                    return True
                time.sleep(1)

            print(f"Failed to connect to {ssid}")
            return False

        except Exception as e:
            print(f"Error connecting to WiFi on Raspberry Pi: {str(e)}")
            return False

    def get_available_networks(self):
        try:
            if self.is_raspberry_pi:
                result = subprocess.run(['sudo', 'iwlist', 'wlan0', 'scan'], capture_output=True, text=True)
                networks = re.findall(r'ESSID:"(.*?)"', result.stdout)
                return list(set(networks))  # Remove duplicates
            else:
                print("This device is not a 64-bit Raspberry Pi.")
                return []
        except Exception as e:
            print(f"Error scanning for networks: {str(e)}")
            return []

    def get_current_network(self):
        try:
            if self.is_raspberry_pi:
                result = subprocess.run(['iwgetid', '-r'], capture_output=True, text=True)
                return result.stdout.strip()
            else:
                print("This device is not a 64-bit Raspberry Pi.")
                return None
        except Exception as e:
            print(f"Error getting current network: {str(e)}")
            return None

class SimulatedWifiService:
    def __init__(self):
        self.networks = ["SimNet1", "SimNet2", "SimNet3", "SimNet4", "SimNet5"]
        self.current_network = None

    def connect_to_network(self, ssid, password):
        if ssid in self.networks:
            self.current_network = ssid
            return True
        return False

    def get_available_networks(self):
        return self.networks

    def get_current_network(self):
        return self.current_network
