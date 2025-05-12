"""
MinIO client module for Vision-to-Vintage application.
Provides connection to MinIO object storage for storing and retrieving data.
"""
import os
import time
import logging
from minio import Minio
from minio.error import S3Error
from pathlib import Path
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global client instance for reuse
_minio_client = None

def get_minio_client():
    """
    Get a MinIO client with connection retry logic.
    """
    global _minio_client
    
    # Return existing client if available
    if _minio_client is not None:
        return _minio_client
    
    # Get connection details from environment
    minio_endpoint = os.environ.get("MINIO_ENDPOINT", "minio:9000")
    minio_user = os.environ.get("MINIO_USER", "minioadmin")
    minio_password = os.environ.get("MINIO_PASSWORD", "minioadmin")
    
    logger.info(f"Connecting to MinIO at {minio_endpoint}")
    
    # Create client instance
    client = Minio(
        minio_endpoint,
        access_key=minio_user,
        secret_key=minio_password,
        secure=False  # Set to True if using HTTPS
    )
    
    # Try to connect with retries
    for attempt in range(5):
        try:
            # Verify connection by listing buckets
            client.list_buckets()
            logger.info("Successfully connected to MinIO")
            _minio_client = client
            return client
        except Exception as e:
            if attempt < 4:
                wait_time = 2 ** attempt  # Exponential backoff
                logger.warning(f"Failed to connect to MinIO (attempt {attempt+1}/5): {str(e)}")
                logger.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                logger.error(f"Failed to connect to MinIO after 5 attempts: {str(e)}")
                return client  # Return client anyway, might succeed later
    
    return client

def ensure_bucket_exists(bucket_name: str) -> bool:
    """
    Ensure a bucket exists, creating it if necessary.
    
    Args:
        bucket_name: Name of the bucket to check/create
        
    Returns:
        True if bucket exists or was created successfully
    """
    client = get_minio_client()
    
    try:
        if not client.bucket_exists(bucket_name):
            logger.info(f"Creating bucket: {bucket_name}")
            client.make_bucket(bucket_name)
            logger.info(f"Successfully created bucket: {bucket_name}")
        return True
    except S3Error as e:
        logger.error(f"Error checking/creating bucket {bucket_name}: {e}")
        return False

def get_object_url(bucket_name: str, object_name: str, expires: int = 7*24*60*60) -> Optional[str]:
    """
    Get a presigned URL for an object.
    
    Args:
        bucket_name: Name of the bucket
        object_name: Name of the object
        expires: Expiration time in seconds (default: 7 days)
        
    Returns:
        Presigned URL or None if failed
    """
    client = get_minio_client()
    
    try:
        return client.presigned_get_object(bucket_name, object_name, expires=expires)
    except Exception as e:
        logger.error(f"Error generating presigned URL for {bucket_name}/{object_name}: {e}")
        return None

class MinioClient:
    def __init__(self):
        self.client = get_minio_client()
        self.bucket_name = "mlflow-artifacts"
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        """Ensure the required bucket exists"""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                logger.info(f"Created bucket: {self.bucket_name}")
        except S3Error as e:
            logger.error(f"Error ensuring bucket exists: {str(e)}")
            raise

    def upload_file(self, file_path: str, object_name: str = None):
        """Upload a file to MinIO"""
        try:
            if object_name is None:
                object_name = Path(file_path).name
            
            self.client.fput_object(
                self.bucket_name,
                object_name,
                file_path
            )
            logger.info(f"Uploaded {file_path} to {object_name}")
            return f"s3://{self.bucket_name}/{object_name}"
        except S3Error as e:
            logger.error(f"Error uploading file: {str(e)}")
            raise

    def download_file(self, object_name: str, file_path: str):
        """Download a file from MinIO"""
        try:
            self.client.fget_object(
                self.bucket_name,
                object_name,
                file_path
            )
            logger.info(f"Downloaded {object_name} to {file_path}")
        except S3Error as e:
            logger.error(f"Error downloading file: {str(e)}")
            raise

    def list_files(self, prefix: str = ""):
        """List files in the bucket with optional prefix"""
        try:
            objects = self.client.list_objects(
                self.bucket_name,
                prefix=prefix,
                recursive=True
            )
            return [obj.object_name for obj in objects]
        except S3Error as e:
            logger.error(f"Error listing files: {str(e)}")
            raise

    def delete_file(self, object_name: str):
        """Delete a file from MinIO"""
        try:
            self.client.remove_object(
                self.bucket_name,
                object_name
            )
            logger.info(f"Deleted {object_name}")
        except S3Error as e:
            logger.error(f"Error deleting file: {str(e)}")
            raise 