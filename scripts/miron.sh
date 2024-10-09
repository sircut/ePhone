#!/bin/bash

# This application sets up a Python or Shell script to run on boot, compatible with Raspberry Pi OS (ARM)

# Check if a script file is provided as an argument
if [ $# -eq 0 ]; then
    echo "Error: No script file specified."
    echo "Usage: $0 <script_file>"
    exit 1
fi

SCRIPT_FILE="$1"

# Check if the specified script file exists
if [ ! -f "$SCRIPT_FILE" ]; then
    echo "Error: Script file '$SCRIPT_FILE' not found."
    exit 1
fi

# Check if the specified file is a Python or Shell script
if [[ "$SCRIPT_FILE" == *.py ]]; then
    EXEC_COMMAND="/usr/bin/python3"
elif [[ "$SCRIPT_FILE" == *.sh ]]; then
    EXEC_COMMAND="/bin/bash"
else
    echo "Error: Unsupported file type. Please provide a .py or .sh file."
    exit 1
fi

# Create the systemd service file
SERVICE_FILE="/etc/systemd/system/miron.service"
sudo tee "$SERVICE_FILE" > /dev/null << EOF
[Unit]
Description=Miron Script Runner
After=network.target

[Service]
Type=simple
ExecStart=$EXEC_COMMAND $(realpath "$SCRIPT_FILE")
User=$USER
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and enable the service
sudo systemctl daemon-reload
sudo systemctl enable miron.service

echo "Miron has been set up to run the specified script on boot for Raspberry Pi Zero 2 W."
echo "The script will run automatically when the system starts."
echo "To start the service immediately, use: sudo systemctl start miron.service"
echo "To stop the service, use: sudo systemctl stop miron.service"
echo "To check the status, use: sudo systemctl status miron.service"

