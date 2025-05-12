from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Vision to Vintage"
    VERSION: str = "1.0.0"
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4
    DEBUG: bool = False
    
    # Model settings
    MODEL_PATH: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "style_transfer_model.pt")
    CANARY_MODEL_PATH: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "canary_style_transfer_model.pt")
    CANARY_ENABLED: bool = False
    CANARY_TRAFFIC_PERCENTAGE: float = 10.0
    
    # MLflow settings
    MLFLOW_TRACKING_URI: str = "http://localhost:5000"
    MLFLOW_TRACKING_USERNAME: str = "admin"
    MLFLOW_TRACKING_PASSWORD: str = "admin"
    MLFLOW_EXPERIMENT_NAME: str = "vision-to-vintage"
    
    # MinIO settings
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_SECURE: bool = False
    MINIO_FEEDBACK_BUCKET: str = "feedback"
    
    # Monitoring settings
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    PROMETHEUS_MULTIPROC_DIR: Optional[str] = None
    
    # Data settings
    DATA_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    STYLES_DIR: str = os.path.join(DATA_DIR, "styles")
    METRICS_DIR: str = os.path.join(DATA_DIR, "metrics")
    
    # Model optimization settings
    MODEL_OPTIMIZATION_ENABLED: bool = True
    QUANTIZATION_ENABLED: bool = True
    TORCHSCRIPT_ENABLED: bool = True
    CUDA_OPTIMIZATIONS_ENABLED: bool = True
    
    # Evaluation settings
    EVALUATION_THRESHOLD: float = 0.7
    DRIFT_THRESHOLD: float = 0.5
    FEEDBACK_COLLECTION_ENABLED: bool = True
    
    class Config:
        case_sensitive = True
        env_file = ".env"

# Create settings instance
settings = Settings()

# Create necessary directories
os.makedirs(settings.DATA_DIR, exist_ok=True)
os.makedirs(settings.STYLES_DIR, exist_ok=True)
os.makedirs(settings.METRICS_DIR, exist_ok=True) 