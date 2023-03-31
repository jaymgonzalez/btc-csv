#!/bin/bash

# ip=$(dig +short myip.opendns.com @resolver1.opendns.com)

dir=/home/jay-server-ventas/workspace/bot

cd $dir

# Activate the virtual environment
source ./bin/activate

cd btc-csv

# Get updated repo
git pull

# Run your Python file
python download_data.py

# Create a commit with a message indicating the changes made
git commit -am "Automated commit $(date)"

# Push the changes to GitHub
git push origin main

# Deactivate the virtual environment
deactivate