#!/bin/bash
set -e

# Create static styles directory if it doesn't exist
mkdir -p /app/static/styles

# Copy style images to static directory for serving
# STYLES_DIR is an environment variable set in Dockerfile (e.g., /app/data/styles)
if [ -d "$STYLES_DIR" ]; then
  echo "Source style directory $STYLES_DIR found. Copying contents..."
  # Using rsync for better handling of subdirectories and updates
  rsync -a --delete "$STYLES_DIR/" /app/static/styles/
  echo "Copied style images to static directory: /app/static/styles"
else
  echo "Warning: Style directory $STYLES_DIR does not exist. No styles will be copied."
fi

# Execute the command passed as arguments to this script (which will be the CMD from Dockerfile)
echo "Executing command: $@"
exec "$@" 