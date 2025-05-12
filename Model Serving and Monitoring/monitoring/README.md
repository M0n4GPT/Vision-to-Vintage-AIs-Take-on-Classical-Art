# Model Monitoring System

## Overview
This directory contains the complete monitoring infrastructure for the model serving system, including:
- Performance monitoring
- Data drift detection
- Model degradation tracking
- Automatic retraining triggers

## Components

### 1. Prometheus Metrics
- Model inference latency
- Request throughput
- Error rates
- Resource utilization

### 2. Grafana Dashboards
- Real-time performance metrics
- Data drift visualization
- Model quality metrics
- System health monitoring

### 3. Drift Detection
- Statistical tests for data drift
- Distribution comparison
- Feature importance tracking
- Label drift monitoring

### 4. Automated Retraining
- Performance degradation triggers
- Data drift thresholds
- Scheduled retraining
- Model versioning

## Setup Instructions
1. Start the monitoring stack:
```bash
./start_monitoring.sh
```

2. Access dashboards:
- Grafana: http://localhost:3000
- Prometheus: http://localhost:9090

## Configuration
- `prometheus/prometheus.yml`: Metrics collection settings
- `grafana/dashboards/`: Dashboard definitions
- `scripts/`: Monitoring utility scripts

## Alerting
- Performance degradation alerts
- Data drift notifications
- System health warnings
- Resource utilization alerts

## Directory Structure

```
monitoring/
├── docker-compose.yml
├── grafana/
│   ├── Dockerfile
│   ├── grafana.ini
│   └── provisioning/
│       ├── dashboards/
│       │   ├── dashboards.yml
│       │   └── style_transfer.json
│       └── datasources/
│           └── prometheus.yml
├── prometheus/
│   ├── Dockerfile
│   └── prometheus.yml
├── README.md
└── start_monitoring.sh
```

## Getting Started

1. Make sure you have Docker and Docker Compose installed
2. Run the start script:
   ```bash
   ./start_monitoring.sh
   ```
3. Access the services:
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3000 (admin/admin)

## Dashboards

The following dashboards are available in Grafana:

1. **Model Inference Latency**: Shows the average inference latency over time
2. **System Resource Usage**: Displays CPU and memory usage
3. **Model Quality Metrics**: Tracks style accuracy, content preservation, and overall quality scores
4. **Data Drift and Model Health**: Monitors data drift and model quality scores

## Metrics

The following metrics are collected:

### Model Metrics
- `model_inference_latency_seconds`: Inference latency in seconds
- `model_style_accuracy_score`: Style accuracy score (0-1)
- `model_content_preservation_score`: Content preservation score (0-1)
- `model_overall_quality_score`: Overall quality score (0-1)
- `model_data_drift_score`: Data drift score (0-1)
- `model_quality_score`: Model quality score (0-1)

### System Metrics
- `system_cpu_usage_percent`: CPU usage percentage
- `system_memory_usage_bytes`: Memory usage in bytes

## Configuration

### Prometheus
- Configuration file: `prometheus/prometheus.yml`
- Scrape interval: 15 seconds
- Evaluation interval: 15 seconds

### Grafana
- Configuration file: `grafana/grafana.ini`
- Default credentials: admin/admin
- Dashboard refresh interval: 5 seconds

## Maintenance

### Updating Dashboards
1. Export the dashboard from Grafana UI
2. Save the JSON to `grafana/provisioning/dashboards/style_transfer.json`
3. Restart the Grafana container

### Adding New Metrics
1. Add the metric to the Prometheus configuration
2. Update the Grafana dashboard to visualize the new metric
3. Restart the monitoring stack

## Troubleshooting

### Common Issues

1. **Prometheus not starting**
   - Check if port 9090 is available
   - Verify the prometheus.yml configuration

2. **Grafana not starting**
   - Check if port 3000 is available
   - Verify the grafana.ini configuration

3. **No metrics showing**
   - Check if the style transfer service is running
   - Verify the Prometheus targets are up
   - Check the scrape configuration

### Logs

View container logs:
```bash
# Prometheus logs
docker-compose logs prometheus

# Grafana logs
docker-compose logs grafana
```

## Security

- Default Grafana credentials should be changed in production
- Prometheus and Grafana are not exposed to the internet by default
- Consider setting up authentication for Prometheus in production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 