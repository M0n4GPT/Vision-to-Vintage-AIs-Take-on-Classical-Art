"""
Drift detection module for monitoring data and label drift in production.
"""

import numpy as np
from scipy import stats
from typing import Dict, List, Tuple, Optional, Any
import logging
from datetime import datetime
import json
from pathlib import Path
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
import os

logger = logging.getLogger(__name__)

class DriftDetector:
    """Detects data and label drift in production environment."""
    
    def __init__(self, reference_data_path: str):
        """
        Initialize the drift detector.
        
        Args:
            reference_data_path: Path to directory containing reference data
        """
        self.reference_data_path = reference_data_path
        self.reference_data: Optional[Dict[str, np.ndarray]] = None
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=2)
        self.logger = logging.getLogger(__name__)
        
        # Load reference data if it exists
        self._load_reference_data()
    
    def _load_reference_data(self) -> None:
        """Load reference data from JSON file if it exists."""
        ref_data_file = os.path.join(self.reference_data_path, 'reference_data.json')
        if os.path.exists(ref_data_file):
            try:
                with open(ref_data_file, 'r') as f:
                    data = json.load(f)
                    self.reference_data = {
                        'content': np.array(data['content']),
                        'style': np.array(data['style'])
                    }
                self.logger.info("Successfully loaded reference data")
            except Exception as e:
                self.logger.error(f"Error loading reference data: {str(e)}")
                self.reference_data = None
    
    def _save_reference_data(self, content_data: np.ndarray, style_data: np.ndarray) -> None:
        """Save new reference data to JSON file."""
        os.makedirs(self.reference_data_path, exist_ok=True)
        ref_data_file = os.path.join(self.reference_data_path, 'reference_data.json')
        try:
            with open(ref_data_file, 'w') as f:
                json.dump({
                    'content': content_data.tolist(),
                    'style': style_data.tolist()
                }, f)
            self.logger.info("Successfully saved reference data")
        except Exception as e:
            self.logger.error(f"Error saving reference data: {str(e)}")
    
    def detect_drift(self, content_data: np.ndarray, style_data: np.ndarray) -> Dict[str, Any]:
        """
        Detect drift between current and reference data.
        
        Args:
            content_data: Current content image features
            style_data: Current style image features
            
        Returns:
            Dictionary containing drift metrics
        """
        if self.reference_data is None:
            self.logger.info("No reference data found, using current data as reference")
            self.reference_data = {
                'content': content_data,
                'style': style_data
            }
            self._save_reference_data(content_data, style_data)
            return {
                'status': 'initialized',
                'message': 'Using current data as reference'
            }
        
        # Calculate drift metrics
        metrics = {}
        
        # Kolmogorov-Smirnov Test for content images
        ks_stat, ks_pvalue = stats.ks_2samp(
            self.reference_data['content'].flatten(),
            content_data.flatten()
        )
        metrics['ks_test'] = {
            'statistic': float(ks_stat),
            'p_value': float(ks_pvalue)
        }
        
        # Chi-Square Test for style distribution
        chi2_stat, chi2_pvalue = stats.chisquare(
            np.histogram(style_data, bins=10)[0],
            np.histogram(self.reference_data['style'], bins=10)[0]
        )
        metrics['chi_square'] = {
            'statistic': float(chi2_stat),
            'p_value': float(chi2_pvalue)
        }
        
        # Wasserstein Distance
        wasserstein_dist = stats.wasserstein_distance(
            self.reference_data['content'].flatten(),
            content_data.flatten()
        )
        metrics['wasserstein_distance'] = float(wasserstein_dist)
        
        # PCA Drift Score
        combined_data = np.vstack([self.reference_data['content'], content_data])
        combined_data_scaled = self.scaler.fit_transform(combined_data)
        pca_features = self.pca.fit_transform(combined_data_scaled)
        
        # Calculate drift score based on PCA components
        ref_pca = pca_features[:len(self.reference_data['content'])]
        current_pca = pca_features[len(self.reference_data['content']):]
        pca_drift = np.mean(np.abs(ref_pca.mean(axis=0) - current_pca.mean(axis=0)))
        metrics['pca_drift_score'] = float(pca_drift)
        
        return metrics
        
    def plot_drift_history(self, output_path: Optional[str] = None) -> None:
        """
        Plot drift metrics history.
        
        Args:
            output_path: Optional path to save the plot
        """
        if not self.drift_metrics:
            logger.warning("No drift metrics to plot")
            return
            
        # Convert to DataFrame
        df = pd.DataFrame(self.drift_metrics)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Plot metrics
        plt.figure(figsize=(12, 6))
        for metric in ['ks_test', 'chi_square', 'wasserstein', 'pca_drift']:
            plt.plot(df['timestamp'], df['metrics'].apply(lambda x: x[metric]),
                    label=metric)
        plt.axhline(y=self.drift_threshold, color='r', linestyle='--',
                   label='Drift Threshold')
        plt.title('Drift Metrics Over Time')
        plt.xlabel('Timestamp')
        plt.ylabel('Metric Value')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path)
        else:
            plt.show()
            
    def get_drift_summary(self) -> Dict:
        """Get summary of drift detection results."""
        if not self.drift_metrics:
            return {"status": "no_data"}
            
        latest = self.drift_metrics[-1]
        return {
            "drift_detected": latest["drift_detected"],
            "latest_metrics": latest["metrics"],
            "timestamp": latest["timestamp"],
            "total_samples": len(self.production_data)
        } 