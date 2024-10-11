# ePhone-GUI

## Description
ePhone-GUI is a Python-based graphical user interface designed for the Raspberry Pi Zero 2 W running 64-bit Raspberry Pi OS. This project transforms the Pi into a customizable phone-like device with a touchscreen interface, offering features like WiFi management, system settings, and more.

## Features
- Fullscreen GUI optimized for Raspberry Pi touchscreen displays
- Navigation sidebar with Home, Settings, and About pages
- Dark mode toggle for comfortable viewing in various lighting conditions
- WiFi connection management tailored for Raspberry Pi
- Custom pixel font integration (Press Start 2P) for a unique visual style
- Keyboard shortcuts for quick actions (useful when a keyboard is attached)

## Hardware Requirements
- Raspberry Pi Zero 2 W
- Raspberry Pi-compatible touchscreen display
- Power supply
- (Optional) Case or enclosure

## Software Requirements
- Raspberry Pi OS (64-bit) Lite or Desktop
- Python 3.7+
- PyQt5
- Other dependencies (listed in requirements.txt)

## Installation

### Setting up your Raspberry Pi
1. Install Raspberry Pi OS (64-bit) on your Pi Zero 2 W
2. Ensure your Pi is connected to the internet
3. Update your system:
   ```
   sudo apt update && sudo apt upgrade -y
   ```

### Installing ePhone-GUI
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ePhone-GUI.git
   cd ePhone-GUI
   ```

2. Install required system packages:
   ```
   sudo apt install python3-pyqt5 python3-pip
   ```

3. Install Python dependencies:
   ```
   pip3 install -r requirements.txt
   ```

4. Make the main script executable:
   ```
   chmod +x main.py
   ```

5. Run the application:
   ```
   python3 main.py
   ```

## Usage
- Navigate through the app using the touchscreen or connected mouse
- Use the sidebar buttons to switch between Home, Settings, and About pages
- Toggle dark mode in the Settings page for comfortable viewing
- Manage WiFi connections directly from the interface
- Use keyboard shortcuts (if a keyboard is attached):
  - 'Q': Quit the application
  - 'F': Toggle fullscreen mode
  - 'D': Toggle dark mode

## Auto-start on Boot
To have ePhone-GUI start automatically when your Raspberry Pi boots:

1. Edit the autostart file:
   ```
   sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
   ```

2. Add this line at the end of the file:
   ```
   @/usr/bin/python3 /home/pi/ePhone-GUI/main.py
   ```

3. Save and exit (Ctrl+X, then Y, then Enter)

## Development
To run the application in development mode with additional debugging features:
```
python3 main.py --dev-interface
```

## Contributing
Contributions to the ePhone-GUI project are welcome! Please follow these steps:
1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
This project is licensed under the [MIT License](LICENSE).

## Acknowledgements
- [Raspberry Pi Foundation](https://www.raspberrypi.org/)
- [Press Start 2P Font](https://fonts.google.com/specimen/Press+Start+2P)
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/)

## Contact
- email@example.com -

Project Link: [https://github.com/yourusername/ePhone-GUI](https://github.com/yourusername/ePhone-GUI)

