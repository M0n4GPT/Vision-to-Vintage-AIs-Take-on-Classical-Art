## Save the Production data

Goal: Whenever a user uploads an image: Save it to a production bucket in MinIO

**Create a production_net Docker network**
```bash
docker network create production_net
```
This ensures all services (MinIO + Flask) can talk using container names.

**Create docker-compose-production.yaml**
```bash
name: production

services:
  vision_to_vintage:
    build:
      context: /home/cc/Vision-to-Vintage-AIs-Take-on-Classical-Art/ModelTraining/vision-to-vintage
      dockerfile: Dockerfile
    container_name: vision_to_vintage
    ports:
      - "9190:9090"
    environment:
      - MINIO_URL=http://minio:9060
      - MINIO_USER=minioadmin
      - MINIO_PASSWORD=minioadmin123
    networks:
      - production_net
    depends_on:
      - minio

  minio:
    image: minio/minio
    container_name: minio
    ports:
      - "9060:9000"
      - "9001:9001"
    environment:
      - MINIO_ROOT_USER=minioadmin
      - MINIO_ROOT_PASSWORD=minioadmin123
    volumes:
      - minio_data:/data
    command: server /data --console-address ':9001'
    networks:
      - production_net

  minio-init:
    image: minio/mc
    container_name: minio_init
    depends_on:
      - minio
    restart: "no"
    entrypoint: >
      /bin/sh -c "
      sleep 5 &&
      mc alias set myminio http://minio:9000 minioadmin minioadmin123 &&
      mc mb -p myminio/production || echo 'Bucket already exists'
      "
    networks:
      - production_net

networks:
  production_net:
    external: true

volumes:
  minio_data:

```

**Modify Your app.py in Vision-to-Vintage**
Add dependencies
In your requirements.txt:
```bash
boto3
```

**In app.py (top level)**
```bash
import boto3
from mimetypes import guess_type
from datetime import datetime
import uuid
from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=2)

s3 = boto3.client(
    's3',
    endpoint_url=os.environ['MINIO_URL'],
    aws_access_key_id=os.environ['MINIO_USER'],
    aws_secret_access_key=os.environ['MINIO_PASSWORD'],
    region_name='us-east-1'
)
```

**Add the upload function**
```python
def upload_to_production_bucket(img_path, style_used, prediction_id):
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    content_type = guess_type(img_path)[0] or 'application/octet-stream'
    ext = os.path.splitext(img_path)[-1]
    s3_key = f"{style_used}/{prediction_id}{ext}"

    with open(img_path, 'rb') as f:
        s3.upload_fileobj(f, "production", s3_key, ExtraArgs={'ContentType': content_type})

    s3.put_object_tagging(
        Bucket="production",
        Key=s3_key,
        Tagging={
            'TagSet': [
                {'Key': 'style', 'Value': style_used},
                {'Key': 'timestamp', 'Value': timestamp}
            ]
        }
    )
```

**Trigger it in your route**
Right after you save the stylized output:
```python
prediction_id = str(uuid.uuid4())
executor.submit(upload_to_production_bucket, out_path, author, prediction_id)
```

**Run your production stack**
```bash
docker compose -f docker-compose-production.yaml up -d
```

**Open & Test**
Website: http://129.114.25.100:9090
MinIO Console: http://129.114.25.100:9060
(login: minioadmin / minioadmin123, open "production" bucket)


