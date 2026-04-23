#!/bin/bash

# Configuration
PROJECT_DIR="/Users/galihpratama/Dev/dawn-dash"
PLIST_NAME="com.dawndash.bot"
PLIST_PATH="$HOME/Library/LaunchAgents/$PLIST_NAME.plist"
DOCKER_BIN=$(which docker)

if [ -z "$DOCKER_BIN" ]; then
    DOCKER_BIN="/usr/local/bin/docker"
fi

echo "🚀 Setting up autostart for Dawn Dash..."

# Create the plist file
cat <<EOF > "$PLIST_PATH"
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>$PLIST_NAME</string>
    <key>ProgramArguments</key>
    <array>
        <string>$DOCKER_BIN</string>
        <string>compose</string>
        <string>-f</string>
        <string>$PROJECT_DIR/compose.yaml</string>
        <string>up</string>
        <string>-d</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>WorkingDirectory</key>
    <string>$PROJECT_DIR</string>
    <key>StandardOutPath</key>
    <string>$PROJECT_DIR/data/autostart.log</string>
    <key>StandardErrorPath</key>
    <string>$PROJECT_DIR/data/autostart.err</string>
</dict>
</plist>
EOF

# Set permissions
chmod 644 "$PLIST_PATH"

# Load the agent
launchctl unload "$PLIST_PATH" 2>/dev/null
launchctl load "$PLIST_PATH"

echo "✅ Autostart configured at $PLIST_PATH"
echo "📝 Logs will be at $PROJECT_DIR/data/autostart.log"
echo "💡 To disable, run: launchctl unload $PLIST_PATH"
