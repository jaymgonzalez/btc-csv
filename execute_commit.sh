#!/bin/bash

# Run your Python file
python download_data.py

# Create a commit with a message indicating the changes made
git commit -am "Automated commit $(date)"

# Push the changes to GitHub
git push origin main
