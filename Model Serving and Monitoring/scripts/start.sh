#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

# Function to check if a port is in use
port_in_use() {
    lsof -i:$1 >/dev/null 2>&1
    return $?
}

# Activate virtual environment
echo -e "${GREEN}Activating virtual environment...${NC}"
source "$PROJECT_ROOT/venv/bin/activate"

# Check if port 8000 is available
if port_in_use 8000; then
    echo -e "${RED}Error: Port 8000 is already in use${NC}"
    exit 1
fi

# Start the FastAPI server
echo -e "\n${GREEN}Starting Vision-to-Vintage API server...${NC}"

echo -e "\n${BLUE}📚 API Documentation:${NC}"
echo -e "${BLUE}• Interactive Swagger UI: ${NC}http://localhost:8000/docs"
echo -e "${BLUE}• ReDoc Documentation: ${NC}http://localhost:8000/redoc"

echo -e "\n${CYAN}🔗 Available Endpoints:${NC}"
echo -e "${CYAN}1. List Styles${NC}"
echo -e "   GET http://localhost:8000/styles"
echo -e "   Returns list of available style options"

echo -e "\n${CYAN}2. Transform Image${NC}"
echo -e "   POST http://localhost:8000/transform"
echo -e "   Parameters:"
echo -e "   - style_name (query parameter)"
echo -e "   - content_image (file upload)"

echo -e "\n${CYAN}3. Submit Evaluation${NC}"
echo -e "   POST http://localhost:8000/evaluate"
echo -e "   Body: JSON with ratings (0-10) and optional comment"
echo -e "   {
     \"style_accuracy\": 8,
     \"content_preservation\": 9,
     \"overall_quality\": 8,
     \"comment\": \"Great result!\"
   }"

echo -e "\n${CYAN}4. View Evaluations${NC}"
echo -e "   GET http://localhost:8000/evaluations"
echo -e "   Returns all submitted evaluations"

echo -e "\n${YELLOW}📸 Available Style Options:${NC}"
echo -e "${YELLOW}• starry_night ${NC}(Van Gogh's Starry Night)"
echo -e "${YELLOW}• mona_lisa ${NC}(Da Vinci's Mona Lisa)"
echo -e "${YELLOW}• the_scream ${NC}(Munch's The Scream)"
echo -e "${YELLOW}• girl_with_pearl_earring ${NC}(Vermeer's Girl with a Pearl Earring)"
echo -e "${YELLOW}• creation_of_adam ${NC}(Michelangelo's Creation of Adam)"
echo -e "${YELLOW}• le_reve ${NC}(Picasso's Le Reve)"
echo -e "${YELLOW}• composition ${NC}(Mondrian's Composition in Red, Blue, and Yellow)"
echo -e "${YELLOW}• dance ${NC}(Matisse's Dance)"
echo -e "${YELLOW}• odalisque ${NC}(Ingres' La Grande Odalisque)"
echo -e "${YELLOW}• impression_sunrise ${NC}(Monet's Impression Sunrise)"

echo -e "\n${GREEN}💡 Quick Start:${NC}"
echo -e "1. Visit ${BLUE}http://localhost:8000/docs${NC} for interactive API testing"
echo -e "2. Use the /styles endpoint to see available styles"
echo -e "3. Upload an image with your chosen style using /transform"
echo -e "4. Rate the result using /evaluate"

echo -e "\n${GREEN}Starting server...${NC}"
cd "$PROJECT_ROOT" && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
