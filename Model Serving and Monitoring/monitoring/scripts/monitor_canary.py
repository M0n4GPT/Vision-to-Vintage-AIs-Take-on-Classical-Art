import os
import time
import json
import logging
import requests
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from prometheus_api_client import PrometheusConnect
import mlflow
from prometheus_client import push_to_gateway, Counter, Gauge, Histogram
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Prometheus metrics
canary_alerts = Counter(
    'canary_alerts_total',
    'Total number of canary alerts',
    ['alert_type', 'severity']
)

canary_metrics_diff = Gauge(
    'canary_metrics_difference',
    'Difference between canary and production metrics',
    ['metric_name']
)

canary_evaluation_duration = Histogram(
    'canary_evaluation_duration_seconds',
    'Time spent evaluating canary deployment',
    buckets=(1, 5, 10, 30, 60, 300)
)

class CanaryMonitor:
    def __init__(
        self,
        prometheus_url: str,
        production_url: str,
        canary_url: str,
        metrics_path: str,
        evaluation_period: int = 3600,  # 1 hour
        check_interval: int = 60,  # 1 minute
        success_threshold: float = 0.95,
        latency_threshold: float = 1.5,  # 1.5x production latency
        error_threshold: float = 0.05,
        alert_email: Optional[str] = None,
        alert_smtp_server: Optional[str] = None,
        alert_smtp_port: int = 587,
        drift_threshold: float = 0.1,
        resource_threshold: float = 1.5
    ):
        self.prometheus = PrometheusConnect(url=prometheus_url)
        self.production_url = production_url
        self.canary_url = canary_url
        self.metrics_path = metrics_path
        self.evaluation_period = evaluation_period
        self.check_interval = check_interval
        self.success_threshold = success_threshold
        self.latency_threshold = latency_threshold
        self.error_threshold = error_threshold
        self.drift_threshold = drift_threshold
        self.resource_threshold = resource_threshold
        self.alert_email = alert_email
        self.alert_smtp_server = alert_smtp_server
        self.alert_smtp_port = alert_smtp_port
        
        # Initialize metrics storage
        self.metrics = {
            'production': [],
            'canary': [],
            'comparison': [],
            'alerts': []
        }
        
        # Create directories
        self.plots_dir = os.path.join(os.path.dirname(metrics_path), 'canary_plots')
        os.makedirs(self.plots_dir, exist_ok=True)
        
        # Initialize MLflow
        try:
            mlflow.set_tracking_uri("http://localhost:5000")
            mlflow.set_experiment("canary-monitoring")
        except Exception as e:
            logger.warning(f"Failed to initialize MLflow: {str(e)}")
        
    def collect_metrics(self) -> Tuple[Dict, Dict]:
        """Collect metrics from both production and canary deployments."""
        try:
            # Query Prometheus for metrics
            prod_metrics = self._query_metrics('production')
            canary_metrics = self._query_metrics('canary')
            
            # Add timestamp
            timestamp = datetime.now().isoformat()
            prod_metrics['timestamp'] = timestamp
            canary_metrics['timestamp'] = timestamp
            
            # Store metrics
            self.metrics['production'].append(prod_metrics)
            self.metrics['canary'].append(canary_metrics)
            
            # Update Prometheus metrics
            for metric in ['success_rate', 'p95_latency', 'error_rate', 'throughput', 'drift_score']:
                canary_metrics_diff.labels(metric_name=metric).set(
                    canary_metrics[metric] - prod_metrics[metric]
                )
            
            # Log to MLflow
            try:
                with mlflow.start_run(run_name=f"canary-monitoring-{timestamp}"):
                    # Log raw metrics
                    mlflow.log_metrics({
                        "prod_success_rate": prod_metrics['success_rate'],
                        "prod_latency": prod_metrics['p95_latency'],
                        "prod_error_rate": prod_metrics['error_rate'],
                        "prod_throughput": prod_metrics['throughput'],
                        "prod_memory_usage": prod_metrics['memory_usage'],
                        "prod_cpu_usage": prod_metrics['cpu_usage'],
                        "prod_drift_score": prod_metrics['drift_score'],
                        "canary_success_rate": canary_metrics['success_rate'],
                        "canary_latency": canary_metrics['p95_latency'],
                        "canary_error_rate": canary_metrics['error_rate'],
                        "canary_throughput": canary_metrics['throughput'],
                        "canary_memory_usage": canary_metrics['memory_usage'],
                        "canary_cpu_usage": canary_metrics['cpu_usage'],
                        "canary_drift_score": canary_metrics['drift_score']
                    })
                    
                    # Generate and log visualizations
                    self._generate_metrics_plot()
                    
            except Exception as e:
                logger.warning(f"Failed to log metrics to MLflow: {str(e)}")
            
            return prod_metrics, canary_metrics
            
        except Exception as e:
            logger.error(f"Error collecting metrics: {str(e)}")
            return None, None
            
    def _query_metrics(self, deployment: str) -> Dict:
        """Query Prometheus for specific metrics."""
        metrics = {}
        
        try:
            # Query success rate
            success_query = f'sum(rate(style_transfer_requests_total{{deployment="{deployment}",status="success"}}[5m])) / sum(rate(style_transfer_requests_total{{deployment="{deployment}"}}[5m]))'
            success_result = self.prometheus.custom_query(success_query)
            metrics['success_rate'] = float(success_result[0]['value'][1]) if success_result else 0.0
            
            # Query latency
            latency_query = f'histogram_quantile(0.95, sum(rate(style_transfer_latency_bucket{{deployment="{deployment}"}}[5m])) by (le))'
            latency_result = self.prometheus.custom_query(latency_query)
            metrics['p95_latency'] = float(latency_result[0]['value'][1]) if latency_result else 0.0
            
            # Query error rate
            error_query = f'sum(rate(style_transfer_requests_total{{deployment="{deployment}",status="error"}}[5m])) / sum(rate(style_transfer_requests_total{{deployment="{deployment}"}}[5m]))'
            error_result = self.prometheus.custom_query(error_query)
            metrics['error_rate'] = float(error_result[0]['value'][1]) if error_result else 0.0
            
            # Query throughput
            throughput_query = f'sum(rate(style_transfer_requests_total{{deployment="{deployment}"}}[5m]))'
            throughput_result = self.prometheus.custom_query(throughput_query)
            metrics['throughput'] = float(throughput_result[0]['value'][1]) if throughput_result else 0.0
            
            # Query memory usage
            memory_query = f'container_memory_usage_bytes{{deployment="{deployment}"}}'
            memory_result = self.prometheus.custom_query(memory_query)
            metrics['memory_usage'] = float(memory_result[0]['value'][1]) if memory_result else 0.0
            
            # Query CPU usage
            cpu_query = f'rate(container_cpu_usage_seconds_total{{deployment="{deployment}"}}[5m])'
            cpu_result = self.prometheus.custom_query(cpu_query)
            metrics['cpu_usage'] = float(cpu_result[0]['value'][1]) if cpu_result else 0.0
            
            # Query data drift score
            drift_query = f'model_feature_drift_score{{deployment="{deployment}"}}'
            drift_result = self.prometheus.custom_query(drift_query)
            metrics['drift_score'] = float(drift_result[0]['value'][1]) if drift_result else 0.0
            
            # Query request duration
            duration_query = f'rate(style_transfer_duration_seconds_sum{{deployment="{deployment}"}}[5m]) / rate(style_transfer_duration_seconds_count{{deployment="{deployment}"}}[5m])'
            duration_result = self.prometheus.custom_query(duration_query)
            metrics['avg_duration'] = float(duration_result[0]['value'][1]) if duration_result else 0.0
            
            # Query batch size
            batch_query = f'rate(style_transfer_batch_size_sum{{deployment="{deployment}"}}[5m]) / rate(style_transfer_batch_size_count{{deployment="{deployment}"}}[5m])'
            batch_result = self.prometheus.custom_query(batch_query)
            metrics['avg_batch_size'] = float(batch_result[0]['value'][1]) if batch_result else 0.0
            
        except Exception as e:
            logger.error(f"Error querying metrics for {deployment}: {str(e)}")
            metrics = {
                'success_rate': 0.0,
                'p95_latency': 0.0,
                'error_rate': 0.0,
                'throughput': 0.0,
                'memory_usage': 0.0,
                'cpu_usage': 0.0,
                'drift_score': 0.0,
                'avg_duration': 0.0,
                'avg_batch_size': 0.0
            }
        
        return metrics
        
    def compare_metrics(self, prod_metrics: Dict, canary_metrics: Dict) -> Dict:
        """Compare metrics between production and canary deployments."""
        comparison = {
            'timestamp': prod_metrics['timestamp'],
            'success_rate_diff': canary_metrics['success_rate'] - prod_metrics['success_rate'],
            'latency_ratio': canary_metrics['p95_latency'] / prod_metrics['p95_latency'] if prod_metrics['p95_latency'] > 0 else float('inf'),
            'error_rate_diff': canary_metrics['error_rate'] - prod_metrics['error_rate'],
            'throughput_ratio': canary_metrics['throughput'] / prod_metrics['throughput'] if prod_metrics['throughput'] > 0 else float('inf'),
            'memory_ratio': canary_metrics['memory_usage'] / prod_metrics['memory_usage'] if prod_metrics['memory_usage'] > 0 else float('inf'),
            'cpu_ratio': canary_metrics['cpu_usage'] / prod_metrics['cpu_usage'] if prod_metrics['cpu_usage'] > 0 else float('inf'),
            'drift_score_diff': canary_metrics['drift_score'] - prod_metrics['drift_score'],
            'duration_ratio': canary_metrics['avg_duration'] / prod_metrics['avg_duration'] if prod_metrics['avg_duration'] > 0 else float('inf'),
            'batch_size_ratio': canary_metrics['avg_batch_size'] / prod_metrics['avg_batch_size'] if prod_metrics['avg_batch_size'] > 0 else float('inf')
        }
        
        self.metrics['comparison'].append(comparison)
        return comparison
        
    def evaluate_canary(self, comparison: Dict) -> bool:
        """Evaluate if canary deployment is performing well."""
        start_time = time.time()
        alerts = []
        severity = "warning"
        
        # Check success rate
        if comparison['success_rate_diff'] < -self.error_threshold:
            alerts.append(f"Canary success rate is significantly lower than production: {comparison['success_rate_diff']:.2f}")
            severity = "critical"
            canary_alerts.labels(alert_type="success_rate", severity=severity).inc()
            
        # Check latency
        if comparison['latency_ratio'] > self.latency_threshold:
            alerts.append(f"Canary latency is too high: {comparison['latency_ratio']:.2f}x production")
            severity = "critical"
            canary_alerts.labels(alert_type="latency", severity=severity).inc()
            
        # Check error rate
        if comparison['error_rate_diff'] > self.error_threshold:
            alerts.append(f"Canary error rate is too high: {comparison['error_rate_diff']:.2f}")
            severity = "critical"
            canary_alerts.labels(alert_type="error_rate", severity=severity).inc()
            
        # Check memory usage
        if comparison['memory_ratio'] > self.resource_threshold:
            alerts.append(f"Canary memory usage is too high: {comparison['memory_ratio']:.2f}x production")
            canary_alerts.labels(alert_type="memory", severity="warning").inc()
            
        # Check CPU usage
        if comparison['cpu_ratio'] > self.resource_threshold:
            alerts.append(f"Canary CPU usage is too high: {comparison['cpu_ratio']:.2f}x production")
            canary_alerts.labels(alert_type="cpu", severity="warning").inc()
            
        # Check data drift
        if comparison['drift_score_diff'] > self.drift_threshold:
            alerts.append(f"Canary data drift is significant: {comparison['drift_score_diff']:.2f}")
            canary_alerts.labels(alert_type="drift", severity="warning").inc()
            
        # Check request duration
        if comparison['duration_ratio'] > self.latency_threshold:
            alerts.append(f"Canary request duration is too high: {comparison['duration_ratio']:.2f}x production")
            canary_alerts.labels(alert_type="duration", severity="warning").inc()
            
        # Check batch size
        if comparison['batch_size_ratio'] < 0.5:  # Significantly smaller batches
            alerts.append(f"Canary batch size is too small: {comparison['batch_size_ratio']:.2f}x production")
            canary_alerts.labels(alert_type="batch_size", severity="warning").inc()
        
        # Store alerts
        if alerts:
            alert_entry = {
                'timestamp': comparison['timestamp'],
                'alerts': alerts,
                'severity': severity
            }
            self.metrics['alerts'].append(alert_entry)
            
            # Send email alert if configured
            if self.alert_email and self.alert_smtp_server:
                self._send_alert_email(alerts, severity)
            
            canary_evaluation_duration.observe(time.time() - start_time)
            return False
            
        canary_evaluation_duration.observe(time.time() - start_time)
        return True
        
    def _send_alert_email(self, alerts: List[str], severity: str):
        """Send alert email."""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.alert_email
            msg['To'] = self.alert_email
            msg['Subject'] = f"Canary Deployment Alert - {severity.upper()}"
            
            body = f"The following issues were detected in the canary deployment (Severity: {severity}):\n\n"
            body += "\n".join(f"- {alert}" for alert in alerts)
            body += "\n\nPlease check the canary monitoring dashboard for more details."
            
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(self.alert_smtp_server, self.alert_smtp_port) as server:
                server.starttls()
                server.login(self.alert_email, os.getenv('ALERT_EMAIL_PASSWORD', ''))
                server.send_message(msg)
                
            logger.info(f"Alert email sent successfully (Severity: {severity})")
            
        except Exception as e:
            logger.error(f"Failed to send alert email: {str(e)}")
            
    def _generate_metrics_plot(self):
        """Generate visualization of metrics comparison."""
        try:
            if not self.metrics['comparison']:
                return
                
            # Convert to DataFrame
            df = pd.DataFrame(self.metrics['comparison'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Create plots
            plt.figure(figsize=(15, 10))
            
            # Success rate difference
            plt.subplot(3, 2, 1)
            plt.plot(df['timestamp'], df['success_rate_diff'], label='Success Rate Diff')
            plt.axhline(y=-self.error_threshold, color='r', linestyle='--', label='Threshold')
            plt.title('Success Rate Difference')
            plt.xlabel('Time')
            plt.ylabel('Difference')
            plt.legend()
            
            # Latency ratio
            plt.subplot(3, 2, 2)
            plt.plot(df['timestamp'], df['latency_ratio'], label='Latency Ratio')
            plt.axhline(y=self.latency_threshold, color='r', linestyle='--', label='Threshold')
            plt.title('Latency Ratio')
            plt.xlabel('Time')
            plt.ylabel('Ratio')
            plt.legend()
            
            # Error rate difference
            plt.subplot(3, 2, 3)
            plt.plot(df['timestamp'], df['error_rate_diff'], label='Error Rate Diff')
            plt.axhline(y=self.error_threshold, color='r', linestyle='--', label='Threshold')
            plt.title('Error Rate Difference')
            plt.xlabel('Time')
            plt.ylabel('Difference')
            plt.legend()
            
            # Resource usage ratios
            plt.subplot(3, 2, 4)
            plt.plot(df['timestamp'], df['memory_ratio'], label='Memory Ratio')
            plt.plot(df['timestamp'], df['cpu_ratio'], label='CPU Ratio')
            plt.axhline(y=self.resource_threshold, color='r', linestyle='--', label='Threshold')
            plt.title('Resource Usage Ratios')
            plt.xlabel('Time')
            plt.ylabel('Ratio')
            plt.legend()
            
            # Drift score difference
            plt.subplot(3, 2, 5)
            plt.plot(df['timestamp'], df['drift_score_diff'], label='Drift Score Diff')
            plt.axhline(y=self.drift_threshold, color='r', linestyle='--', label='Threshold')
            plt.title('Drift Score Difference')
            plt.xlabel('Time')
            plt.ylabel('Difference')
            plt.legend()
            
            # Request duration ratio
            plt.subplot(3, 2, 6)
            plt.plot(df['timestamp'], df['duration_ratio'], label='Duration Ratio')
            plt.axhline(y=self.latency_threshold, color='r', linestyle='--', label='Threshold')
            plt.title('Request Duration Ratio')
            plt.xlabel('Time')
            plt.ylabel('Ratio')
            plt.legend()
            
            plt.tight_layout()
            plot_path = os.path.join(self.plots_dir, f'canary_metrics_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
            plt.savefig(plot_path)
            plt.close()
            
            # Log plot to MLflow
            try:
                mlflow.log_artifact(plot_path)
            except Exception as e:
                logger.warning(f"Failed to log plot to MLflow: {str(e)}")
                
        except Exception as e:
            logger.error(f"Failed to generate metrics plot: {str(e)}")
        
    def save_metrics(self):
        """Save collected metrics to file."""
        try:
            os.makedirs(os.path.dirname(self.metrics_path), exist_ok=True)
            with open(self.metrics_path, 'w') as f:
                json.dump(self.metrics, f, indent=2)
            logger.info(f"Metrics saved to {self.metrics_path}")
        except Exception as e:
            logger.error(f"Failed to save metrics: {str(e)}")
            
    def run_monitoring(self):
        """Run the monitoring loop."""
        logger.info("Starting canary monitoring...")
        
        while True:
            try:
                # Collect metrics
                prod_metrics, canary_metrics = self.collect_metrics()
                if prod_metrics is None or canary_metrics is None:
                    logger.error("Failed to collect metrics")
                    time.sleep(self.check_interval)
                    continue
                
                # Compare metrics
                comparison = self.compare_metrics(prod_metrics, canary_metrics)
                
                # Evaluate canary
                is_healthy = self.evaluate_canary(comparison)
                
                if is_healthy:
                    logger.info("Canary deployment is healthy")
                else:
                    logger.warning("Issues detected in canary deployment")
                
                # Save metrics
                self.save_metrics()
                
                # Wait for next check
                time.sleep(self.check_interval)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {str(e)}")
                time.sleep(self.check_interval)

def main():
    # Configuration
    prometheus_url = os.getenv('PROMETHEUS_URL', 'http://localhost:9090')
    production_url = os.getenv('PRODUCTION_URL', 'http://localhost:8000')
    canary_url = os.getenv('CANARY_URL', 'http://localhost:8001')
    metrics_path = os.getenv('METRICS_PATH', 'data/canary_metrics.json')
    
    # Create monitor
    monitor = CanaryMonitor(
        prometheus_url=prometheus_url,
        production_url=production_url,
        canary_url=canary_url,
        metrics_path=metrics_path,
        alert_email=os.getenv('ALERT_EMAIL'),
        alert_smtp_server=os.getenv('ALERT_SMTP_SERVER'),
        alert_smtp_port=int(os.getenv('ALERT_SMTP_PORT', '587'))
    )
    
    # Run monitoring
    monitor.run_monitoring()

if __name__ == '__main__':
    main() 