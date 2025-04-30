#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}Starting environment setup...${NC}"

# Clean up existing environment
echo -e "${GREEN}Cleaning up existing environment...${NC}"
deactivate 2>/dev/null || true
rm -rf "$PROJECT_ROOT/venv"
rm -rf "$PROJECT_ROOT/__pycache__"
rm -rf "$PROJECT_ROOT/.pytest_cache"
find "$PROJECT_ROOT" -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null

# Create required directories
echo -e "${GREEN}Creating required directories...${NC}"
mkdir -p "$PROJECT_ROOT/data/styles"
mkdir -p "$PROJECT_ROOT/data/metrics"
mkdir -p "$PROJECT_ROOT/data/reference"

# Download sample style image if styles directory is empty
if [ ! "$(ls -A $PROJECT_ROOT/data/styles)" ]; then
    echo -e "${GREEN}Downloading sample style image...${NC}"
    curl https://raw.githubusercontent.com/tensorflow/models/master/research/nst_blogpost/starry_night.jpg -o "$PROJECT_ROOT/data/styles/starry_night.jpg"
fi

# Create new virtual environment
echo -e "${GREEN}Creating new virtual environment...${NC}"
cd "$PROJECT_ROOT"
python -m venv venv

# Activate virtual environment
echo -e "${GREEN}Activating virtual environment...${NC}"
source "venv/bin/activate"

# Install requirements
echo -e "${GREEN}Installing requirements...${NC}"
pip install --upgrade pip
pip install wheel
pip install -r "$PROJECT_ROOT/requirements.txt"

# Run tests
echo -e "${GREEN}Running tests...${NC}"
cd "$PROJECT_ROOT"
pytest "$PROJECT_ROOT/tests/"

echo -e "${GREEN}Setup complete!${NC}"
echo -e "${GREEN}To activate the virtual environment, run:${NC}"
echo -e "${GREEN}source venv/bin/activate${NC}" 
