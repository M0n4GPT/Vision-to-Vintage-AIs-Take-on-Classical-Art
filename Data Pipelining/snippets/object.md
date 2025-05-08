# Artwork ETL Pipeline Documentation
**Overview**
This ETL pipeline processes the Best Artworks of All Time dataset from Kaggle. The pipeline is built with Docker Compose and includes three stages:
* **Extract**: Downloads and unzips the dataset.
* **Transform**: Splits the dataset into train/val/test.
* **Load**: Uploads processed data to an object store on Chameleon Cloud.

**Files & Structure**
* docker-compose-etl.yaml: Main Compose file defining all ETL services.
* artwork volume: Shared volume for staging dataset files.
* .config/rclone/rclone.conf: Mount point for object storage credentials.
* Data will be loaded into the object store container named: object-persist-project35.

| Component        | Tool / Image Used              |
| ---------------- | ------------------------------ |
| Containerization | `docker-compose`               |
| Language         | Python 3.11                    |
| Library          | `pillow`, `numpy`              |
| Storage Upload   | `rclone` official Docker image |
| Dataset Source   | Kaggle API (via `curl`)        |

## **How to Run**
setting up rclone path "Vision-to-Vintage-AIs-Take-on-Classical-Art/Data Pipelining/object_storage_setup
/setup_steps.md"

Step 2: Set up environment
```bash
export RCLONE_CONTAINER=object-persist-<yourNetID>
```

Step 3:Run each pipeline stage
```bash
docker compose -f Data\ Pipelining/docker/docker-compose-etl.yaml run extract-data
docker compose -f Data\ Pipelining/docker/docker-compose-etl.yaml run transform-data
docker compose -f Data\ Pipelining/docker/docker-compose-etl.yaml run load-data
```


**Output**
* After extraction: /data/images_only/ contains original folders (50 artists).
* After transformation: /data/processed/{train,val,test}/<artist_name>/ contains split and copied images.
* After loading: The processed folder is uploaded to object storage.

