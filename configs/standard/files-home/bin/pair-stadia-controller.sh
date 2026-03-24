#!/bin/bash

# Default to your controller's MAC, but allow passing a custom one as an argument
DEFAULT_CONTROLLER_MAC="E0:1E:9D:D9:36:B1" # 97NC-36B1
MAC="${1:-$DEFAULT_CONTROLLER_MAC}"

echo "🧹 Removing any existing/stale pairing for $MAC..."
# We ignore errors here in case it's already removed
bluetoothctl remove "$MAC" > /dev/null 2>&1

echo -e "\n🎮 Please put your controller into pairing mode."
echo "   (For Stadia: Hold Stadia + Y until it flashes orange)"
read -n 1 -s -r -p "Press any key to continue once it's flashing..."
echo -e "\n"

echo "📡 Scanning for devices in the background..."
# Start a scan in the background
bluetoothctl scan on > /dev/null 2>&1 &
SCAN_PID=$!

echo "⏳ Waiting for device to be discovered..."
MAX_WAIT=20
WAIT_COUNT=0
DISCOVERED=false

# Wait until the device becomes known to bluez
while [ $WAIT_COUNT -lt $MAX_WAIT ]; do
    # 'bluetoothctl info' returns an exit code of 0 if it has found the MAC
    if bluetoothctl info "$MAC" > /dev/null 2>&1; then
        DISCOVERED=true
        break
    fi
    sleep 1
    ((WAIT_COUNT++))
done

# We found it (or timed out), so we can stop scanning
kill $SCAN_PID > /dev/null 2>&1

if [ "$DISCOVERED" = false ]; then
    echo "❌ Failed to discover device $MAC after $MAX_WAIT seconds."
    echo "Please ensure it is in pairing mode and try again."
    exit 1
fi

echo "✅ Device discovered!"
echo "🔄 Attempting to pair (up to 3 tries)..."

PAIR_SUCCESS=false
for i in {1..3}; do
    if bluetoothctl pair "$MAC"; then
        PAIR_SUCCESS=true
        break
    fi
    echo "⚠️ Pairing attempt $i failed. Retrying in 2 seconds..."
    sleep 2
done

if [ "$PAIR_SUCCESS" = false ]; then
    echo "❌ Failed to pair securely after 3 attempts. You might need to restart the controller."
    exit 1
fi

echo "🤝 Trusting device..."
bluetoothctl trust "$MAC"

echo "🔌 Connecting to device..."
CONNECT_SUCCESS=false
for i in {1..3}; do
    if bluetoothctl connect "$MAC"; then
        CONNECT_SUCCESS=true
        break
    fi
    echo "⚠️ Connection attempt $i failed. Retrying in 2 seconds..."
    sleep 2
done

if [ "$CONNECT_SUCCESS" = false ]; then
    echo "❌ Failed to complete the connection."
    exit 1
fi

echo "🎉 Success! The controller is paired, trusted, and connected."
