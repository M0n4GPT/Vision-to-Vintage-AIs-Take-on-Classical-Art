#!/usr/bin/env python
import logging
from minio import Minio
from minio.error import S3Error
import time
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# MinIO client setup
def get_minio_client(retries=5):
    """Get a connected MinIO client with retries."""
    minio_endpoint = os.environ.get("MINIO_ENDPOINT", "minio:9000")
    minio_user = os.environ.get("MINIO_USER", "minioadmin")
    minio_password = os.environ.get("MINIO_PASSWORD", "minioadmin")
    
    client = Minio(
        minio_endpoint,
        access_key=minio_user,
        secret_key=minio_password,
        secure=False
    )
    
    # Try to connect with retries
    for attempt in range(retries):
        try:
            logger.info(f"Connecting to MinIO at {minio_endpoint} (attempt {attempt+1}/{retries})")
            # Test connection with a list_buckets call
            client.list_buckets()
            logger.info("Successfully connected to MinIO")
            return client
        except Exception as e:
            logger.warning(f"Failed to connect to MinIO: {str(e)}")
            if attempt < retries - 1:
                sleep_time = 2 ** attempt  # Exponential backoff
                logger.info(f"Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
            else:
                logger.error("All connection attempts failed")
                raise
    
    return client

def create_buckets():
    """Create all required buckets."""
    try:
        client = get_minio_client()
        
        # Define buckets to create
        required_buckets = ["feedback", "metrics", "drift"]
        
        for bucket in required_buckets:
            try:
                if not client.bucket_exists(bucket):
                    logger.info(f"Creating bucket: {bucket}")
                    client.make_bucket(bucket)
                    logger.info(f"Successfully created bucket: {bucket}")
                else:
                    logger.info(f"Bucket already exists: {bucket}")
            except S3Error as e:
                logger.error(f"Error creating bucket {bucket}: {e}")
        
        logger.info("All required buckets created")
        
    except Exception as e:
        logger.error(f"Failed to create buckets: {str(e)}")
        raise

if __name__ == "__main__":
    logger.info("Starting MinIO bucket initialization")
    create_buckets()
    logger.info("MinIO bucket initialization completed") 