# Model Training Proposal

## 1. Training Strategy

- **Distributed Data Parallel (DDP)**:
  - Implement DDP for multi-GPU training to speed up convergence for style transfer tasks.
  - Set up synchronization of gradients across GPUs during training.
  
- **Fully Sharded Data Parallel (FSDP)**:
  - Implement FSDP to shard model parameters across multiple GPUs.
  - Test with larger models for more complex artistic transformations.
  
- **Optimized Batch Sizing**:
  - Experiment with batch sizes ranging from **8 to 64** to evaluate the impact on memory efficiency and training speed.
  - Monitor convergence speed and model performance (accuracy and style transfer quality) with varying batch sizes.

## 2. Experiment Tracking

- **MLFlow Setup**:
  - Set up an **MLFlow tracking server** on Chameleon for logging training experiments.
  - Configure dashboards for real-time experiment monitoring.
  - Set up a Jupyter server to interactively analyze experiments.
  
- **Logging Metrics**:
  - Log **model parameters** (architecture, hyperparameters, optimizer).
  - Log **training metrics**: content loss, style loss, and classification accuracy.
  - Track comparative results of different training strategies and style transfer configurations.
  - Register models for version control and reusability.

## 3. Training Job Scheduling

- **Ray Cluster Setup**:
  - Deploy a **Ray cluster** on Chameleon, configured with **at least 2 GPUs** (NVIDIA V100 or A100).
  - Set up **dynamic resource allocation** to optimize GPU utilization across multiple experiments.
  - Implement **checkpointing and fault tolerance** using Ray Train for long-running tasks.
  
- **Training Experiment Execution**:
  - Start and configure **Ray Train** with multiple workers and fractional GPUs.
  - Submit concurrent training jobs for multiple style transfer models.
  - Monitor the Ray cluster using the **Ray dashboard**.

## 4. Hyperparameter Tuning

- **Ray Tune Setup**:
  - Use **Ray Tune** for hyperparameter optimization, focusing on refining parameters for style transfer and artist classification.
  <!--
  - Implement **Bayesian optimization** and **ASHA** for automated tuning of style transfer parameters (e.g., style weight, stroke consistency).
  -->
  
- **Logging and Tracking**:
  - Log all hyperparameter tuning experiments in **MLFlow** to track the best configurations.

## 5. Infrastructure Setup

- **GPU Cluster**:
  - Ensure a multi-GPU setup for DDP/FSDP experiments to scale training for high-resolution artistic images.
  
- **Persistent Storage**:
  - Set up storage for training datasets, model checkpoints, and transformed outputs.

- **Chameleon Cloud**:
  - Host **MLFlow tracking** and the **Ray cluster** on Chameleon for experiment management and training job distribution.

- **Ray Cluster**:
  - Ensure the **Ray cluster** supports multiple concurrent style transformation experiments, maximizing GPU resource efficiency.
