#!/bin/bash

# Vision to Vintage - Consolidated Services Script
# This script handles starting, stopping, monitoring, and testing services.

# Define project name for Docker Compose
COMPOSE_PROJECT_NAME="visiontovintage"

# Define all ports used by our services
APP_PORT=8000
MINIO_API_PORT=9000
MINIO_CONSOLE_PORT=9001
MLFLOW_PORT=5000
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000

# Color output function
print_message() {
    COLOR=$1
    MESSAGE=$2
    case $COLOR in
        "green") echo -e "\033[0;32m${MESSAGE}\033[0m" ;;
        "yellow") echo -e "\033[0;33m${MESSAGE}\033[0m" ;;
        "red") echo -e "\033[0;31m${MESSAGE}\033[0m" ;;
        "blue") echo -e "\033[0;34m${MESSAGE}\033[0m" ;;
        *) echo "${MESSAGE}" ;;
    esac
}

# Function to check for port conflicts and resolve them
check_port_conflicts() {
    print_message "yellow" "Checking for port conflicts..."
    
    # Define all ports to check - using simple arrays instead of associative array
    PORT_NAMES=("APP_PORT" "MINIO_API_PORT" "MINIO_CONSOLE_PORT" "MLFLOW_PORT" "PROMETHEUS_PORT" "GRAFANA_PORT")
    PORT_VALUES=($APP_PORT $MINIO_API_PORT $MINIO_CONSOLE_PORT $MLFLOW_PORT $PROMETHEUS_PORT $GRAFANA_PORT)
    
    # Array to track if we found any conflicts
    CONFLICTS_FOUND=false
    
    # Check each port
    for i in "${!PORT_NAMES[@]}"; do
        PORT_NAME=${PORT_NAMES[$i]}
        PORT=${PORT_VALUES[$i]}
        CONFLICT=$(docker ps -q --filter "publish=$PORT")
        
        if [ -n "$CONFLICT" ]; then
            CONFLICTS_FOUND=true
            print_message "red" "Port $PORT ($PORT_NAME) is used by container(s): $(docker ps --filter "publish=$PORT" --format '{{.Names}} ({{.ID}})')"
            
            # Automatically stop the conflicting containers
            for container in $(docker ps -q --filter "publish=$PORT"); do
                print_message "yellow" "Stopping container ${container} using port $PORT..."
                docker stop ${container}
            done
        fi
    done
    
    if [ "$CONFLICTS_FOUND" = false ]; then
        print_message "green" "No Docker container port conflicts detected."
    fi
    
    # Check for non-Docker processes using these ports (just provide info)
    print_message "yellow" "Checking for other processes using ports..."
    
    # This part is informational only as it would require sudo
    print_message "blue" "If container stops did not resolve conflicts, check for other processes:"
    for i in "${!PORT_NAMES[@]}"; do
        PORT_NAME=${PORT_NAMES[$i]}
        PORT=${PORT_VALUES[$i]}
        print_message "blue" "sudo lsof -i :$PORT  # For $PORT_NAME"
    done
}

# Function to stop all services
stop_services() {
    echo "Stopping all services for project '$COMPOSE_PROJECT_NAME'..."
    # Try to bring down compose services first
    if docker compose --project-name "$COMPOSE_PROJECT_NAME" ps -q | grep -q .; then
        # Added --volumes for a cleaner slate, though not the primary fix for name conflict
        docker compose --project-name "$COMPOSE_PROJECT_NAME" down --remove-orphans --volumes
        if [ $? -ne 0 ]; then
            echo "Warning: 'docker compose down' encountered an issue, but continuing."
        fi
    else
        echo "No running services found for project '$COMPOSE_PROJECT_NAME' to stop with compose."
    fi

    # Explicitly stop and remove known fixed-name containers that might conflict
    # (like one named exactly 'mlflow' if started manually or by a different compose setup)
    # These are potential raw container names, not necessarily service names from compose.
    local fixed_conflict_names=("mlflow" "grafana" "prometheus" "minio" "app") 
    for name in "${fixed_conflict_names[@]}"; do
        local target_container_id
        # Check for container name possibly prefixed with / or not
        target_container_id=$(docker ps -a --filter "name=^/${name}$" --format "{{.ID}}" | head -n 1)
        if [ -z "$target_container_id" ]; then
            target_container_id=$(docker ps -a --filter "name=^${name}$" --format "{{.ID}}" | head -n 1)
        fi

        if [ -n "$target_container_id" ]; then
            echo "Found potentially conflicting fixed-name container matching '$name' (ID: $target_container_id). Attempting to stop and remove..."
            if ! docker stop "$target_container_id" ; then
                echo "Warning: Failed to stop container $name (ID: $target_container_id). It might be already stopped."
            fi
            
            if ! docker rm "$target_container_id" ; then
                echo "Warning: Failed to remove container $name (ID: $target_container_id). Attempting force remove..."
                if ! docker rm -f "$target_container_id" ; then
                    echo "ERROR: Failed to force remove container $name (ID: $target_container_id). This WILL LIKELY cause 'docker compose up' to fail."
                    # You might want to exit here if this is critical: exit 1
                else
                    echo "Successfully force removed container $name (ID: $target_container_id)."
                fi
            else
                echo "Successfully stopped and removed container $name (ID: $target_container_id)."
            fi
        fi
    done

    check_port_conflicts
}

# Function to start all services
start_services() {
    # Stop any existing services first to avoid conflicts
    stop_services
    
    print_message "yellow" "Building Docker images (if necessary)..."
    docker-compose -p "${COMPOSE_PROJECT_NAME}" build
    
    print_message "yellow" "Starting all services in detached mode..."
    docker-compose -p "${COMPOSE_PROJECT_NAME}" up -d
    
    print_message "green" "Services started. Current status:"
    docker-compose -p "${COMPOSE_PROJECT_NAME}" ps
    
    # Display service access URLs
    print_message "green" "\nAccess services at:"
    MAIN_APP_PORT=$(docker-compose -p "${COMPOSE_PROJECT_NAME}" port app $APP_PORT 2>/dev/null | cut -d ':' -f2)
    MINIO_API_PORT_MAPPED=$(docker-compose -p "${COMPOSE_PROJECT_NAME}" port minio $MINIO_API_PORT 2>/dev/null | cut -d ':' -f2)
    MINIO_CONSOLE_PORT_MAPPED=$(docker-compose -p "${COMPOSE_PROJECT_NAME}" port minio $MINIO_CONSOLE_PORT 2>/dev/null | cut -d ':' -f2)
    MLFLOW_PORT_MAPPED=$(docker-compose -p "${COMPOSE_PROJECT_NAME}" port mlflow $MLFLOW_PORT 2>/dev/null | cut -d ':' -f2)
    PROMETHEUS_PORT_MAPPED=$(docker-compose -p "${COMPOSE_PROJECT_NAME}" port prometheus $PROMETHEUS_PORT 2>/dev/null | cut -d ':' -f2)
    GRAFANA_PORT_MAPPED=$(docker-compose -p "${COMPOSE_PROJECT_NAME}" port grafana $GRAFANA_PORT 2>/dev/null | cut -d ':' -f2)
    
    echo "--------------------------------------------------"
    [ -n "$MAIN_APP_PORT" ] && echo "Vision to Vintage API: http://localhost:${MAIN_APP_PORT}"
    [ -n "$MINIO_API_PORT_MAPPED" ] && echo "MinIO API:             http://localhost:${MINIO_API_PORT_MAPPED}"
    [ -n "$MINIO_CONSOLE_PORT_MAPPED" ] && echo "MinIO Console:         http://localhost:${MINIO_CONSOLE_PORT_MAPPED} (User: minioadmin, Pass: minioadmin)"
    [ -n "$MLFLOW_PORT_MAPPED" ] && echo "MLflow UI:             http://localhost:${MLFLOW_PORT_MAPPED}"
    [ -n "$PROMETHEUS_PORT_MAPPED" ] && echo "Prometheus UI:         http://localhost:${PROMETHEUS_PORT_MAPPED}"
    [ -n "$GRAFANA_PORT_MAPPED" ] && echo "Grafana UI:            http://localhost:${GRAFANA_PORT_MAPPED} (User: admin, Pass: admin)"
    echo "--------------------------------------------------"
    
    # Check if we have any failed containers
    FAILED_SERVICES=$(docker-compose -p "${COMPOSE_PROJECT_NAME}" ps --services --filter "status=exited" 2>/dev/null)
    if [ -n "$FAILED_SERVICES" ]; then
        print_message "red" "\nWARNING: Some services failed to start. Check logs for details:"
        for service in $FAILED_SERVICES; do
            print_message "red" "  - $service"
            print_message "blue" "    To see logs: docker-compose -p ${COMPOSE_PROJECT_NAME} logs $service"
        done
    fi
    
    print_message "yellow" "\nServices are running in the background."
    print_message "yellow" "To view app logs: ./services.sh logs"
    print_message "yellow" "To stop services: ./services.sh stop"
}

# Function to display logs
show_logs() {
    print_message "yellow" "Following logs for the 'app' service. Press Ctrl+C to detach from logs (services will continue running)."
    
    # Trap Ctrl+C during logs to just print a message and exit the log follow, not stop services
    trap 'echo -e "\nDetached from app logs. Services are still running."; exit 0' INT
    docker-compose -p "${COMPOSE_PROJECT_NAME}" logs -f app
}

# Function to run tests
run_tests() {
    print_message "yellow" "Running tests..."
    
    # First check if services are running
    SERVICE_COUNT=$(docker-compose -p "${COMPOSE_PROJECT_NAME}" ps -q | wc -l)
    if [ "$SERVICE_COUNT" -eq 0 ]; then
        print_message "red" "No services are running. Please start services first with: ./services.sh start"
        exit 1
    fi
    
    # Run API tests using curl
    echo "Testing API health..."
    MAIN_APP_PORT=$(docker-compose -p "${COMPOSE_PROJECT_NAME}" port app $APP_PORT 2>/dev/null | cut -d ':' -f2)
    if [ -z "$MAIN_APP_PORT" ]; then
        print_message "red" "App service is not running or port mapping failed."
        exit 1
    fi
    
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:${MAIN_APP_PORT}/health)
    if [ "$HTTP_STATUS" -eq 200 ]; then
        print_message "green" "API health check: OK (200)"
    else
        print_message "red" "API health check failed: ${HTTP_STATUS}"
    fi
    
    # Test styles API
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:${MAIN_APP_PORT}/api/styles)
    if [ "$HTTP_STATUS" -eq 200 ]; then
        print_message "green" "Styles API: OK (200)"
    else
        print_message "red" "Styles API failed: ${HTTP_STATUS}"
    fi
    
    # Run additional monitoring tests here...
    print_message "green" "Tests completed."
}

# Function to monitor resources
monitor_resources() {
    print_message "yellow" "Monitoring Docker resources..."
    
    # Summary of running containers
    print_message "blue" "Container Overview:"
    docker stats --no-stream
    
    # More detailed resource info
    print_message "blue" "\nDetailed Container Stats (Press Ctrl+C to exit):"
    docker stats
}

# Function to clean up old duplicate script files
cleanup_old_scripts() {
    print_message "yellow" "Checking for old script files..."
    
    # List of old scripts that should be removed/renamed
    DEPRECATED_SCRIPTS=(
        "start_services.sh"
        "stop_services.sh"
        "monitoring/scripts/services.sh"
        "monitoring/scripts/test.sh"
        "monitoring/monitor.sh"
    )
    
    for script in "${DEPRECATED_SCRIPTS[@]}"; do
        if [ -f "$script" ]; then
            print_message "yellow" "Found old script: $script"
            print_message "yellow" "Renaming to ${script}.bak"
            mv "$script" "${script}.bak"
        fi
    done
    
    print_message "green" "Cleanup completed."
}

# Function to regenerate the style transfer model
regenerate_model() {
    print_message "yellow" "Regenerating the style transfer model (models/model.pt)..."
    print_message "blue" "This will use styles from 'data/styles/' to create the Stylizer model."
    print_message "blue" "The training loop for the base StyleTransferModel decoder will be SKIPPED."

    # Define paths relative to the script's location (assuming it's in Model Serving and Monitoring)
    local script_dir
    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
    local model_script_path="${script_dir}/models/train_style_transfer.py"
    local style_dir_for_stylizer_path="${script_dir}/data/styles"
    local export_model_path="${script_dir}/models/model.pt"
    # Data root for the training script (needed for dataset init, even if training loop is skipped for content dir check)
    # Point it to a directory that exists, e.g., the main data directory.
    # The script's StyleTransferDataset expects data_root/content and data_root/style/0,1,2...
    # Since run_training_loop=False, these specific training subdirs are not strictly needed for Stylizer export.
    local data_root_path="${script_dir}/data"

    if [ ! -f "$model_script_path" ]; then
        print_message "red" "ERROR: Model training script not found at $model_script_path"
        exit 1
    fi
    if [ ! -d "$style_dir_for_stylizer_path" ]; then
        print_message "red" "ERROR: Style directory for Stylizer not found at $style_dir_for_stylizer_path"
        exit 1
    fi
    
    # Create a dummy content directory if it doesn't exist, as StyleTransferDataset expects it
    local dummy_content_dir="${data_root_path}/content"
    if [ ! -d "$dummy_content_dir" ]; then
        print_message "yellow" "Dummy content directory for training script not found at $dummy_content_dir. Creating it."
        mkdir -p "$dummy_content_dir"
        # You might want to add a dummy image here if the script strictly requires one, e.g.:
        # touch "${dummy_content_dir}/dummy_content.jpg"
    fi
    # Also, StyleTransferDataset expects data_root/style with 0,1,2... subdirs. We can create a dummy one.
    local dummy_training_style_dir="${data_root_path}/style"
    if [ ! -d "$dummy_training_style_dir" ]; then
        print_message "yellow" "Dummy style directory for training script not found at $dummy_training_style_dir. Creating it."
        mkdir -p "$dummy_training_style_dir"
        # mkdir -p "${dummy_training_style_dir}/0"
        # touch "${dummy_training_style_dir}/0/dummy_style.jpg"
    fi

    print_message "yellow" "Executing model regeneration script..."
    # Ensure python environment can find torch, etc. This might need venv activation if not run in a pre-configured env.
    # For simplicity, assuming python3 is available and has necessary packages.
    python3 "$model_script_path" \
        --data_root "$data_root_path" \
        --style_dir_for_stylizer "$style_dir_for_stylizer_path" \
        --export_path "$export_model_path" \
        --epochs 1 \
        --global_batch_size 2 \
        --micro_batch_size 1
        # Add other args as needed, but run_training_loop=False in script bypasses most training ones

    if [ $? -eq 0 ]; then
        print_message "green" "Model regeneration script completed. New model should be at $export_model_path"
    else
        print_message "red" "ERROR: Model regeneration script failed. Check output above."
        exit 1
    fi
}

# Display usage information
show_usage() {
    echo "Usage: $0 [command]"
    echo "Commands:"
    echo "  start     - Start all services (stops existing services first)"
    echo "  stop      - Stop all services"
    echo "  logs      - View application logs"
    echo "  test      - Run basic API tests"
    echo "  monitor   - Monitor system resources"
    echo "  cleanup   - Rename old script files (with .bak extension)"
    echo "  regenerate - Regenerate the style transfer model"
    echo "  help      - Show this help message"
}

# Main logic
if [ $# -eq 0 ]; then
    # Default to start if no arguments
    start_services
else
    case "$1" in
        start)
            start_services
            ;;
        stop)
            stop_services
            ;;
        logs)
            show_logs
            ;;
        test)
            run_tests
            ;;
        monitor)
            monitor_resources
            ;;
        cleanup)
            cleanup_old_scripts
            ;;
        regenerate)
            regenerate_model
            ;;
        *)
            show_usage
            ;;
    esac
fi 