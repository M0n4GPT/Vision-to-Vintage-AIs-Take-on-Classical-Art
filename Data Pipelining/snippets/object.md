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


::: {.cell .markdown}

## Using object storage
### Object storage using the Horizon GUI

First, let's try creating an object storage container from the OpenStack Horizon GUI. 

Open the GUI for CHI@TACC:

* from the [Chameleon website](https://chameleoncloud.org/hardware/)
* click "Experiment" > "CHI@TACC"
* log in if prompted to do so
* check the project drop-down menu near the top left (which shows e.g. "CHI-XXXXXX"), and make sure the correct project is selected.

In the menu sidebar on the left side, click on "Object Store" > "Containers" and then, "Create Container". You will be prompted to set up your container step by step using a graphical "wizard".

* Specify the name as <code>object-persist-<b>project35</b></code> 
* Leave other settings at their defaults, and click "Submit".

:::

::: {.cell .markdown}

### Use `rclone` and authenticate to object store from a compute instance

We will want to connect to this object store from the compute instance we configured earlier, and copy some data to it!

For *write* access to the object store from the compute instance, we will need to authenticate with valid OpenStack credentials. To support this, we will create an *application credential*, which consists of an ID and a secret that allows a script or application to authenticate to the service. 

An application credential is a good way for something like a data pipeline to authenticate, since it can be used non-interactively, and can be revoked easily in case it is compromised without affecting the entire user account.

In the menu sidebar on the left side of the Horizon GUI, click "Identity" > "Application Credentials". Then, click "Create Application Credential".

**created Application Credentials**

Now that we have an application credential, we can use it to allow an application to authenticate to the Chameleon object store service. There are several applications and utilities for working with OpenStack's Swift object store service; we will use one called [`rclone`](https://github.com/rclone/rclone).


On the compute instance, install `rclone`:
```bash
# run on node-persist
curl https://rclone.org/install.sh | sudo bash
```

We also need to modify the configuration file for FUSE (**F**ilesystem in **USE**rspace: the interface that allows user space applications to mount virtual filesystems), so that object store containers mounted by our user will be availabe to others, including Docker containers:

```bash
# run on node-persist
# this line makes sure user_allow_other is un-commented in /etc/fuse.conf
sudo sed -i '/^#user_allow_other/s/^#//' /etc/fuse.conf
```

Next, create a configuration file for `rclone` with the ID and secret from the application credential you just generated:

```bash
# run on node-persist
mkdir -p ~/.config/rclone
nano  ~/.config/rclone/rclone.conf
```

Paste the following into the config file, but substitute your own application credential ID and secret. 

You will also need to substitute your own user ID. You can find it using "Identity" > "Users" in the Horizon GUI; it is an alphanumeric string (*not* the human-readable user name).


```
[chi_tacc]
type = swift
user_id = YOUR_USER_ID
application_credential_id = APP_CRED_ID
application_credential_secret = APP_CRED_SECRET
auth = https://chi.tacc.chameleoncloud.org:5000/v3
region = CHI@TACC
```


Use Ctrl+O and Enter to save the file, and Ctrl+X to exit `nano`.

To test it, run

```bash
# run on node-persist
rclone lsd chi_tacc:
```

and verify that you see your container listed. This confirms that `rclone` can authenticate to the object store.

:::

::: {.cell .markdown}

### Create a pipeline to load training data into the object store

Next, we will prepare a simple ETL pipeline to get the Artwork dataset into the object store. It will:

Extract the data into a staging area (local filesystem on the instance) by downloading and unzipping the dataset from Kaggle.

Transform the data by splitting it into train/val/test folders, each containing subdirectories for every artist—organized as required by PyTorch.

Load the processed dataset into the object store using rclone.

We are going to define the pipeline stages inside a Docker Compose file. All of the services in the container will share a common artwork volume. Then, we have:

1. A service to extract the Artwork dataset from the Internet.
This service runs a Python container image, downloads the dataset zip file from Kaggle using curl, unzips it, and keeps only the images/ folder. The data is saved into a shared artwork volume for downstream stages.

```
  extract-data:
    container_name: etl_extract_data
    image: python:3.11
    user: root
    volumes:
      - artwork:/data
    working_dir: /data
    command:
      - bash
      - -c
      - |
        set -e

        echo "Resetting dataset directory..."
        rm -rf ArtworkRaw images_only
        mkdir -p ArtworkRaw
        cd ArtworkRaw

        echo "Downloading dataset zip using curl..."
        curl -L -o best-artworks-of-all-time.zip https://www.kaggle.com/api/v1/datasets/download/ikarus777/best-artworks-of-all-time

        echo "Unzipping dataset..."
        unzip -q best-artworks-of-all-time.zip
        rm -f best-artworks-of-all-time.zip

        echo "Moving only 'images' folder to /data/images_only..."
        mv images /data/images_only
        cd ..
        rm -rf ArtworkRaw

        echo "Listing contents of /data/images_only after extract stage:"
        ls -l /data/images_only
```

2. A service that runs a Python container image, and uses a Python script to organize the artwork data into directories according to artist name.
The script reads the downloaded dataset, splits the images for each artist into training, validation, and test sets (70/15/15 split), and creates a PyTorch-compatible directory structure under a new processed/ folder inside the shared artwork volume.
Preprocessing: All images were resized to 224×224 pixels and normalized to ensure consistent input for model training.



```
  transform-data:
    container_name: etl_transform_data
    image: python:3.11
    volumes:
      - artwork:/data
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
        from PIL import Image
        import numpy as np

        RAW_DIR = "/data/images_only/images"
        OUT_DIR = "/data/processed"
        SPLITS = ["train", "val", "test"]
        SPLIT_RATIOS = [0.7, 0.15, 0.15]
        TARGET_SIZE = (224, 224)

        if not os.path.exists(RAW_DIR):
            raise Exception(f"Missing raw data at {RAW_DIR}")

        os.makedirs(OUT_DIR, exist_ok=True)

        top_level_dirs = [d for d in os.listdir(RAW_DIR) if os.path.isdir(os.path.join(RAW_DIR, d))]

        for artist in top_level_dirs:
            try:
                artist_path = os.path.join(RAW_DIR, artist)
                images = [f for f in os.listdir(artist_path) if f.lower().endswith((".jpg", ".png", ".jpeg"))]
                random.shuffle(images)

                n_total = len(images)
                n_train = int(SPLIT_RATIOS[0] * n_total)
                n_val = int(SPLIT_RATIOS[1] * n_total)
                n_test = n_total - n_train - n_val

                print(f"Processing artist: {artist} - total images: {n_total}")

                split_map = {
                    "train": images[:n_train],
                    "val": images[n_train:n_train+n_val],
                    "test": images[n_train+n_val:]
                }

                for split in SPLITS:
                    split_dir = os.path.join(OUT_DIR, split, artist)
                    os.makedirs(split_dir, exist_ok=True)
                    for fname in split_map[split]:
                        src = os.path.join(artist_path, fname)
                        dst = os.path.join(split_dir, fname)

                        try:
                            with Image.open(src) as img:
                                img = img.convert("RGB")
                                img = img.resize(TARGET_SIZE)
                                img.save(dst)
                        except Exception as e:
                            print(f"Failed to process image {src}: {e}")

            except Exception as e:
                print(f"Skipping artist {artist} due to error: {e}")
        '

        echo "Listing contents of /data/processed after transform stage:"
        ls -l /data/processed

```

3. And finally, a service that uses `rclone copy` to load the organized data into the object store. Note that we pass some arguments to `rclone copy` to increase the parallelism, so that the data is loaded more quicly. Also note that since the name of the container includes your individual net ID, we have specified it using an environment variable that must be set before this stage can run.

```
  load-data:
    container_name: etl_load_data
    image: rclone/rclone:latest
    volumes:
      - artwork:/data
      - ~/.config/rclone/rclone.conf:/root/.config/rclone/rclone.conf:ro
    entrypoint: /bin/sh
    command:
      - -c
      - |
        if [ -z "$RCLONE_CONTAINER" ]; then
          echo "ERROR: RCLONE_CONTAINER is not set"
          exit 1
        fi

        echo "Cleaning up existing contents of object store container..."
        rclone delete chi_tacc:$RCLONE_CONTAINER --rmdirs || true

        echo "Uploading processed dataset..."
        rclone copy /data/processed chi_tacc:$RCLONE_CONTAINER \
          --progress \
          --transfers=32 \
          --checkers=16 \
          --multi-thread-streams=4 \
          --fast-list

        echo "Listing directories in container after load stage:"
        rclone lsd chi_tacc:$RCLONE_CONTAINER
```

These services are defined in ~/Vision-to-Vintage-AIs-Take-on-Classical-Art/Data Pipelining/docker/docker-compose-etl.yaml.

Now, we can run the stages using Docker. (If we had a workflow orchestrator, we could use it to run the pipeline stages – but at this point, simple sequential execution is sufficient.)


```bash
cd ~/Vision-to-Vintage-AIs-Take-on-Classical-Art
docker compose -f "Data Pipelining/docker/docker-compose-etl.yaml" run extract-data
```

```bash
docker compose -f "Data Pipelining/docker/docker-compose-etl.yaml" run transform-data

```

```bash
# run on node-persist
export RCLONE_CONTAINER=object-persist-project35
docker compose -f "Data Pipelining/docker/docker-compose-etl.yaml" run load-data
```

Once the dataset is uploaded to the object store, it's ready for model training! You can now optionally clean up the Docker volume that was used as temporary staging:

```bash
docker volume rm artwork-etl_artwork
```

You can verify the upload through the Horizon GUI. The object store container is persistent and exists independently of any compute instance – meaning your data remains saved even if no instance is currently running.

:::

::: {.cell .markdown}

## Mount an object store to local file system
**Step 1: Create a Mount Point**
First, create a directory where the object store will be mounted:
```bash
sudo mkdir -p /mnt/project35
sudo chown -R cc /mnt/project35
sudo chgrp -R cc /mnt/project35
```
This sets up /mnt/object as the mount point with the appropriate permissions.

**Step 2: Mount the Object Store Using Rclone**
Assuming you've already configured rclone with a remote named chi_tacc, mount your object store container (e.g., object-persist_project35) to the mount point:
```bash
rclone mount chi_tacc:object-persist-project35 /mnt/project35 --read-only --allow-other --daemon
```
**Step 3: Verify the Mount**
Check that the mount was successful and that the expected directories (train, test, val) are present:
```bash
ls /mnt/project35
```
