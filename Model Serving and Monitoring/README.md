# Vision to Vintage - AI Style Transfer

This application allows you to transform your photos using the style of classical artists. It uses a neural style transfer model to apply artistic styles to images, with proper monitoring and MLOps practices in place.

## Features

- **Style Transfer API**: Upload an image and apply an artistic style
- **Pre-defined Styles**: Choose from several classic artworks
- **Monitoring**: Prometheus metrics for API and model performance
- **Visualization**: Grafana dashboards to visualize metrics
- **Model Management**: MLflow for model tracking
- **Feedback Collection**: User feedback collection for model improvement

## Architecture

The application is structured as follows:

```
.
├── app/                     # FastAPI application
│   ├── templates/           # HTML templates
│   ├── Dockerfile           # FastAPI app container
│   └── main.py              # Main application
├── data/                    # Data directory
│   ├── metrics/             # Metrics storage
│   ├── production/          # Generated images
│   └── styles/              # Style images
├── model_management/        # Model management code
│   └── model_serving.py     # Model serving module
├── models/                  # Model files
│   └── model.pt             # Main model
├── monitoring/              # Monitoring modules
│   ├── scripts/             # Setup scripts
│   ├── grafana/             # Grafana config
│   ├── prometheus/          # Prometheus config
│   └── monitoring.py        # Monitoring module
├── tests/                   # Test files
├── docker-compose.yml       # Docker Compose config
├── requirements.txt         # Python dependencies
├── setup_styles.py          # Style setup script
├── start_services.sh        # Startup script
└── stop_services.sh         # Shutdown script
```

## Requirements

- Docker and Docker Compose
- Python 3.9+
- Style images in data/styles directory

## Setup and Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd Vision-to-Vintage
   ```

2. Add style images to the `data/styles` directory. Images should be named in the format:
   ```
   Artist_Name,Painting_Name.jpg
   ```
   For example: `Vincent_van_Gogh,Starry_Night.jpg`

3. Start the services:
   ```
   chmod +x start_services.sh
   ./start_services.sh
   ```

4. Access the web interface at http://localhost:8000

## Usage

1. Open your browser and navigate to http://localhost:8000
2. Browse available styles at http://localhost:8000/styles
3. Upload an image you want to transform
4. Enter the style ID from the styles page
5. Click "Transform Image" and wait for the result
6. Download your transformed image or provide feedback on the result

## Monitoring

- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (login: admin/admin)
- MLflow: http://localhost:5001
- MinIO: http://localhost:9001 (login: minioadmin/minioadmin)

## Development

### Local Development

To set up a local development environment:

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the FastAPI application:
   ```
   uvicorn app.main:app --reload
   ```

### Running Tests

```
pytest tests/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.