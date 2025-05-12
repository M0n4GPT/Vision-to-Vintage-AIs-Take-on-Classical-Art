"""
Monitoring module for style transfer application.
Handles metrics collection, logging, and dashboard integration.
"""
import os
import time
import json
import logging
import numpy as np
from typing import Dict, List, Optional, Union, Any
from datetime import datetime
from pathlib import Path
from prometheus_client import Counter, Histogram, Gauge, Summary, CollectorRegistry, generate_latest, REGISTRY

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define paths
PROJECT_ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = PROJECT_ROOT / "data"
METRICS_DIR = DATA_DIR / "metrics"
LOGS_DIR = DATA_DIR / "logs"

# Ensure directories exist
os.makedirs(METRICS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Define default metrics
api_requests_total = Counter(
    'api_requests_total', 
    'Total number of API requests',
    ['endpoint', 'method', 'status_code']
)

api_request_duration = Histogram(
    'api_request_duration_seconds',
    'API request duration in seconds',
    ['endpoint', 'method'],
    buckets=(0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, float("inf"))
)

model_predictions_total = Counter(
    'model_predictions_total',
    'Total number of model predictions',
    ['status', 'style']
)
         
model_prediction_duration_seconds = Histogram(
    'model_prediction_duration_seconds',
    'Time spent processing model predictions',
    buckets=(0.1, 0.5, 1.0, 2.0, 5.0, 10.0, float("inf"))
)

model_memory_usage = Gauge(
    'model_memory_usage_bytes',
    'Memory usage of the model in bytes'
)

model_feature_drift_score = Gauge(
    'model_feature_drift_score',
    'Score indicating the level of data drift'
)

feedback_collection_total = Counter(
    'feedback_collection_total',
    'Total number of feedback entries collected',
    ['sentiment']
)

_metrics_manager_instance: Optional['MetricsManager'] = None

class MetricsManager:
    """Manager for collecting and reporting metrics."""
    
    def __init__(self):
        """Initialize the metrics manager."""
        if _metrics_manager_instance is not None:
            pass

        self.registry = REGISTRY
        self.start_time = time.time()
        self.metrics_file = METRICS_DIR / "metrics.json"
        self.log_file = LOGS_DIR / f"app_log_{datetime.now().strftime('%Y%m%d')}.log"
        
        # Initialize metrics storage
        self.metrics_data = self._load_metrics()
        
    def _load_metrics(self) -> Dict:
        """Load metrics from file if it exists."""
        if os.path.exists(self.metrics_file):
            try:
                with open(self.metrics_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading metrics file: {e}")
        
        # Default metrics structure
        return {
            "api_requests": {},
            "model_predictions": {},
            "model_performance": {
                "inference_times": [],
                "memory_usage": []
            },
            "data_drift": {
                "scores": []
            },
            "feedback": {
                "positive": 0,
                "neutral": 0,
                "negative": 0
            },
            "uptime": 0
        }
    
    def _save_metrics(self) -> None:
        """Save metrics to file."""
        try:
            # Update uptime
            self.metrics_data["uptime"] = time.time() - self.start_time
            
            with open(self.metrics_file, 'w') as f:
                json.dump(self.metrics_data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving metrics file: {e}")
    
    def record_api_request(self, endpoint: str, method: str, status_code: int, duration: float) -> None:
        """Record API request metrics."""
        try:
            # Update Prometheus metrics
            api_requests_total.labels(endpoint=endpoint, method=method, status_code=status_code).inc()
            api_request_duration.labels(endpoint=endpoint, method=method).observe(duration)
            
            # Update internal metrics
            endpoint_key = f"{method}_{endpoint}"
            if endpoint_key not in self.metrics_data["api_requests"]:
                self.metrics_data["api_requests"][endpoint_key] = {
                    "total": 0,
                    "success": 0,
                    "error": 0,
                    "avg_duration": 0
                }
            
            self.metrics_data["api_requests"][endpoint_key]["total"] += 1
            
            if 200 <= status_code < 400:
                self.metrics_data["api_requests"][endpoint_key]["success"] += 1
            else:
                self.metrics_data["api_requests"][endpoint_key]["error"] += 1
            
            # Update average duration using weighted average
            current_avg = self.metrics_data["api_requests"][endpoint_key]["avg_duration"]
            current_total = self.metrics_data["api_requests"][endpoint_key]["total"]
            self.metrics_data["api_requests"][endpoint_key]["avg_duration"] = (
                (current_avg * (current_total - 1) + duration) / current_total
            )
            
            # Save metrics periodically (every 10 requests)
            if sum(endpoint["total"] for endpoint in self.metrics_data["api_requests"].values()) % 10 == 0:
                self._save_metrics()
                
        except Exception as e:
            logger.error(f"Error recording API request metrics: {e}")
    
    def record_model_prediction(self, style: str, status: str, duration: float, memory_usage: Optional[int] = None) -> None:
        """Record model prediction metrics."""
        try:
            # Update Prometheus metrics
            model_predictions_total.labels(status=status, style=style).inc()
            model_prediction_duration_seconds.observe(duration)
            
            if memory_usage:
                model_memory_usage.set(memory_usage)
            
            # Update internal metrics
            if style not in self.metrics_data["model_predictions"]:
                self.metrics_data["model_predictions"][style] = {
                    "total": 0,
                    "success": 0,
                    "error": 0,
                    "avg_duration": 0
                }
            
            self.metrics_data["model_predictions"][style]["total"] += 1
            
            if status == "success":
                self.metrics_data["model_predictions"][style]["success"] += 1
            else:
                self.metrics_data["model_predictions"][style]["error"] += 1
            
            # Update average duration
            current_avg = self.metrics_data["model_predictions"][style]["avg_duration"]
            current_total = self.metrics_data["model_predictions"][style]["total"]
            self.metrics_data["model_predictions"][style]["avg_duration"] = (
                (current_avg * (current_total - 1) + duration) / current_total
            )
            
            # Add to inference times list (keep only last 1000)
            self.metrics_data["model_performance"]["inference_times"].append(duration)
            self.metrics_data["model_performance"]["inference_times"] = (
                self.metrics_data["model_performance"]["inference_times"][-1000:]
            )
            
            # Add memory usage if provided
            if memory_usage:
                self.metrics_data["model_performance"]["memory_usage"].append(memory_usage)
                self.metrics_data["model_performance"]["memory_usage"] = (
                    self.metrics_data["model_performance"]["memory_usage"][-1000:]
                )
            
            # Save metrics periodically
            if sum(style["total"] for style in self.metrics_data["model_predictions"].values()) % 10 == 0:
                self._save_metrics()
                
        except Exception as e:
            logger.error(f"Error recording model prediction metrics: {e}")
    
    def record_data_drift(self, drift_score: float) -> None:
        """Record data drift metrics."""
        try:
            # Update Prometheus metrics
            model_feature_drift_score.set(drift_score)
            
            # Update internal metrics
            self.metrics_data["data_drift"]["scores"].append({
                "timestamp": datetime.now().isoformat(),
                "score": drift_score
            })
            
            # Keep only last 1000 scores
            self.metrics_data["data_drift"]["scores"] = (
                self.metrics_data["data_drift"]["scores"][-1000:]
            )
            
            # Save metrics
            self._save_metrics()
                
        except Exception as e:
            logger.error(f"Error recording data drift metrics: {e}")
    
    def record_feedback(self, sentiment: str) -> None:
        """Record user feedback metrics."""
        try:
            # Update Prometheus metrics
            feedback_collection_total.labels(sentiment=sentiment).inc()
            
            # Update internal metrics
            if sentiment in self.metrics_data["feedback"]:
                self.metrics_data["feedback"][sentiment] += 1
            else:
                # For unexpected sentiment values
                self.metrics_data["feedback"]["neutral"] += 1
            
            # Save metrics
            self._save_metrics()
                
        except Exception as e:
            logger.error(f"Error recording feedback metrics: {e}")
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get a summary of collected metrics."""
        try:
            # Calculate summary statistics
            inference_times = self.metrics_data["model_performance"]["inference_times"]
            
            summary = {
                "uptime_seconds": time.time() - self.start_time,
                "api_requests": {
                    "total": sum(endpoint["total"] for endpoint in self.metrics_data["api_requests"].values()),
                    "success_rate": sum(endpoint["success"] for endpoint in self.metrics_data["api_requests"].values()) / 
                                  max(1, sum(endpoint["total"] for endpoint in self.metrics_data["api_requests"].values()))
                },
                "model_predictions": {
                    "total": sum(style["total"] for style in self.metrics_data["model_predictions"].values()),
                    "success_rate": sum(style["success"] for style in self.metrics_data["model_predictions"].values()) / 
                                  max(1, sum(style["total"] for style in self.metrics_data["model_predictions"].values()))
                },
                "model_performance": {
                    "avg_inference_time": np.mean(inference_times) if inference_times else 0,
                    "p95_inference_time": np.percentile(inference_times, 95) if len(inference_times) >= 20 else 0,
                    "p99_inference_time": np.percentile(inference_times, 99) if len(inference_times) >= 100 else 0
                },
                "feedback": self.metrics_data["feedback"],
                "data_drift": {
                    "current_score": self.metrics_data["data_drift"]["scores"][-1]["score"] 
                                   if self.metrics_data["data_drift"]["scores"] else 0,
                    "avg_score": np.mean([entry["score"] for entry in self.metrics_data["data_drift"]["scores"]])
                                 if self.metrics_data["data_drift"]["scores"] else 0
                }
            }
            
            return summary
                
        except Exception as e:
            logger.error(f"Error getting metrics summary: {e}")
            return {"error": str(e)}

def get_metrics_manager() -> MetricsManager:
    """Get the singleton instance of the MetricsManager."""
    global _metrics_manager_instance
    if _metrics_manager_instance is None:
        _metrics_manager_instance = MetricsManager()
    return _metrics_manager_instance 