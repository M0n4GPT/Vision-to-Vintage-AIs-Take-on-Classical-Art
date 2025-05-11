::: {.cell .markdown}

## Utilizing Block Storage for Persistent Data Management

we leverage block storage volumes on Chameleon Cloud, which offer persistent storage independent of any single compute instance. This approach allows us to:
* Create a block storage volume at KVM@TACC
* Attach it to a compute instance
* Format and mount it with a filesystem
* Utilize it as a Docker volume for containerized applications
* Detach and reattach it to new instances as needed

By integrating block storage into our workflow, we ensure that critical data remains intact across sessions, facilitating a more robust and flexible research environment.
:::

::: {.cell .markdown}

### Block storage using the Horizon GUI

First, let's try creating a block storage volume from the OpenStack Horizon GUI. Open the GUI for KVM@TACC:

* from the [Chameleon website](https://chameleoncloud.org/hardware/)
* click "Experiment" > "KVM@TACC"
* log in if prompted to do so
* check the project drop-down menu near the top left (which shows e.g. "CHI-XXXXXX"), and make sure the correct project is selected.

In the menu sidebar on the left side, click on "Volumes" > "Volumes" and then, "Create Volume". You will be prompted to set up your volume step by step using a graphical "wizard".

* Specify the name as <code>block-persist-<b>project35</b></code>
* Specify the size as 5 GiB.
* Leave other settings at their defaults, and click "Create Volume".

Next, it's time to to attach the block storage volume to the compute instance we created earlier. From  "Volumes" > "Volumes", next to *your* volume, click the ▼ in the menu on the right and choose "Manage Attachments". In the "Attach to Instance" menu, choose your compute instance. Then, click "Attach Volume".

Now, the "Volumes" overview page in the Horizon GUI should show something like for your volume:

```
| Name                | Description | Size | Status | Group | Type     | Attached To                     | Availability Zone | Bootable | Encrypted |
|---------------------|-------------|------|--------|-------|----------|---------------------------------|-------------------|----------|-----------|
| block-persist-project35 | -           | 5GiB | In-use | -     | ceph-ssd | /dev/vdb on node-persist-netID  | nova              | No       | No        |
```

On the instance, let's confirm that we can see the block storage volume. Run

```bash
lsblk
```

and verify that `vdb` appears in the output.

The volume is essentially a raw disk. Before we can use it **for the first time** after creating it, we need to partition the disk, create a filesystem on the partition, and mount it. In subsequent uses, we will only need to mount it.

> **Note**: if the volume already had data on it, creating a filesystem on it would erase all its data! This procedure is *only* for the initial setup of a volume, before it has any data on it.

First, we create a partition with an `ext4` filesystem, occupying the entire volume:

```bash
sudo parted -s /dev/vdb mklabel gpt
sudo parted -s /dev/vdb mkpart primary ext4 0% 100%
```

Verify that we now have the partition `vdb1` in the output of 

```bash
lsblk
```

Next, we format the partition:

```bash
sudo mkfs.ext4 /dev/vdb1
```

Finally, we can create a directory in the local filesystem, mount the partition to that directory:

```bash
sudo mkdir -p /mnt/block
sudo mount /dev/vdb1 /mnt/block
```

and change the owner of that directory to the `cc` user:

```bash
sudo chown -R cc /mnt/block
sudo chgrp -R cc /mnt/block
```

Run

```bash
df -h
```

and verify that the output includes a line with `/dev/vdb1` mounted on `/mnt/block`:

```
Filesystem      Size  Used Avail Use% Mounted on
/dev/vdb1       2.0G   24K  1.9G   1% /mnt/block
```

:::


::: {.cell .markdown}

## Create Docker Volumes on Persistent Block Storage

In this project, we are building a style transfer system that transforms input images into the style of famous artists. To ensure the model training environment is persistent across VM restarts, we configure key ML platform services (MLFlow, PostgreSQL, MinIO, and Jupyter) to use Chameleon Cloud’s persistent block storage.

Our goal is to:

1. Log all experiments using MLFlow
2. Store model parameters and metrics in PostgreSQLSave model artifacts in MinIO
3. Train and evaluate our models in JupyterLab

All these services will use mounted block storage directories to persist data across instance shutdowns.

### Prepare Persistent Storage Directories
The persistent volume was mounted at:
```bash
/mnt/block/
```

These folders serve as volume mounts for our PostgreSQL and MinIO services.

### Configure Docker Compose

We use Docker Compose to bring up the following services:
* mlflow: Experiment tracking service
* postgres: Backend database for MLFlow
* minio: Object store for saving model files/artifacts
* jupyter: Interactive notebook server

The Docker Compose file is located at:
```bash
 cd ~/Vision-to-Vintage-AIs-Take-on-Classical-Art/Data\ Pipelining
```
Bring the services:
```bah
HOST_IP=$(curl --silent http://169.254.169.254/latest/meta-data/public-ipv4)
```

Run the services:
```bash
docker compose -f docker/docker-compose-block.yaml up -d
```
You should see all services starting with status Running or Healthy.

![image](https://github.com/user-attachments/assets/39fd5516-f14b-4e52-8d57-4b9f1228d166)

### Open Services in Browser

To make the services accessible from your browser, open the following ports in your Chameleon Cloud security group:

| Service    | Port | Example URL                     |
| ---------- | ---- | ------------------------------- |
| MLFlow     | 8000 | http\://YOUR\_FLOATING\_IP:8000 |
| JupyterLab | 8888 | http\://YOUR\_FLOATING\_IP:8888 |
| MinIO      | 9000 | http\://YOUR\_FLOATING\_IP:9000 |


Example:
If our floating IP is 129.114.25.100:

MLFlow: http://129.114.25.100:8000

MinIO: http://129.114.25.100:9000

Jupyter: http://129.114.25.100:8888

### Tracking ML Experiments with MLFlow
Once Jupyter is running, we can log experiments by adding the following snippet to any notebook that evaluates or trains a model:

```
import mlflow
import mlflow.pytorch

mlflow.set_experiment("style-transfer-artwork")

with mlflow.start_run():
    mlflow.log_metric("eval_accuracy", overall_accuracy)
    mlflow.pytorch.log_model(model, "style_transfer_model")

```

This will:

* Log the evaluation metric (overall_accuracy) to PostgreSQL

* Save the trained model to MinIO, under the mlflow bucket
