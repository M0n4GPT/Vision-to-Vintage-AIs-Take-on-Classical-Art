import os
import json
import logging
import argparse
from datetime import datetime, timedelta
import numpy as np
from typing import Dict, List, Any
import mlflow
from prometheus_client import start_http_server, Gauge
import time
import threading
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import joblib
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DriftMonitor:
    def __init__(
        self,
        reference_data_dir: str,
        production_data_dir: str,
        metrics_port: int = 8000,
        drift_threshold: float = 0.1,
        check_interval: int = 3600
    ):
        self.reference_data_dir = reference_data_dir
        self.production_data_dir = production_data_dir
        self.metrics_port = metrics_port
        self.drift_threshold = drift_threshold
        self.check_interval = check_interval
        
        # Initialize Prometheus metrics
        self.drift_score = Gauge(
            "data_drift_score",
            "Data drift score between reference and production data",
            ["feature"]
        )
        self.style_drift = Gauge(
            "style_drift_score",
            "Drift score for each style",
            ["style"]
        )
        self.overall_drift = Gauge(
            "overall_drift_score",
            "Overall drift score across all features"
        )
        
        # Load reference data
        self.reference_data = self.load_reference_data()
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=0.95)  # Keep 95% of variance
        
        # Check if reference data is empty
        if len(self.reference_data) == 0:
            logger.warning("Reference data is empty. Creating dummy reference data for initialization.")
            # Create dummy reference data (one sample with 100 features)
            self.reference_data = np.random.rand(5, 100)
            logger.info(f"Created dummy reference data with shape {self.reference_data.shape}")
        
        # Fit scaler and PCA on reference data
        self.scaler.fit(self.reference_data)
        self.pca.fit(self.scaler.transform(self.reference_data))
        
        # Save model for future use
        os.makedirs(os.path.join(os.path.dirname(reference_data_dir), "models"), exist_ok=True)
        joblib.dump(self.scaler, os.path.join(os.path.dirname(reference_data_dir), "models", "scaler.pkl"))
        joblib.dump(self.pca, os.path.join(os.path.dirname(reference_data_dir), "models", "pca.pkl"))
    
    def load_reference_data(self) -> np.ndarray:
        """Load and preprocess reference data."""
        features = []
        
        # Check if the directory exists
        if not os.path.exists(self.reference_data_dir):
            logger.warning(f"Reference data directory does not exist: {self.reference_data_dir}")
            return np.array(features)
            
        for style in os.listdir(self.reference_data_dir):
            style_dir = os.path.join(self.reference_data_dir, style)
            if os.path.isdir(style_dir):
                for file in os.listdir(style_dir):
                    if file.endswith(('.jpg', '.jpeg', '.png')):
                        # Load and extract features
                        features.append(self.extract_features(
                            os.path.join(style_dir, file)
                        ))
        
        if not features:
            logger.warning("No reference data files found.")
            
        return np.array(features)
    
    def extract_features(self, image_path: str) -> np.ndarray:
        """Extract features from an image."""
        try:
            image = Image.open(image_path).convert('RGB')
            image = image.resize((224, 224))  # Resize to standard size
            image_array = np.array(image)
            
            # Simple feature extraction:
            # 1. Average RGB values per channel
            avg_rgb = image_array.mean(axis=(0, 1))
            
            # 2. Standard deviation of RGB values
            std_rgb = image_array.std(axis=(0, 1))
            
            # 3. Histogram features - simplified to 10 bins per channel
            hist_features = []
            for channel in range(3):
                hist, _ = np.histogram(image_array[:, :, channel], bins=10, range=(0, 256))
                hist = hist / hist.sum()  # Normalize
                hist_features.extend(hist)
            
            # Combine features
            features = np.concatenate([avg_rgb, std_rgb, np.array(hist_features)])
            return features
        except Exception as e:
            logger.error(f"Error extracting features from {image_path}: {e}")
            # Return a vector of zeros as a fallback
            return np.zeros(36)  # 3 (avg) + 3 (std) + 30 (hist)
    
    def calculate_drift_score(
        self,
        reference_data: np.ndarray,
        production_data: np.ndarray
    ) -> Dict[str, float]:
        """Calculate drift scores for each feature."""
        # Check if we have enough data
        if len(reference_data) < 2 or len(production_data) < 2:
            logger.warning("Not enough samples for reliable drift calculation.")
            return {"insufficient_data": 0.0}

        try:
            # Transform data
            ref_transformed = self.pca.transform(
                self.scaler.transform(reference_data)
            )
            prod_transformed = self.pca.transform(
                self.scaler.transform(production_data)
            )
            
            # Calculate drift scores
            drift_scores = {}
            for i in range(ref_transformed.shape[1]):
                ref_dist = np.histogram(ref_transformed[:, i], bins=50)[0]
                prod_dist = np.histogram(prod_transformed[:, i], bins=50)[0]
                
                # Normalize distributions
                ref_dist = ref_dist / (np.sum(ref_dist) + 1e-10)
                prod_dist = prod_dist / (np.sum(prod_dist) + 1e-10)
                
                # Calculate KL divergence
                kl_div = np.sum(
                    ref_dist * np.log((ref_dist + 1e-10) / (prod_dist + 1e-10))
                )
                drift_scores[f"feature_{i}"] = kl_div
            
            return drift_scores
        except Exception as e:
            logger.error(f"Error calculating drift score: {str(e)}")
            return {"error": 0.0}
    
    def monitor_drift(self):
        """Monitor data drift in production."""
        while True:
            try:
                # Load production data
                production_data = self.load_production_data()
                
                if len(production_data) == 0:
                    logger.info("No production data available for drift monitoring. Skipping this check.")
                elif len(self.reference_data) == 0:
                    logger.warning("No reference data available for drift monitoring. Skipping this check.")
                else:
                    # Calculate drift scores
                    drift_scores = self.calculate_drift_score(
                        self.reference_data,
                        production_data
                    )
                    
                    # Update Prometheus metrics
                    for feature, score in drift_scores.items():
                        self.drift_score.labels(feature=feature).set(score)
                    
                    # Calculate overall drift score
                    overall_score = np.mean(list(drift_scores.values()))
                    self.overall_drift.set(overall_score)
                    
                    # Log to MLflow
                    try:
                        mlflow.log_metrics(drift_scores)
                        mlflow.log_metric("overall_drift_score", overall_score)
                    except Exception as e:
                        logger.warning(f"Failed to log to MLflow: {str(e)}")
                    
                    # Check for drift
                    if overall_score > self.drift_threshold:
                        logger.warning(
                            f"Data drift detected! Overall score: {overall_score:.3f}"
                        )
                        self.handle_drift_detection(drift_scores)
                
            except Exception as e:
                logger.error(f"Error in drift monitoring: {str(e)}")
            
            time.sleep(self.check_interval)
    
    def load_production_data(self) -> np.ndarray:
        """Load and preprocess production data."""
        features = []
        
        # Check if the directory exists
        if not os.path.exists(self.production_data_dir):
            logger.warning(f"Production data directory does not exist: {self.production_data_dir}")
            return np.array(features)
            
        for style in os.listdir(self.production_data_dir):
            style_dir = os.path.join(self.production_data_dir, style)
            if os.path.isdir(style_dir):
                for file in os.listdir(style_dir):
                    if file.endswith(('.jpg', '.jpeg', '.png')):
                        # Load and extract features
                        features.append(self.extract_features(
                            os.path.join(style_dir, file)
                        ))
        
        if not features:
            logger.info("No production data files found in the current check.")
            
        return np.array(features)
    
    def handle_drift_detection(self, drift_scores: Dict[str, float]):
        """Handle drift detection by triggering retraining or alerting."""
        # Save drift information
        drift_info = {
            "timestamp": datetime.utcnow().isoformat(),
            "drift_scores": drift_scores,
            "overall_score": np.mean(list(drift_scores.values())),
            "threshold": self.drift_threshold
        }
        
        drift_dir = "drift_detections"
        os.makedirs(drift_dir, exist_ok=True)
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        drift_file = os.path.join(drift_dir, f"drift_detection_{timestamp}.json")
        
        with open(drift_file, 'w') as f:
            json.dump(drift_info, f, indent=2)
        
        # TODO: Implement retraining trigger or alerting system
        logger.info(f"Drift detection saved to {drift_file}")

def main():
    parser = argparse.ArgumentParser(description="Monitor data drift in production")
    parser.add_argument("--reference-data-dir", required=True, help="Directory containing reference data")
    parser.add_argument("--production-data-dir", required=True, help="Directory containing production data")
    parser.add_argument("--metrics-port", type=int, default=8000, help="Port for Prometheus metrics")
    parser.add_argument("--drift-threshold", type=float, default=0.1, help="Threshold for drift detection")
    parser.add_argument("--check-interval", type=int, default=3600, help="Interval between drift checks in seconds")
    
    args = parser.parse_args()
    
    # Start Prometheus metrics server
    start_http_server(args.metrics_port)
    
    # Initialize and start drift monitor
    monitor = DriftMonitor(
        reference_data_dir=args.reference_data_dir,
        production_data_dir=args.production_data_dir,
        metrics_port=args.metrics_port,
        drift_threshold=args.drift_threshold,
        check_interval=args.check_interval
    )
    
    # Start monitoring in a separate thread
    monitor_thread = threading.Thread(
        target=monitor.monitor_drift,
        daemon=True
    )
    monitor_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping drift monitor...")

if __name__ == "__main__":
    main() 