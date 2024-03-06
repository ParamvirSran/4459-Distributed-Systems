#!/bin/bash

# Define log file for this script's operations
LOG_FILE="testing.log"
echo "Testing session started at $(date)" > "$LOG_FILE"

# Stop any previously running instances of the servers
echo "Stopping any existing servers (primary, backup, and heartbeat)..."
pkill -f heartbeat_service.py
pkill -f primary.py
pkill -f backup.py

# Start the Heartbeat Server
echo "Starting the Heartbeat Server..."
python heartbeat_service.py &
HEARTBEAT_PID=$!
echo "Heartbeat Server started with PID $HEARTBEAT_PID"
echo "Heartbeat Server PID: $HEARTBEAT_PID" >> "$LOG_FILE"

# Wait for the Heartbeat Server to initialize
sleep 2

# Start the Primary Server
echo "Starting the Primary Server..."
python primary.py &
PRIMARY_PID=$!
echo "Primary Server started with PID $PRIMARY_PID"
echo "Primary Server PID: $PRIMARY_PID" >> "$LOG_FILE"

# Wait for the Primary Server to initialize
sleep 2

# Start the Backup Server
echo "Starting the Backup Server..."
python backup.py &
BACKUP_PID=$!
echo "Backup Server started with PID $BACKUP_PID"
echo "Backup Server PID: $BACKUP_PID" >> "$LOG_FILE"

# Instructions for manual testing
echo "All servers are running. You can now test the system manually by running 'python client.py'."
echo "Press CTRL+C to stop all servers and end this testing session."

# Function to clean up (stop all servers) upon script exit
cleanup() {
    echo "Stopping all servers..."
    kill $HEARTBEAT_PID $PRIMARY_PID $BACKUP_PID
    echo "All servers stopped."
    echo "Testing session ended at $(date)" >> "$LOG_FILE"
}

# Trap SIGINT (Ctrl+C) and SIGTERM; call cleanup function
trap cleanup SIGINT SIGTERM

# Wait indefinitely until a signal is received
wait
