#!/bin/bash
# OpenAgenda v1.4 AppImage Wrapper

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create AppDir structure
mkdir -p "$SCRIPT_DIR/AppDir/usr/bin"
mkdir -p "$SCRIPT_DIR/AppDir/usr/share/applications"
mkdir -p "$SCRIPT_DIR/AppDir/usr/share/pixmaps"

# Copy application files
cp "$SCRIPT_DIR/open-agenda-v1.4.py" "$SCRIPT_DIR/AppDir/usr/bin/open-agenda"

# Create launcher
cat > "$SCRIPT_DIR/AppDir/usr/bin/open-agenda" << 'EOF'
#!/bin/bash
SELF=$(readlink -f "$0")
APPDIR=${SELF%/*}
cd "$APPDIR"
python3 "$(dirname "$SELF")/open_agenda.py" "$@"
EOF

chmod +x "$SCRIPT_DIR/AppDir/usr/bin/open-agenda"

# Copy desktop file
cp "$SCRIPT_DIR/open-agenda-v1.4.desktop" "$SCRIPT_DIR/AppDir/usr/share/applications/"

# Copy icon
cp "$SCRIPT_DIR/open-agenda-icon.png" "$SCRIPT_DIR/AppDir/usr/share/pixmaps/"

# Create AppRun
cat > "$SCRIPT_DIR/AppDir/AppRun" << 'EOF'
#!/bin/bash
SELF=$(readlink -f "$0")
APPDIR=${SELF%/*}
export PATH="$APPDIR/usr/bin:$PATH"
exec python3 "$APPDIR/usr/bin/open-agenda" "$@"
EOF

chmod +x "$SCRIPT_DIR/AppDir/AppRun"

# Copy icon to AppDir
cp "$SCRIPT_DIR/open-agenda-icon.png" "$SCRIPT_DIR/AppDir/"

echo "AppDir structure created!"
