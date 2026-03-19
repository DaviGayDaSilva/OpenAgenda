#!/bin/bash
# OpenAgenda v1.4 - Android (Termux) Installer
# Install on Android: termux-setup-storage, then run this script

echo "📅 OpenAgenda v1.4 - Android Installer"
echo "======================================"

# Update packages
echo "📦 Updating packages..."
apt update && apt upgrade -y

# Install Python and tkinter
echo "🐍 Installing Python and tkinter..."
apt install -y python3 python3-tk

# Create app directory
mkdir -p ~/open-agenda
cd ~/open-agenda

# Copy files from current directory (if mounted)
if [ -f "/sdcard/Download/open-agenda-v1.4.py" ]; then
    cp /sdcard/Download/open-agenda-v1.4.py .
    cp /sdcard/Download/open-agenda-v1.4.desktop .
elif [ -f "$(dirname "$0")/open-agenda-v1.4.py" ]; then
    cp "$(dirname "$0")/open-agenda-v1.4.py" .
fi

# Create launcher script
cat > open-agenda << 'EOF'
#!/bin/bash
cd ~/open-agenda
python3 open-agenda-v1.4.py
EOF

chmod +x open-agenda

# Create shortcut
echo "#!/bin/bash
cd ~/open-agenda
python3 open-agenda-v1.4.py" > $PREFIX/bin/open-agenda
chmod +x $PREFIX/bin/open-agenda

echo ""
echo "✅ Installation complete!"
echo "📱 Run with: open-agenda"
echo "   Or: python3 ~/open-agenda/open-agenda-v1.4.py"
echo ""
echo "📍 Data will be saved in: ~/open-agenda/"
