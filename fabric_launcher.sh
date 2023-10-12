#!/bin/bash

# Check if "variables.txt" exists
if [ -f "variables.txt" ]; then
    # Use awk to create variables
    while IFS='=' read -r key value; do
        declare "$key=$value"
    done < "variables.txt"
    
    # Check if MODLOADER is "Fabric"
    if [ "$MODLOADER" = "Fabric" ]; then
        # Define the URL to download the jar file
        fabric_url="https://meta.fabricmc.net/v2/versions/loader/$MINECRAFT_VERSION/$MODLOADER_VERSION/$FABRIC_INSTALLER_VERSION/server/jar"
        
        # Download the jar file using curl
        http_status=$(curl -w "%{http_code}" -o "fabric-server-launch.jar" "$fabric_url" -s)
        
        # Check if the download is successful
        if [ "$http_status" -eq 200 ]; then
            echo "File downloaded as fabric-server-launch.jar"
        else
            echo "Failed to download file: $http_status"
        fi
    else
        echo "MODLOADER is not Fabric. Doing nothing."
    fi
else
    echo "variables.txt not found. Doing nothing."
fi

# If the file fabric-server-launch.jar exists, rename it to server.jar
if [ -f "fabric-server-launch.jar" ]; then
    rm -rf server.jar
    mv fabric-server-launch.jar server.jar
    echo "Renamed fabric-server-launch.jar to server.jar"
else
    echo "An error occurred: fabric-server-launch.jar not found."
fi
