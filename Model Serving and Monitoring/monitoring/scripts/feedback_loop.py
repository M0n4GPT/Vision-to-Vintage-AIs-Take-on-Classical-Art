import os
import json
import logging
import argparse
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import tensorflow as tf
from tensorflow import keras
import mlflow
import mlflow.tensorflow
from prometheus_client import Counter, Gauge, Histogram
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Prometheus metrics
retraining_counter = Counter(
    'model_retraining_total',
    'Total number of model retraining events',
    ['status']
)

model_performance = Gauge(
    'model_performance_metrics',
    'Model performance metrics',
    ['metric_name']
)

retraining_duration = Histogram(
    'model_retraining_duration_seconds',
    'Time spent retraining the model',
    buckets=(60, 300, 600, 1800, 3600)
)

class FeedbackLoop:
    def __init__(
        self,
        metrics_path: str,
        model_path: str,
        data_path: str,
        mlflow_tracking_uri: str,
        retraining_threshold: float = 0.1,  # 10% degradation
        min_samples: int = 1000,
        evaluation_window: int = 7,  # days
        drift_threshold: float = 0.2,
        performance_threshold: float = 0.15
    ):
        self.metrics_path = metrics_path
        self.model_path = model_path
        self.data_path = data_path
        self.retraining_threshold = retraining_threshold
        self.min_samples = min_samples
        self.evaluation_window = evaluation_window
        self.drift_threshold = drift_threshold
        self.performance_threshold = performance_threshold
        
        # Initialize MLFlow
        mlflow.set_tracking_uri(mlflow_tracking_uri)
        
        # Create directories
        os.makedirs('feedback_logs', exist_ok=True)
        os.makedirs('feedback_plots', exist_ok=True)
        
    def load_metrics(self) -> pd.DataFrame:
        """Load and process metrics from file."""
        try:
            with open(self.metrics_path, 'r') as f:
                metrics = json.load(f)
            
            # Convert to DataFrame
            df = pd.DataFrame(metrics['comparison'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Add drift metrics if available
            if 'drift_scores' in metrics:
                drift_df = pd.DataFrame(metrics['drift_scores'])
                drift_df['timestamp'] = pd.to_datetime(drift_df['timestamp'])
                df = df.merge(drift_df, on='timestamp', how='left')
            
            return df
            
        except Exception as e:
            logger.error(f"Error loading metrics: {str(e)}")
            return pd.DataFrame()
            
    def analyze_metrics(self, df: pd.DataFrame) -> Dict:
        """Analyze metrics to detect degradation and drift."""
        if df.empty:
            return {'needs_retraining': False, 'reason': 'No metrics available'}
            
        # Calculate moving averages
        window = f'{self.evaluation_window}D'
        df['success_rate_ma'] = df['success_rate_diff'].rolling(window=window).mean()
        df['latency_ma'] = df['latency_ratio'].rolling(window=window).mean()
        df['error_rate_ma'] = df['error_rate_diff'].rolling(window=window).mean()
        
        # Add drift analysis if available
        if 'drift_score' in df.columns:
            df['drift_ma'] = df['drift_score'].rolling(window=window).mean()
        
        # Get latest metrics
        latest = df.iloc[-1]
        
        # Check for degradation
        degradation = {
            'success_rate': latest['success_rate_ma'] < -self.retraining_threshold,
            'latency': latest['latency_ma'] > 1 + self.retraining_threshold,
            'error_rate': latest['error_rate_ma'] > self.retraining_threshold
        }
        
        # Check for drift if available
        if 'drift_ma' in latest:
            degradation['drift'] = latest['drift_ma'] > self.drift_threshold
        
        needs_retraining = any(degradation.values())
        reason = 'No significant degradation detected'
        
        if needs_retraining:
            reasons = []
            if degradation.get('success_rate', False):
                reasons.append('Success rate degradation')
            if degradation.get('latency', False):
                reasons.append('Latency increase')
            if degradation.get('error_rate', False):
                reasons.append('Error rate increase')
            if degradation.get('drift', False):
                reasons.append('Data drift detected')
            reason = ', '.join(reasons)
            
        # Generate performance report
        self._generate_performance_report(df)
            
        return {
            'needs_retraining': needs_retraining,
            'reason': reason,
            'metrics': {
                'success_rate': latest['success_rate_ma'],
                'latency': latest['latency_ma'],
                'error_rate': latest['error_rate_ma'],
                'drift_score': latest.get('drift_ma', None)
            }
        }
        
    def _generate_performance_report(self, df: pd.DataFrame):
        """Generate performance visualization and report."""
        try:
            plt.figure(figsize=(15, 10))
            
            # Plot success rate trend
            plt.subplot(2, 2, 1)
            plt.plot(df['timestamp'], df['success_rate_ma'], label='Success Rate')
            plt.axhline(y=-self.retraining_threshold, color='r', linestyle='--', label='Threshold')
            plt.title('Success Rate Trend')
            plt.xlabel('Time')
            plt.ylabel('Success Rate')
            plt.legend()
            
            # Plot latency trend
            plt.subplot(2, 2, 2)
            plt.plot(df['timestamp'], df['latency_ma'], label='Latency')
            plt.axhline(y=1 + self.retraining_threshold, color='r', linestyle='--', label='Threshold')
            plt.title('Latency Trend')
            plt.xlabel('Time')
            plt.ylabel('Latency Ratio')
            plt.legend()
            
            # Plot error rate trend
            plt.subplot(2, 2, 3)
            plt.plot(df['timestamp'], df['error_rate_ma'], label='Error Rate')
            plt.axhline(y=self.retraining_threshold, color='r', linestyle='--', label='Threshold')
            plt.title('Error Rate Trend')
            plt.xlabel('Time')
            plt.ylabel('Error Rate')
            plt.legend()
            
            # Plot drift trend if available
            if 'drift_ma' in df.columns:
                plt.subplot(2, 2, 4)
                plt.plot(df['timestamp'], df['drift_ma'], label='Drift Score')
                plt.axhline(y=self.drift_threshold, color='r', linestyle='--', label='Threshold')
                plt.title('Drift Score Trend')
                plt.xlabel('Time')
                plt.ylabel('Drift Score')
                plt.legend()
            
            plt.tight_layout()
            plot_path = os.path.join('feedback_plots', f'performance_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
            plt.savefig(plot_path)
            plt.close()
            
            # Log plot to MLflow
            try:
                mlflow.log_artifact(plot_path)
            except Exception as e:
                logger.warning(f"Failed to log plot to MLflow: {str(e)}")
                
        except Exception as e:
            logger.error(f"Failed to generate performance report: {str(e)}")
        
    def collect_training_data(self) -> Optional[tf.data.Dataset]:
        """Collect and prepare data for retraining."""
        try:
            # Load production data
            data_dir = os.path.join(self.data_path, 'production')
            if not os.path.exists(data_dir):
                logger.error(f"Production data directory not found: {data_dir}")
                return None
                
            # Load images and their metrics
            image_paths = []
            metrics = []
            
            for root, _, files in os.walk(data_dir):
                for file in files:
                    if file.endswith('.jpg') or file.endswith('.png'):
                        image_path = os.path.join(root, file)
                        metric_path = image_path.replace('.jpg', '.json').replace('.png', '.json')
                        
                        if os.path.exists(metric_path):
                            with open(metric_path, 'r') as f:
                                metric = json.load(f)
                            image_paths.append(image_path)
                            metrics.append(metric)
                            
            if len(image_paths) < self.min_samples:
                logger.warning(f"Insufficient samples for retraining: {len(image_paths)} < {self.min_samples}")
                return None
                
            # Create dataset
            def load_and_preprocess(image_path):
                image = tf.io.read_file(image_path)
                image = tf.image.decode_image(image, channels=3)
                image = tf.image.resize(image, [256, 256])
                image = tf.cast(image, tf.float32) / 255.0
                return image
                
            dataset = tf.data.Dataset.from_tensor_slices(image_paths)
            dataset = dataset.map(load_and_preprocess)
            dataset = dataset.batch(32).prefetch(tf.data.AUTOTUNE)
            
            # Log dataset statistics
            self._log_dataset_stats(image_paths, metrics)
            
            return dataset
            
        except Exception as e:
            logger.error(f"Error collecting training data: {str(e)}")
            return None
            
    def _log_dataset_stats(self, image_paths: List[str], metrics: List[Dict]):
        """Log dataset statistics."""
        try:
            stats = {
                'total_samples': len(image_paths),
                'timestamp': datetime.now().isoformat(),
                'metrics_summary': {
                    'success_rate': np.mean([m.get('success_rate', 0) for m in metrics]),
                    'error_rate': np.mean([m.get('error_rate', 0) for m in metrics]),
                    'latency': np.mean([m.get('latency', 0) for m in metrics])
                }
            }
            
            # Save stats
            stats_path = os.path.join('feedback_logs', f'dataset_stats_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
            with open(stats_path, 'w') as f:
                json.dump(stats, f, indent=2)
                
            # Log to MLflow
            try:
                mlflow.log_metrics(stats['metrics_summary'])
                mlflow.log_artifact(stats_path)
            except Exception as e:
                logger.warning(f"Failed to log dataset stats to MLflow: {str(e)}")
                
        except Exception as e:
            logger.error(f"Failed to log dataset stats: {str(e)}")
            
    def retrain_model(self, dataset: tf.data.Dataset) -> bool:
        """Retrain the model with new data."""
        start_time = time.time()
        try:
            # Start MLFlow run
            with mlflow.start_run(run_name=f"retraining_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
                # Load base model
                model = tf.keras.models.load_model(self.model_path)
                
                # Compile model
                model.compile(
                    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                    loss='mse',
                    metrics=['mae']
                )
                
                # Train model
                history = model.fit(
                    dataset,
                    epochs=10,
                    callbacks=[
                        tf.keras.callbacks.EarlyStopping(
                            monitor='val_loss',
                            patience=3,
                            restore_best_weights=True
                        )
                    ]
                )
                
                # Log metrics
                mlflow.log_metrics({
                    'final_loss': history.history['loss'][-1],
                    'final_mae': history.history['mae'][-1]
                })
                
                # Update Prometheus metrics
                model_performance.labels(metric_name='loss').set(history.history['loss'][-1])
                model_performance.labels(metric_name='mae').set(history.history['mae'][-1])
                retraining_duration.observe(time.time() - start_time)
                retraining_counter.labels(status='success').inc()
                
                # Save model
                model_save_path = os.path.join(self.model_path, 'retrained_model')
                model.save(model_save_path)
                mlflow.log_artifacts(model_save_path, "model")
                
                # Generate training report
                self._generate_training_report(history)
                
                logger.info("Model retraining completed successfully")
                return True
                
        except Exception as e:
            logger.error(f"Error retraining model: {str(e)}")
            retraining_counter.labels(status='failure').inc()
            return False
            
    def _generate_training_report(self, history: Dict):
        """Generate training visualization and report."""
        try:
            plt.figure(figsize=(12, 5))
            
            # Plot loss
            plt.subplot(1, 2, 1)
            plt.plot(history.history['loss'], label='Training Loss')
            plt.plot(history.history['val_loss'], label='Validation Loss')
            plt.title('Model Loss')
            plt.xlabel('Epoch')
            plt.ylabel('Loss')
            plt.legend()
            
            # Plot MAE
            plt.subplot(1, 2, 2)
            plt.plot(history.history['mae'], label='Training MAE')
            plt.plot(history.history['val_mae'], label='Validation MAE')
            plt.title('Model MAE')
            plt.xlabel('Epoch')
            plt.ylabel('MAE')
            plt.legend()
            
            plt.tight_layout()
            plot_path = os.path.join('feedback_plots', f'training_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
            plt.savefig(plot_path)
            plt.close()
            
            # Log plot to MLflow
            try:
                mlflow.log_artifact(plot_path)
            except Exception as e:
                logger.warning(f"Failed to log plot to MLflow: {str(e)}")
                
        except Exception as e:
            logger.error(f"Failed to generate training report: {str(e)}")
            
    def run_feedback_loop(self) -> bool:
        """Run the complete feedback loop."""
        # Load and analyze metrics
        metrics_df = self.load_metrics()
        analysis = self.analyze_metrics(metrics_df)
        
        if not analysis['needs_retraining']:
            logger.info(f"No retraining needed: {analysis['reason']}")
            return True
            
        logger.info(f"Retraining needed: {analysis['reason']}")
        logger.info(f"Current metrics: {analysis['metrics']}")
        
        # Collect training data
        dataset = self.collect_training_data()
        if dataset is None:
            logger.error("Failed to collect training data")
            return False
            
        # Retrain model
        success = self.retrain_model(dataset)
        if not success:
            logger.error("Model retraining failed")
            return False
            
        logger.info("Feedback loop completed successfully")
        return True

def main():
    parser = argparse.ArgumentParser(description='Run feedback loop for model retraining')
    parser.add_argument('--metrics-path', required=True, help='Path to metrics file')
    parser.add_argument('--model-path', required=True, help='Path to model directory')
    parser.add_argument('--data-path', required=True, help='Path to data directory')
    parser.add_argument('--mlflow-tracking-uri', required=True, help='MLFlow tracking URI')
    parser.add_argument('--retraining-threshold', type=float, default=0.1,
                      help='Threshold for triggering retraining')
    parser.add_argument('--min-samples', type=int, default=1000,
                      help='Minimum samples required for retraining')
    parser.add_argument('--evaluation-window', type=int, default=7,
                      help='Evaluation window in days')
    parser.add_argument('--drift-threshold', type=float, default=0.2,
                      help='Threshold for drift detection')
    parser.add_argument('--performance-threshold', type=float, default=0.15,
                      help='Threshold for performance degradation')
    
    args = parser.parse_args()
    
    feedback_loop = FeedbackLoop(
        metrics_path=args.metrics_path,
        model_path=args.model_path,
        data_path=args.data_path,
        mlflow_tracking_uri=args.mlflow_tracking_uri,
        retraining_threshold=args.retraining_threshold,
        min_samples=args.min_samples,
        evaluation_window=args.evaluation_window,
        drift_threshold=args.drift_threshold,
        performance_threshold=args.performance_threshold
    )
    
    success = feedback_loop.run_feedback_loop()
    exit(0 if success else 1)

if __name__ == '__main__':
    main() 