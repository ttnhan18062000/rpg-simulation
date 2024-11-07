#!/bin/bash

# Array of directories to check and their corresponding processes
declare -A processes
processes["dashboard"]="npm run dev"
processes["dashboard/server"]="node server.js"
processes["data_streaming/kafka"]="python push_to_mongodb.py"
processes["game"]="python game.py"


# Loop through each directory and associated command
for dir in "${!processes[@]}"; do
    if [ -d "$dir" ]; then
        echo "Directory $dir exists. Starting associated process..."
        ${processes[$dir]} &  # Run the command in the background
    else
        echo "Directory $dir does not exist. Skipping process."
    fi
done

# Wait for all background processes to complete
wait