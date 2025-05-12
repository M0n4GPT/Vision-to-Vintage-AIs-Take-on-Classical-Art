import numpy as np
from PIL import Image
import torch
import torchvision.transforms as transforms
from typing import List, Dict, Tuple, Optional
import logging
from datetime import datetime, timedelta
import json
import os
from prometheus_client import Gauge, Histogram, Counter
import mlflow
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import wasserstein_distance
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Prometheus metrics
feature_drift_score = Gauge(
    'feature_drift_score',
    'Score indicating the level of feature drift'
)

label_drift_score = Gauge(
    'label_drift_score',
    'Score indicating the level of label drift'
)

drift_detection_latency = Histogram(
    'drift_detection_latency_seconds',
    'Time spent detecting drift',
    buckets=(0.1, 0.5, 1.0, 2.0, 5.0)
)

drift_alerts_total = Counter(
    'drift_alerts_total',
    'Total number of drift alerts',
    ['type', 'severity']
)

class DataDriftMonitor:
    def __init__(
        self,
        reference_data_path: str,
        drift_threshold: float = 0.1,
        alert_threshold: float = 0.2,
        window_size: int = 100,
        pca_components: int = 50
    ):
        """Initialize the data drift monitor with reference data"""
        self.reference_data_path = reference_data_path
        self.reference_stats = self._load_reference_stats()
        self.drift_threshold = drift_threshold
        self.alert_threshold = alert_threshold
        self.window_size = window_size
        self.pca_components = pca_components
        
        # Initialize image transforms
        self.transform = transforms.Compose([
            transforms.Resize(512),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        # Create directories
        os.makedirs('drift_logs', exist_ok=True)
        os.makedirs('drift_plots', exist_ok=True)
        
        # Initialize drift window
        self.drift_window = []
        
        # Initialize PCA
        self.pca = PCA(n_components=pca_components)
        self.scaler = StandardScaler()
        
        # Initialize drift history
        self.drift_history = []

    def _load_reference_stats(self) -> Dict:
        """Load reference statistics from file"""
        try:
            stats_file = os.path.join(self.reference_data_path, 'reference_stats.json')
            if os.path.exists(stats_file):
                with open(stats_file, 'r') as f:
                    stats = json.load(f)
                    
                # Convert lists to numpy arrays for better performance
                if 'mean' in stats:
                    stats['mean'] = np.array(stats['mean'])
                if 'std' in stats:
                    stats['std'] = np.array(stats['std'])
                if 'histogram' in stats and stats['histogram']:
                    stats['histogram'] = np.array(stats['histogram'])
                    
                return stats
            else:
                logger.warning("Reference stats file not found, initializing empty stats")
                return {
                    'mean': np.array([0.485, 0.456, 0.406]),  # ImageNet means
                    'std': np.array([0.229, 0.224, 0.225]),   # ImageNet stds
                    'histogram': None,
                    'pca_components': None,
                    'scaler_mean': None,
                    'scaler_scale': None
                }
        except Exception as e:
            logger.error(f"Failed to load reference stats: {str(e)}")
            return {}

    def _compute_image_stats(self, image: Image.Image) -> Dict:
        """Compute statistics for a single image"""
        try:
            # Convert to tensor
            tensor = self.transform(image)
            
            # Compute mean and std
            mean = tensor.mean(dim=[1, 2]).numpy()
            std = tensor.std(dim=[1, 2]).numpy()
            
            # Compute histogram
            histogram = torch.histc(tensor, bins=50, min=0, max=1).numpy()
            
            # Compute PCA features
            features = tensor.view(1, -1).numpy()
            if self.reference_stats.get('scaler_mean') is not None:
                features = (features - self.reference_stats['scaler_mean']) / self.reference_stats['scaler_scale']
            if self.reference_stats.get('pca_components') is not None:
                features = features @ self.reference_stats['pca_components'].T
            
            return {
                'mean': mean,
                'std': std,
                'histogram': histogram,
                'pca_features': features
            }
        except Exception as e:
            logger.error(f"Failed to compute image stats: {str(e)}")
            return {}

    def _compute_drift_score(self, current_stats: Dict, reference_stats: Dict) -> float:
        """Compute drift score between current and reference statistics"""
        try:
            scores = []
            
            # Compare means
            if 'mean' in current_stats and 'mean' in reference_stats:
                mean_diff = np.mean(np.abs(current_stats['mean'] - reference_stats['mean']))
                scores.append(mean_diff)
            
            # Compare stds
            if 'std' in current_stats and 'std' in reference_stats:
                std_diff = np.mean(np.abs(current_stats['std'] - reference_stats['std']))
                scores.append(std_diff)
            
            # Compare histograms
            if current_stats.get('histogram') is not None and reference_stats.get('histogram') is not None:
                hist_diff = wasserstein_distance(
                    current_stats['histogram'],
                    reference_stats['histogram']
                )
                scores.append(hist_diff)
            
            # Compare PCA features
            if current_stats.get('pca_features') is not None and reference_stats.get('pca_components') is not None:
                pca_diff = np.mean(np.abs(current_stats['pca_features']))
                scores.append(pca_diff)
            
            # Combine scores (equal weights)
            drift_score = np.mean(scores) if scores else 0.0
            
            return float(drift_score)
        except Exception as e:
            logger.error(f"Failed to compute drift score: {str(e)}")
            return 0.0

    def detect_drift(self, image: Image.Image) -> Tuple[bool, float, str]:
        """Detect drift in a single image"""
        start_time = time.time()
        try:
            # Compute current stats
            current_stats = self._compute_image_stats(image)
            
            # Compute drift score
            drift_score = self._compute_drift_score(current_stats, self.reference_stats)
            
            # Update drift window
            self.drift_window.append(drift_score)
            if len(self.drift_window) > self.window_size:
                self.drift_window.pop(0)
            
            # Update Prometheus metrics
            feature_drift_score.set(drift_score)
            drift_detection_latency.observe(time.time() - start_time)
            
            # Log to MLflow
            try:
                mlflow.log_metric("feature_drift_score", drift_score)
                if len(self.drift_window) > 1:
                    mlflow.log_metric("drift_trend", np.mean(self.drift_window))
            except Exception as e:
                logger.warning(f"Failed to log to MLflow: {str(e)}")
            
            # Determine drift severity
            severity = "none"
            if drift_score > self.alert_threshold:
                severity = "critical"
                drift_alerts_total.labels(type="feature", severity="critical").inc()
            elif drift_score > self.drift_threshold:
                severity = "warning"
                drift_alerts_total.labels(type="feature", severity="warning").inc()
            
            # Log drift detection
            self._log_drift_detection(drift_score, severity)
            
            # Generate drift plot
            self._generate_drift_plot()
            
            # Check if drift exceeds threshold
            drift_detected = drift_score > self.drift_threshold
            
            return drift_detected, drift_score, severity
            
        except Exception as e:
            logger.error(f"Drift detection failed: {str(e)}")
            return False, 0.0, "error"

    def _log_drift_detection(self, drift_score: float, severity: str):
        """Log drift detection results"""
        try:
            timestamp = datetime.now().isoformat()
            log_entry = {
                'timestamp': timestamp,
                'drift_score': drift_score,
                'threshold': self.drift_threshold,
                'severity': severity,
                'window_mean': np.mean(self.drift_window) if self.drift_window else 0.0,
                'window_std': np.std(self.drift_window) if self.drift_window else 0.0
            }
            
            # Append to drift log file
            log_file = os.path.join('drift_logs', f'drift_log_{datetime.now().strftime("%Y%m%d")}.json')
            
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            else:
                logs = []
            
            logs.append(log_entry)
            
            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)
            
            # Update drift history
            self.drift_history.append(log_entry)
            if len(self.drift_history) > 1000:  # Keep last 1000 entries
                self.drift_history = self.drift_history[-1000:]
                
        except Exception as e:
            logger.error(f"Failed to log drift detection: {str(e)}")

    def _generate_drift_plot(self):
        """Generate drift visualization plot"""
        try:
            if len(self.drift_window) < 2:
                return
            
            plt.figure(figsize=(12, 6))
            
            # Plot drift scores
            plt.subplot(2, 1, 1)
            plt.plot(self.drift_window, label='Drift Score')
            plt.axhline(y=self.drift_threshold, color='r', linestyle='--', label='Warning Threshold')
            plt.axhline(y=self.alert_threshold, color='g', linestyle='--', label='Alert Threshold')
            plt.title('Feature Drift Over Time')
            plt.xlabel('Window Position')
            plt.ylabel('Drift Score')
            plt.legend()
            
            # Plot drift distribution
            plt.subplot(2, 1, 2)
            sns.histplot(self.drift_window, bins=20)
            plt.axvline(x=self.drift_threshold, color='r', linestyle='--', label='Warning Threshold')
            plt.axvline(x=self.alert_threshold, color='g', linestyle='--', label='Alert Threshold')
            plt.title('Drift Score Distribution')
            plt.xlabel('Drift Score')
            plt.ylabel('Count')
            plt.legend()
            
            # Save plot
            plt.tight_layout()
            plot_path = os.path.join('drift_plots', f'drift_plot_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
            plt.savefig(plot_path)
            plt.close()
            
            # Log plot to MLflow
            try:
                mlflow.log_artifact(plot_path)
            except Exception as e:
                logger.warning(f"Failed to log plot to MLflow: {str(e)}")
                
        except Exception as e:
            logger.error(f"Failed to generate drift plot: {str(e)}")

    def update_reference_stats(self, new_stats: Dict):
        """Update reference statistics with new data"""
        try:
            # Update PCA if new data is available
            if 'pca_features' in new_stats:
                features = np.array([s['pca_features'] for s in new_stats['pca_features']])
                self.scaler.fit(features)
                self.pca.fit(self.scaler.transform(features))
                
                new_stats['pca_components'] = self.pca.components_
                new_stats['scaler_mean'] = self.scaler.mean_
                new_stats['scaler_scale'] = self.scaler.scale_
            
            self.reference_stats = new_stats
            
            # Save updated stats
            stats_file = os.path.join(self.reference_data_path, 'reference_stats.json')
            with open(stats_file, 'w') as f:
                json.dump(new_stats, f, indent=2)
                
            logger.info("Reference statistics updated successfully")
            
        except Exception as e:
            logger.error(f"Failed to update reference stats: {str(e)}")

    def get_drift_history(self, days: int = 7) -> List[Dict]:
        """Get drift detection history for the specified number of days"""
        try:
            history = []
            for i in range(days):
                date = (datetime.now() - timedelta(days=i)).strftime("%Y%m%d")
                log_file = os.path.join('drift_logs', f'drift_log_{date}.json')
                
                if os.path.exists(log_file):
                    with open(log_file, 'r') as f:
                        history.extend(json.load(f))
            
            # Convert to DataFrame for analysis
            df = pd.DataFrame(history)
            if not df.empty:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df = df.sort_values('timestamp')
                
                # Add rolling statistics
                df['rolling_mean'] = df['drift_score'].rolling(window=10).mean()
                df['rolling_std'] = df['drift_score'].rolling(window=10).std()
            
            return df.to_dict('records') if not df.empty else []
            
        except Exception as e:
            logger.error(f"Failed to get drift history: {str(e)}")
            return []

    def get_drift_summary(self) -> Dict:
        """Get summary statistics of drift detection"""
        try:
            if not self.drift_history:
                return {}
            
            df = pd.DataFrame(self.drift_history)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            summary = {
                'total_detections': len(df),
                'current_drift_score': df['drift_score'].iloc[-1],
                'mean_drift_score': df['drift_score'].mean(),
                'std_drift_score': df['drift_score'].std(),
                'max_drift_score': df['drift_score'].max(),
                'min_drift_score': df['drift_score'].min(),
                'warning_count': len(df[df['severity'] == 'warning']),
                'critical_count': len(df[df['severity'] == 'critical']),
                'last_updated': df['timestamp'].max().isoformat()
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Failed to get drift summary: {str(e)}")
            return {} 