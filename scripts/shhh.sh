#!/bin/bash

# This app sets up SSH for Raspberry Pi OS (ARM)

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit
fi

# Update package list
apt update

# Install SSH server (if not already installed)
apt install -y openssh-server

# Enable and start the SSH service
systemctl enable ssh
systemctl start ssh

# Configure SSH for Raspberry Pi OS (ARM)
SSH_CONFIG="/etc/ssh/sshd_config"

# Backup the original SSH config file
cp "$SSH_CONFIG" "${SSH_CONFIG}.bak"

# Configure SSH settings
cat << EOF >> "$SSH_CONFIG"

# Disable root login
PermitRootLogin no

# Use SSH protocol 2
Protocol 2

# Set maximum authentication attempts
MaxAuthTries 3

# Disable empty passwords
PermitEmptyPasswords no

# Enable public key authentication
PubkeyAuthentication yes

# Disable password authentication (uncomment if using only key-based auth)
# PasswordAuthentication no

# Set idle timeout interval
ClientAliveInterval 300
ClientAliveCountMax 2

# Allow only specific users (replace with your username)
AllowUsers pi

# Restrict SSH access to a specific IP range (uncomment and modify as needed)
# AllowUsers *@192.168.1.0/24

EOF

# Restart SSH service to apply changes
systemctl restart ssh

echo "SSH has been configured with enhanced security settings for Raspberry Pi OS (ARM)."
echo "Please review the changes in $SSH_CONFIG and adjust as needed."
echo "Remember to set up public key authentication before disabling password authentication."

# Enable SSH at boot (in case it's not already enabled)
raspi-config nonint do_ssh 0

echo "SSH configuration for Raspberry Pi OS (ARM) is complete."

