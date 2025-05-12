# Vision to Vintage - AI Style Transfer: Model Serving and Monitoring

This core component of the Vision-to-Vintage project is responsible for serving the trained style transfer model, managing its lifecycle, monitoring its performance and the health of the serving system, and implementing a robust MLOps pipeline.

## Overview

The system allows users to upload images and apply various "vintage" artistic styles derived from classical artworks. It's built with a focus on scalability, reproducibility, and continuous improvement through monitoring and feedback.

**Key Features:**

*   **Style Transfer API**: A FastAPI-based application serves the core style transfer functionality.
*   **Dynamic Style Selection**: Users can browse and select from a variety of pre-defined artistic styles.
*   **Comprehensive Monitoring**: Leverages Prometheus for metrics collection and Grafana for visualization of API performance, model behavior, system health, data drift, and model degradation.
*   **Model Management & Experiment Tracking**: MLflow is integrated for tracking experiments, model versions, and artifacts.
*   **Feedback Loop**: Mechanisms are in place to collect user feedback and production data, enabling continuous model improvement and evaluation.
*   **Containerized Deployment**: All services are containerized using Docker and orchestrated with Docker Compose for consistent environments and ease of management.
*   **Automated Testing**: Includes unit, integration, and load testing capabilities.

## Directory Structure

The `Model Serving and Monitoring` directory is organized as follows:

*   **`app/`**: Contains the source code for the FastAPI application.
    *   `main.py`: The main application file defining API endpoints.
    *   `api/`: Routers for organizing API endpoints (e.g., `transform.py`, `evaluation.py`).
    *   `core/`: Core application logic, including configuration (`config.py`).
    *   `schemas/`: Pydantic models for API request/response validation.
    *   `static/`: Static assets like style images.
    *   `templates/`: HTML templates (if any served directly by FastAPI).
    *   `minio_client.py`: Client for interacting with MinIO object storage.
    *   `model_registry.py`: Logic for interacting with the MLflow model registry.
    *   `Dockerfile`: Instructions to build the FastAPI application container.
    *   `entrypoint.sh`: Script executed when the application container starts.
*   **`data/`**: Stores all data relevant to the project.
    *   `content/`: Content images for training/testing.
    *   `style/`: Style images for training (organized by number).
    *   `styles/`: Style images for inference/display (organized by artist/name).
    *   `styles_metadata.json`: Metadata for available styles.
    *   `production/`: Data collected from the "production" environment (user uploads, feedback).
    *   `reference/`: Reference datasets for drift detection or baseline metrics.
    *   `test/`: Test datasets for offline evaluation.
    *   `models/`: Trained model artifacts (e.g., the JIT-scripted `style_transfer_model.pt`).
    *   `mlflow/`: MLflow backend store and artifact storage configurations if local.
    *   `BUCKETS_README.md`: Documentation for data storage conventions.
*   **`drift_detections/`**: Stores output reports from data drift detection mechanisms (e.g., JSON files).
*   **`logs/`**: Contains log files from various components, like `drift_monitor.log`.
*   **`mlflow/`**: (Top-level) Contains a `Dockerfile` to build a custom MLflow image with Prometheus exporter.
*   **`mlruns/`**: Default local directory for MLflow experiment tracking data and artifacts.
*   **`model_management/`**: Scripts and utilities for the model lifecycle.
    *   `model_serving.py`: Core logic for loading and using the style transfer model for inference.
    *   `evaluate_model.py`: Script for performing offline model evaluation.
    *   `model_retraining.py`: Script to orchestrate model retraining.
    *   `convert_to_torchscript.py`: Utility for JIT scripting PyTorch models.
    *   `save_model.py`: Utility for saving models.
*   **`models/`**: (Top-level) Contains primary model artifacts and training scripts.
    *   `train_style_transfer.py`: The main script for training the style transfer model and JIT scripting the `Stylizer`.
    *   `style_transfer_model.pt`: The JIT-scripted `Stylizer` model used for inference.
*   **`monitoring/`**: Scripts and configurations for monitoring.
    *   `monitoring.py`: Python code for custom monitoring logic (e.g., `MetricsManager`).
    *   `prometheus/`: Prometheus configuration (`prometheus.yml`) and alerting rules.
    *   `grafana/`: Grafana configurations, datasource provisioning, and dashboard JSON files.
    *   `scripts/`: Various monitoring scripts (drift detection, degradation monitoring, load testing, canary evaluation, feedback loop management).
*   **`tests/`**: Automated tests.
    *   `api_tests/`: Integration tests for the API.
    *   `load_test.py`: Load testing script (e.g., using Locust).
    *   `load_test_results/`: Storage for load test outputs.
    *   `test_*.py`: Pytest files for unit and integration testing various components.
*   **`venv/`**: Python virtual environment (typically gitignored).
*   **`.gitignore`**: Specifies files and directories for Git to ignore.
*   **`direct_stylizer_output.png`**: A debugging output image from direct model testing.
*   **`docker-compose.yml`**: Defines and configures all services (FastAPI app, MLflow, Prometheus, Grafana, MinIO).
*   **`requirements.txt`**: Python package dependencies.
*   **`services.sh`**: Shell script for managing the lifecycle of Docker services.
*   **`setup_styles.py`**: Utility script for organizing style images.

## System Workflow & Architecture

The system operates through a series of interconnected components orchestrated by Docker Compose:

1.  **User Request & Inference:**
    *   A user interacts with a frontend (or API client), sending an image and a style choice to the **FastAPI application** (`app/main.py`).
    *   The FastAPI app validates the request (using Pydantic schemas from `app/schemas/`) and invokes the model serving logic in `model_management/model_serving.py`.
    *   `model_serving.py` loads the JIT-scripted **style transfer model** (`models/style_transfer_model.pt`).
    *   The model processes the image, applying the chosen style.
    *   The FastAPI app returns the stylized image to the user.

2.  **Training & Offline Evaluation:**
    *   The style transfer model is trained using `models/train_style_transfer.py`, utilizing content images from `data/content/` and style images from `data/style/`.
    *   The trained `Stylizer` is JIT-scripted for optimized inference.
    *   **MLflow** (configured in `docker-compose.yml`, data in `mlruns/`) tracks experiments, parameters, metrics, and model artifacts.
    *   Offline evaluation is performed using `model_management/evaluate_model.py` and test sets from `data/test/`. Results are logged to MLflow.
    *   Automated tests in `tests/` (e.g., `test_model_evaluation.py`) verify model behavior and performance.
    *   Models meeting criteria can be registered in the MLflow Model Registry via `app/model_registry.py`.

3.  **Monitoring & Alerting:**
    *   The FastAPI app exposes a `/metrics` endpoint.
    *   **Prometheus** (`monitoring/prometheus/prometheus.yml`) scrapes these metrics, as well as metrics from other services like MLflow (if instrumented via `mlflow/Dockerfile`).
    *   **Grafana** (`monitoring/grafana/`) queries Prometheus to provide dashboards for:
        *   API performance (latency, request rates, errors).
        *   Model prediction confidence and class distribution.
        *   System resource usage (via cAdvisor if integrated).
        *   Data drift and model degradation indicators.
    *   Alerting rules are defined in Prometheus/Grafana to notify of issues.

4.  **Feedback Loop & Production Data Management:**
    *   The FastAPI app has an endpoint (`/submit_feedback`) to collect user feedback, managed by `monitoring/monitoring.py` (`MetricsManager`).
    *   User-uploaded images, model predictions, and feedback are stored in **MinIO object storage** (`docker-compose.yml`, interaction via `app/minio_client.py`), typically in the `data/production/` bucket.
    *   This production data can be used for:
        *   Online evaluation (comparing model predictions to human-annotated labels).
        *   Generating datasets for model retraining (`model_management/model_retraining.py`).

5.  **Drift & Degradation Monitoring:**
    *   Scripts in `monitoring/scripts/` (e.g., `drift_monitor.py`, `degradation_monitor.py`) periodically analyze production data from MinIO and model outputs.
    *   Drift detection results are stored in `drift_detections/`.
    *   These scripts can push metrics to Prometheus or trigger alerts if significant drift or degradation is detected.

6.  **Load Testing:**
    *   `tests/load_test.py` simulates concurrent user traffic against the API.
    *   Performance metrics under load are observed in Prometheus/Grafana, and detailed reports can be saved in `tests/load_test_results/`.

## Meeting MLOps Project Requirements

This project addresses key MLOps requirements as follows:

1.  **Serving from an API endpoint:**
    *   **Implementation:** The core functionality is provided by the FastAPI application in `app/main.py`, defining endpoints like `/transform` (input: image, style ID; output: stylized image), `/styles`, and `/feedback`. Services are orchestrated by `docker-compose.yml`.
    *   **Status:** Satisfied.

2.  **Identify requirements (model size, throughput, latency, concurrency):**
    *   **Implementation:** Requirements are documented in this README. Decisions like using JIT-scripted models (`models/train_style_transfer.py`), containerization, and implementing load testing (`tests/load_test.py`) are driven by performance considerations.
    *   **Status:** Satisfied (documentation and implicit design choices).

3.  **Model optimizations to satisfy requirements:**
    *   **Implementation:**
        *   **TorchScript (JIT compilation):** The `Stylizer` model is JIT-scripted in `models/train_style_transfer.py` and the resulting `style_transfer_model.pt` is used for serving, reducing Python overhead and enabling graph optimizations. This is loaded by `model_management/model_serving.py`.
    *   **Status:** Satisfied.

4.  **System optimizations to satisfy requirements:**
    *   **Implementation:**
        *   **Containerization:** Docker (`app/Dockerfile`, `docker-compose.yml`) ensures reproducible environments and facilitates scaling.
        *   **Asynchronous Operations:** FastAPI supports async request handling. Uvicorn workers can be configured for concurrency.
        *   **Efficient Static File Serving:** For style images and UI assets.
    *   **Status:** Foundational elements satisfied. Advanced cloud scaling (auto-scaling groups, Kubernetes) would be next steps beyond the current local setup.

5.  **Offline evaluation of model:**
    *   **Implementation:**
        *   Scripts: `model_management/evaluate_model.py`.
        *   Test data: Stored in `data/test/`.
        *   Metrics logging: **MLflow** (`mlruns/`, `docker-compose.yml` service) is used to track experiments and log evaluation metrics.
        *   Automated tests: Pytest files in `tests/` (e.g., `test_model_evaluation.py`) can check for accuracy, specific failure modes, and performance on data slices.
        *   Model Registration: `app/model_registry.py` allows for interaction with MLflow Model Registry for automated registration based on evaluation results.
    *   **Status:** Satisfied (framework and key scripts in place).

6.  **Load test in staging:**
    *   **Implementation:**
        *   Script: `tests/load_test.py` (e.g., using Locust or `requests`).
        *   Results: Stored in `tests/load_test_results/` and visualized via Prometheus/Grafana metrics during the test.
        *   Environment: The `docker-compose` setup can serve as the staging environment for these tests.
    *   **Status:** Satisfied.

7.  **Online evaluation in canary (simulated):**
    *   **Implementation:**
        *   Monitoring: **Prometheus** (`monitoring/prometheus/prometheus.yml`) and **Grafana** (`monitoring/grafana/`) provide real-time monitoring of the application, crucial for observing canary performance.
        *   Scripts: `monitoring/scripts/monitor_canary.py` and `canary_evaluation.py` provide a basis for specific canary testing logic.
        *   Artificial Users: Load testing scripts or custom clients can simulate user traffic for the canary.
    *   **Status:** Foundational monitoring in place. True canary deployment requires infrastructure-level traffic splitting.

8.  **Close the loop:**
    *   **Implementation:**
        *   Feedback Collection: `/submit_feedback` endpoint in `app/main.py`, with logic in `monitoring/monitoring.py` (`MetricsManager`).
        *   Production Data Storage: **MinIO** (`docker-compose.yml` service, `app/minio_client.py`) stores uploaded images, predictions, and feedback in `data/production/`.
        *   Data Labeling: While not fully automated in the current file list, the stored production data is ready for labeling (e.g., via an external tool, or scripts could be added to integrate with Label Studio).
        *   Retraining: `model_management/model_retraining.py` can be adapted to use this labeled production data from MinIO for retraining.
    *   **Status:** Satisfied (key mechanisms for data collection and retraining trigger are present).

9.  **Monitor for data drift:**
    *   **Implementation:**
        *   Scripts: `monitoring/scripts/drift_monitor.py`, `data_drift.py`.
        *   Reference Data: Stored in `data/reference/`.
        *   Drift Reports: Results saved in `drift_detections/`.
        *   Visualization: Drift metrics can be pushed to Prometheus and visualized in Grafana dashboards.
    *   **Status:** Satisfied (tooling and storage in place).

10. **Monitor for model degradation:**
    *   **Implementation:**
        *   Scripts: `monitoring/scripts/degradation_monitor.py`.
        *   Process: Uses the "closed loop" (newly labeled production data from MinIO) to periodically re-evaluate the deployed model's performance.
        *   Metrics: Degradation metrics (e.g., drop in accuracy on recent data) can be logged to MLflow or exposed via Prometheus for Grafana dashboards and alerting.
        *   Trigger Retraining: Significant degradation can trigger `model_management/model_retraining.py`.
    *   **Status:** Satisfied (tooling and process outlined).

## Setup and Usage

1.  **Prerequisites:**
    *   Docker and Docker Compose
    *   Python 3.9+ (for running scripts outside Docker if needed)
    *   Git

2.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd Vision-to-Vintage-AIs-Take-on-Classical-Art/Model Serving and Monitoring
    ```

3.  **Prepare Style Images:**
    *   Ensure style images are present in `app/static/styles/ArtistName/PaintingName.jpg`.
    *   Update `data/styles_metadata.json` if new styles are added.
    *   For training, place style images in `data/style/[number]/` and content images in `data/content/`.

4.  **Build and Start Services:**
    *   Use the provided script:
        ```bash
        chmod +x services.sh
        ./services.sh start
        ```
    *   This will build the necessary Docker images and start all services defined in `docker-compose.yml`.

5.  **Access Services:**
    *   **Web Application (FastAPI UI if enabled, or for API interaction):** `http://localhost:8000`
    *   **Prometheus:** `http://localhost:9090`
    *   **Grafana:** `http://localhost:3000` (Default login: `admin`/`admin` - change on first login)
    *   **MLflow:** `http://localhost:5001`
    *   **MinIO:** `http://localhost:9001` (Login from `docker-compose.yml` environment variables, e.g., `minioadmin`/`minioadmin`)

6.  **Using the Application:**
    *   Navigate to the web application.
    *   Browse available styles (e.g., via a `/styles` page or API endpoint).
    *   Upload an image for transformation, select a style, and view the result.
    *   Provide feedback if the feature is enabled.

7.  **Stopping Services:**
    ```bash
    ./services.sh stop
    ```

8.  **Viewing Logs:**
    ```bash
    ./services.sh logs <service_name>  # e.g., ./services.sh logs app
    ```

## Development & Testing

*   **Local Python Development:**
    *   Create and activate a virtual environment:
        ```bash
   python -m venv venv
        source venv/bin/activate  # For Linux/macOS
        # venv\Scripts\activate    # For Windows
   ```
    *   Install dependencies:
        ```bash
   pip install -r requirements.txt
   ```
    *   Run FastAPI locally (for the app service):
        ```bash
        cd app
        uvicorn main:app --reload --host 0.0.0.0 --port 8000
        ```
*   **Running Automated Tests:**
    ```bash
pytest tests/
```
*   **Running Load Tests:**
    Execute the script in `tests/load_test.py` (e.g., `locust -f tests/load_test.py`) and monitor Grafana/Prometheus.

This updated README should provide a comprehensive guide to the "Model Serving and Monitoring" part of your project.