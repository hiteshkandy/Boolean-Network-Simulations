#!/bin/bash

# Directory provided as argument
directory="$1"

# Check if directory exists
if [ ! -d "$directory" ]; then
    echo "Directory does not exist."
    exit 1
fi

# Loop through all files in the directory
for file in "$directory"/*; do
    if [ -f "$file" ]; then
        # Sort the file by the first word and overwrite the file
        sort -k1,1 "$file" -o "$file"
        echo "Sorted $file"
    fi
done
