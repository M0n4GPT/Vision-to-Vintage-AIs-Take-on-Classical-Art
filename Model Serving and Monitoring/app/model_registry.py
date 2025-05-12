import mlflow
import mlflow.pytorch
import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from model_management.model_serving import ModelManager
from monitoring.monitoring import ModelMonitor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelRegistry:
    def __init__(self, tracking_uri: str = "http://localhost:5000"):
        """Initialize the model registry with MLflow tracking server"""
        mlflow.set_tracking_uri(tracking_uri)
        self.experiment_name = "style_transfer"
        self._setup_experiment()

    def _setup_experiment(self):
        """Set up MLflow experiment if it doesn't exist"""
        try:
            experiment = mlflow.get_experiment_by_name(self.experiment_name)
            if experiment is None:
                mlflow.create_experiment(self.experiment_name)
            mlflow.set_experiment(self.experiment_name)
        except Exception as e:
            logger.error(f"Failed to set up experiment: {str(e)}")
            raise

    def register_model(self, 
                      model_path: str,
                      metrics: Dict[str, float],
                      params: Dict[str, Any],
                      description: str = "") -> str:
        """Register a new model version with MLflow"""
        try:
            with mlflow.start_run():
                # Log parameters
                mlflow.log_params(params)
                
                # Log metrics
                mlflow.log_metrics(metrics)
                
                # Log model
                mlflow.pytorch.log_model(
                    pytorch_model=model_path,
                    artifact_path="model",
                    registered_model_name="style_transfer"
                )
                
                # Log description
                if description:
                    mlflow.set_tag("description", description)
                
                # Log timestamp
                mlflow.set_tag("timestamp", datetime.now().isoformat())
                
                run_id = mlflow.active_run().info.run_id
                logger.info(f"Model registered successfully with run_id: {run_id}")
                return run_id
                
        except Exception as e:
            logger.error(f"Failed to register model: {str(e)}")
            raise

    def get_latest_model(self) -> Optional[str]:
        """Get the latest model version from the registry"""
        try:
            client = mlflow.tracking.MlflowClient()
            latest_versions = client.get_latest_versions("style_transfer")
            
            if not latest_versions:
                logger.warning("No model versions found in registry")
                return None
                
            latest = latest_versions[0]
            logger.info(f"Latest model version: {latest.version}")
            return latest.source
            
        except Exception as e:
            logger.error(f"Failed to get latest model: {str(e)}")
            return None

    def get_model_metrics(self, run_id: str) -> Dict[str, float]:
        """Get metrics for a specific model version"""
        try:
            client = mlflow.tracking.MlflowClient()
            run = client.get_run(run_id)
            return run.data.metrics
            
        except Exception as e:
            logger.error(f"Failed to get model metrics: {str(e)}")
            return {}

    def compare_models(self, run_id1: str, run_id2: str) -> Dict[str, Any]:
        """Compare two model versions"""
        try:
            client = mlflow.tracking.MlflowClient()
            run1 = client.get_run(run_id1)
            run2 = client.get_run(run_id2)
            
            comparison = {
                'metrics_diff': {},
                'params_diff': {}
            }
            
            # Compare metrics
            for metric in run1.data.metrics:
                if metric in run2.data.metrics:
                    comparison['metrics_diff'][metric] = {
                        'run1': run1.data.metrics[metric],
                        'run2': run2.data.metrics[metric],
                        'diff': run1.data.metrics[metric] - run2.data.metrics[metric]
                    }
            
            # Compare parameters
            for param in run1.data.params:
                if param in run2.data.params:
                    comparison['params_diff'][param] = {
                        'run1': run1.data.params[param],
                        'run2': run2.data.params[param]
                    }
            
            return comparison
            
        except Exception as e:
            logger.error(f"Failed to compare models: {str(e)}")
            return {}

    def promote_model(self, run_id: str, stage: str = "Production") -> bool:
        """Promote a model version to a specific stage"""
        try:
            client = mlflow.tracking.MlflowClient()
            client.transition_model_version_stage(
                name="style_transfer",
                version=run_id,
                stage=stage
            )
            logger.info(f"Model {run_id} promoted to {stage}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to promote model: {str(e)}")
            return False 