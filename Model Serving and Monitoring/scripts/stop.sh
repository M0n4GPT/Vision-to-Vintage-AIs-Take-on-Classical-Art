#!/bin/bash

# Kill any running uvicorn processes
pkill -f "uvicorn serving.main:app"
