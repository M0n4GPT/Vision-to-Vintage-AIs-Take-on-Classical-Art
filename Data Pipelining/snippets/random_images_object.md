# Random Image Dataset ETL Pipeline Documentation

**Overview**
This ETL pipeline processes a generic random image dataset from kaggle. The pipeline is built with Docker Compose and includes three stages:

* **Extract**: Pulls the zipped dataset from a remote source.
* **Transform**: Splits the dataset into train/val/test.
* **Load**: Uploads the processed data into the object store using Rclone.

---

## ETL Pipeline

**1. Extract**
Downloads the dataset zip file via `curl`, unzips it, and places the folder under `random_images_only/`.

```yaml
  extract-random:
    container_name: etl_extract_random
    image: python:3.11
    user: root
    volumes:
      - random_images:/data
    working_dir: /data
    command:
      - bash
      - -c
      - |
        set -e

        echo "Resetting dataset directory..."
        rm -rf RandomRaw random_images_only
        mkdir -p RandomRaw
        cd RandomRaw

        echo "Downloading random image dataset using curl..."
        curl -L -o random-image-sample-dataset.zip https://www.kaggle.com/api/v1/datasets/download/pankajkumar2002/random-image-sample-dataset

        echo "Unzipping dataset..."
        unzip -q random-image-sample-dataset.zip
        rm -f random-image-sample-dataset.zip

        echo "Moving contents to /data/random_images_only..."
        mv * /data/random_images_only
        cd ..
        rm -rf RandomRaw

        echo "Listing contents of /data/random_images_only after extract stage:"
        ls -l /data/random_images_only
```

**2. Transform**
Splits into train/val/test

```yaml
  transform-random:
    container_name: etl_transform_random
    image: python:3.11
    volumes:
      - random_images:/data
    working_dir: /data
    command:
      - bash
      - -c
      - |
        set -e

        echo "Installing required libraries..."
        pip install pillow numpy

        echo "Running transform script..."
        python3 -c '
        import os
        import random
        import shutil

        RAW_DIR = "/data/random_images_only"
        OUT_DIR = "/data/random_split"
        SPLITS = ["random_train", "random_val", "random_test"]
        SPLIT_RATIOS = [0.7, 0.15, 0.15]

        if not os.path.exists(RAW_DIR):
            raise Exception(f"Missing raw data at {RAW_DIR}")

        os.makedirs(OUT_DIR, exist_ok=True)

        images = [f for f in os.listdir(RAW_DIR) if f.lower().endswith((".jpg", ".png", ".jpeg"))]
        random.shuffle(images)

        n_total = len(images)
        n_train = int(SPLIT_RATIOS[0] * n_total)
        n_val = int(SPLIT_RATIOS[1] * n_total)
        n_test = n_total - n_train - n_val

        print(f"Total random images: {n_total}")

        split_map = {
            "random_train": images[:n_train],
            "random_val": images[n_train:n_train+n_val],
            "random_test": images[n_train+n_val:]
        }

        for split in SPLITS:
            split_dir = os.path.join(OUT_DIR, split)
            os.makedirs(split_dir, exist_ok=True)
            for fname in split_map[split]:
                shutil.copy2(os.path.join(RAW_DIR, fname), os.path.join(split_dir, fname))
        '

        echo "Listing contents of /data/random_split after transform stage:"
        ls -l /data/random_split
```

**3. Load**
Uploads processed folders to the object store.

```yaml
  load-random:
    container_name: etl_load_random
    image: rclone/rclone:latest
    volumes:
      - random_images:/data
      - ~/.config/rclone/rclone.conf:/root/.config/rclone/rclone.conf:ro
    entrypoint: /bin/sh
    command:
      - -c
      - |
        if [ -z "$RCLONE_CONTAINER" ]; then
          echo "ERROR: RCLONE_CONTAINER is not set"
          exit 1
        fi

        echo "Uploading random image data..."
        rclone copy /data/random_split chi_tacc:$RCLONE_CONTAINER/random_inputs \
          --progress \
          --transfers=32 \
          --checkers=16 \
          --multi-thread-streams=4 \
          --fast-list

        echo "Listing uploaded directories in object store:"
        rclone lsd chi_tacc:$RCLONE_CONTAINER/random_inputs
```

---

## Run the Pipeline

```bash
cd ~/Vision-to-Vintage-AIs-Take-on-Classical-Art/Data\ Pipelining/docker
export RCLONE_CONTAINER=object-persist-project35

docker compose -f docker_compose_random_images_etl.yaml run extract-random
docker compose -f docker_compose_random_images_etl.yaml run transform-random
docker compose -f docker_compose_random_images_etl.yaml run load-random
```
