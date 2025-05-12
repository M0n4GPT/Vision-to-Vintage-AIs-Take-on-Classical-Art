
# Using Ray Train

## Stop MLFlow system
Stop the MLFlow tracking server and its associated pieces (database, object store) with

```bash
# run on node-mltrain
docker compose -f style_transfer/docker/docker-compose-mlflow.yaml down
```
and then stop the Jupyter server with

```bash
# run on node-mltrain
docker stop jupyter
```

## Start the Ray cluster
### Understand the Ray cluster


- We will operate a Ray cluster with a head node (responsible for scheduling and managing jobs and data, and serving a dashboard), and two worker nodes.
- For observability, the Ray head node uses [Prometheus](https://prometheus.io/) to collect metrics, and [Grafana](https://grafana.com/) to visualize them in a dashboard.
- The Ray worker nodes will use the MinIO object store for persistent storage from jobs. We will save model checkpoints in this MinIO storage, so that if a job is interrupted, a new Ray worker can resume from the last checkpoint.
- In addition to the elements that make up the Ray cluster, we will separately bring up a Jupyter notebook server container, in which we'll submit jobs to the cluster.


### Start the Ray cluster - AMD(gpu_mi100) GPUs
For the Ray experiment, must use a node with two GPUs. Run

```bash
# run on nodedocker stop jupyter
rocm-smi
```
and confirm that you see two GPUs.

First, we're going to build a container image for the Ray worker nodes, with Ray and ROCm installed. Run

```bash
# run on node
docker build -t ray-rocm:2.42.1 -f style_transfer/docker/Dockerfile.ray-rocm .
```

It will take 5-10 minutes to build the container image.

You can see this Dockerfile here: [Dockerfile.ray-rocm](https://github.com/M0n4GPT/vision-to-vintage/blob/master/style_transfer/docker/Dockerfile.ray-rocm).


We'll bring up our Ray cluster with Docker Compose. Run:

```bash
# run on node
export HOST_IP=$(curl --silent http://169.254.169.254/latest/meta-data/public-ipv4 )
docker compose -f style_transfer/docker/docker-compose-ray-rocm.yaml up -d
```

You can see this Docker Compose YAML here: [docker-compose-ray-rocm.yaml](https://github.com/M0n4GPT/vision-to-vintage/blob/master/style_transfer/docker/docker-compose-ray-rocm.yaml).


When it is finished, the output of 

```bash
# run on node
docker ps
```

should show that the `ray-head`, `ray-worker-0`, and `ray-worker-1` containers are running.

Verify that a GPU is visible to each of the worker nodes.

```bash
# run on node
docker exec ray-worker-0 "rocm-smi"
```

and

```bash
# run on node
docker exec ray-worker-1 "rocm-smi"
```

### Start a Jupyter container

Start a Jupyter notebook container that does *not* have any GPUs attached. We'll use this container to submit jobs to the Ray cluster.


```bash
# run on node
docker build -t jupyter-ray -f style_transfer/docker/Dockerfile.jupyter-ray .
```

Run

```bash
# run on node
HOST_IP=$(curl --silent http://169.254.169.254/latest/meta-data/public-ipv4 )
docker run  -d --rm  -p 8888:8888 \
    -v ~/style_transfer:/home/jovyan/work/ \
    -e RAY_ADDRESS=http://${HOST_IP}:8265/ \
    -e IMG_DATA_DIR=/project35 \
    --mount type=bind,source=/home/cc/project35,target=/project35,readonly \
    --name jupyter \
    jupyter-ray
```


Then, run 

```bash
# run on node-mltrain
docker logs jupyter
```

and look for a line like

```
http://127.0.0.1:8888/lab?token=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

Paste this into a browser tab, but in place of `127.0.0.1`, substitute the floating IP assigned to your instance, to open the Jupyter notebook interface.

In the file browser on the left side, open the `work` directory.

Open a terminal ("File > New > Terminal") inside the Jupyter server environment, and in this terminal, run

```bash
# runs on jupyter container inside node-mltrain
env
```

to see environment variables. Confirm that the `RAY_ADDRESS` is set, with the correct floating IP address.

### Access Ray cluster dashboard

The Ray head node serves a dashboard on port 8265. In a browser, open

```
http://A.B.C.D:8265
```


Click on the "Cluster" tab and verify that you see your head node and two worker nodes.

## Submit jobs to the Ray cluster

Now that we have a Ray cluster running, we can use it to specify the resource requirements and runtime environment for a job, and submit it to Ray. 

### Submit a job with no modifications

To start, submit a training job to Ray cluster, without modifying the code of our training job at all.

Open a terminal inside this Jupyter environment ("File > New > New Terminal") and `cd` to the `work` directory. Then, clone the training code.

```bash
# run in a terminal inside jupyter container
cd ~/work
# git clone https://github.com/M0n4GPT/vision-to-vintage/ray
```

Open `train_ray.py`, and view it directly there.


To run it on a worker node, though, we must give Ray some instructions about how to set up the runtime environment on the worker nodes. Two files necessary for this, `requirements.txt` and `runtime.json`, are inside the "work" directory:

* We assume that the worker nodes already have the img dataset at `/project35`, since we attached our data volume to those containers. So we don't have to worry about getting the data to the worker node in this case. We will have to make sure that the environment variable `IMG_DATA_DIR` is set, so that the training script can find the data. (In general, we will need to make sure that either worker nodes have access to the data, or they download it at the beginning of the training job.)
* We need to make sure that the worker nodes have the Python packages necessary to run our script. We'll put the list of packages in `requirements.txt`.
* And, we need to direct Ray to run this on a GPU node.

In `runtime.json`:

```json
{
    "pip": "requirements.txt",
    "env_vars": {
        "IMG_DATA_DIR": "/project35"
    }
}
```

we specify that when setting up a worker node to run our job, Ray should:

* install the Python packages listed in `requirements.txt`
* and set the `IMG_DATA_DIR` directory.

With this in hand, we can submit our job! In a terminal inside the Jupyter environment, run `pip install "ray[default]"` first, then


```bash
# runs on jupyter container inside node-mltrain, from inside the "work" directory
ray job submit --runtime-env runtime.json --entrypoint-num-gpus 1 --entrypoint-num-cpus 8 --verbose  --working-dir .  -- python3 train_style_transfer.py \
    --data_root "$IMG_DATA_DIR" \
    --global_batch_size 32 \
    --micro_batch_size 8 \
    --epochs 5 \
    --precision fp32 \
    --strategy none \
    --export_path ./stylizer.pt
```

where we pass 

* the runtime environment specification, 
* the number of GPUs and CPUs our job requires, 
* we specify that we would like to see verbose output, 
* that the current working directory should be packaged up and shipped to the worker nodes,
* and that the command to run is: `python xxx.py`.

While it is running, click on the "Overview", "Cluster", and "Jobs" tabs in the Ray dashboard.

* Initially, the job will be a in PENDING state, as the runtime environment is set up. This is slow the first time (because of downloading the Python packages), but faster in subsequent runs because the packages are cached on the workers.
Let the training job finish, and get to SUCCEEDED state. (This may take up to 10-15 minutes.)


### Submit an infeasible job

If we submit a job for which there is no node that satisfies the resource requirements. Run

```bash
# runs on jupyter container inside node-mltrain, from inside the "work" directory
ray job submit --runtime-env runtime.json --entrypoint-num-gpus 2 --entrypoint-num-cpus 8 --verbose  --working-dir .  -- python3 train_style_transfer.py \
    --data_root "$IMG_DATA_DIR" \
    --global_batch_size 32 \
    --micro_batch_size 8 \
    --epochs 5 \
    --precision fp32 \
    --strategy none \
    --export_path ./stylizer.pt
```

noting that we have no node with 2 GPUs - only two nodes, each with 1 GPU. 

In the Ray dashboard "Overview" page, observe that this request is listed in "Demands" in the "Resource Status" section.

The job will be stuck in PENDING state until we add a node with 2 GPUs to the cluster, at which time it can be scheduled.

In a commercial cloud, when deployed with Kubernetes, a Ray cluster could [autoscale](https://docs.ray.io/en/latest/cluster/vms/user-guides/configuring-autoscaling.html) in this situation to accommodate the demand that could not be satisfied. Our cluster is not auto-scaling and we are not going to add a node with 2 GPUs, so this job will wait forever.

Use Ctrl+C to stop the process in the Jupyter terminal. (The job is still submitted and PENDING, but not consuming worker resources, since it cannot be scheduled.)







