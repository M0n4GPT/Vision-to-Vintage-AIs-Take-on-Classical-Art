"""
Monitoring and metrics utility functions for the Vision-to-Vintage model serving application.
"""
from prometheus_client import Counter, Histogram, Gauge, Summary
from typing import Dict, Any, Optional, List
import numpy as np
import time
from datetime import datetime
import json
from pathlib import Path

class MetricsManager:
    """Manager class for handling monitoring metrics."""
    
    def __init__(self):
        """Initialize metrics."""
        # Request metrics
        self.inference_requests = Counter(
            'inference_requests_total', 
            'Total number of inference requests'
        )
        self.inference_latency = Histogram(
            'inference_latency_seconds',
            'Inference latency in seconds',
            buckets=(0.1, 0.5, 1.0, 2.0, 5.0)
        )
        self.batch_size = Summary(
            'batch_size',
            'Distribution of batch sizes'
        )
        
        # Error metrics
        self.model_errors = Counter(
            'model_errors_total',
            'Total number of model errors',
            ['error_type']
        )
        
        # Resource metrics
        self.active_connections = Gauge(
            'active_connections',
            'Number of active connections'
        )
        self.memory_usage = Gauge(
            'memory_usage_bytes',
            'Current memory usage in bytes'
        )
        
        # Drift metrics
        self.distribution_drift = Gauge(
            'distribution_drift',
            'Distribution drift from reference data',
            ['metric_type']
        )
    
    def record_inference(self, start_time: float, success: bool = True, error_type: Optional[str] = None) -> None:
        """
        Record inference metrics.
        
        Args:
            start_time: Start time of inference
            success: Whether the inference was successful
            error_type: Type of error if inference failed
        """
        self.inference_requests.inc()
        self.inference_latency.observe(time.time() - start_time)
        
        if not success and error_type:
            self.model_errors.labels(error_type=error_type).inc()
    
    def record_batch_size(self, size: int) -> None:
        """Record batch size."""
        self.batch_size.observe(size)
    
    def update_connections(self, connected: bool) -> None:
        """Update connection metrics."""
        if connected:
            self.active_connections.inc()
        else:
            self.active_connections.dec()
    
    def update_memory_usage(self, usage_bytes: int) -> None:
        """Update memory usage metric."""
        self.memory_usage.set(usage_bytes)
    
    def calculate_drift_metrics(self, 
                              reference_data: np.ndarray,
                              current_data: np.ndarray,
                              save_path: Optional[str] = None) -> Dict[str, float]:
        """
        Calculate and record drift metrics.
        
        Args:
            reference_data: Reference data distribution
            current_data: Current data distribution
            save_path: Optional path to save drift metrics
            
        Returns:
            Dictionary containing drift metrics
        """
        # Calculate statistics
        ref_mean = np.mean(reference_data)
        ref_std = np.std(reference_data)
        curr_mean = np.mean(current_data)
        curr_std = np.std(current_data)
        
        # Calculate drift metrics
        mean_drift = abs(curr_mean - ref_mean) / ref_mean
        std_drift = abs(curr_std - ref_std) / ref_std
        ks_stat = self._calculate_ks_statistic(reference_data, current_data)
        
        # Record metrics
        self.distribution_drift.labels(metric_type='mean').set(mean_drift)
        self.distribution_drift.labels(metric_type='std').set(std_drift)
        self.distribution_drift.labels(metric_type='ks').set(ks_stat)
        
        metrics = {
            "mean_drift": float(mean_drift),
            "std_drift": float(std_drift),
            "ks_statistic": float(ks_stat),
            "timestamp": datetime.now().isoformat()
        }
        
        # Save metrics if path provided
        if save_path:
            self._save_drift_metrics(metrics, save_path)
        
        return metrics
    
    def _calculate_ks_statistic(self, data1: np.ndarray, data2: np.ndarray) -> float:
        """Calculate Kolmogorov-Smirnov statistic."""
        from scipy import stats
        return float(stats.ks_2samp(data1.flatten(), data2.flatten()).statistic)
    
    def _save_drift_metrics(self, metrics: Dict[str, float], save_path: str) -> None:
        """Save drift metrics to disk."""
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing metrics if file exists
        if save_path.exists():
            with open(save_path, 'r') as f:
                existing_metrics = json.load(f)
            if not isinstance(existing_metrics, list):
                existing_metrics = [existing_metrics]
        else:
            existing_metrics = []
        
        # Append new metrics and save
        existing_metrics.append(metrics)
        with open(save_path, 'w') as f:
            json.dump(existing_metrics, f, indent=2) 