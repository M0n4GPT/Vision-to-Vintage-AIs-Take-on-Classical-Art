# Vision-to-Vintage API

A FastAPI-based service for AI-powered classical art style transfer with monitoring capabilities.

## Project Structure

```
Model Serving/
├── app/                      # Application code
│   ├── core/                # Core functionality
│   │   ├── models/         # Model-related code
│   │   ├── monitoring/     # Monitoring and drift detection
│   │   └── utils/          # Utility functions
│   └── api/                # API endpoints
├── config/                  # Configuration files
│   ├── docker/             # Docker-related configs
│   └── monitoring/         # Monitoring configs
├── data/                    # Data storage
│   ├── reference/          # Reference data for drift detection
│   ├── metrics/            # Metrics storage
│   └── styles/             # Style images
├── scripts/                 # Utility scripts
│   ├── setup.sh            # Setup script
│   ├── start.sh            # Start script
│   └── stop.sh             # Stop script
├── tests/                   # Test files
├── docker-compose.yml       # Main Docker compose file
├── requirements.txt         # Python dependencies
└── README.md               # Project documentation
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run setup script:
```bash
./scripts/setup.sh
```

3. Start the service:
```bash
./scripts/start.sh
```

## API Endpoints

- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint
- `GET /metrics` - Prometheus metrics endpoint
- `GET /drift-dashboard` - Drift monitoring dashboard
- `POST /transform` - Transform an image with a style

## Monitoring

The service includes:
- Prometheus metrics
- Drift detection
- Real-time monitoring dashboard

## Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

2. Install development dependencies:
```bash
pip install -r requirements.txt
```

3. Run tests:
```bash
pytest tests/
```

## License

MIT License 