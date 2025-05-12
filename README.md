<!-- 
more focus on target users
value:museum (business metric?)
outside dataset -- whats inside -- scale
Summary of infrastructure requirements
filter model training how to satisfy the requirement
-->

## Vision to Vintage: AI’s Take on Classical Art

### Discuss: Value proposition:

_Current Status Quo_
 
The **Metropolitan Museum of Art** relies on **traditional engagement methods** such as guided tours, plaques, and audio guides to educate visitors. While effective, these methods are **passive and lack personalization**, limiting engagement, particularly for younger and casual visitors.
 
_Proposed AI System_

We introduce an **interactive AI-powered exhibit** that allows visitors to:
1.  **Submit or choose a photo**, which is analyzed using object detection.
2.  **Apply artist-specific styles** based on the detected content.
3.  **Guess the artist** in a gamified challenge, reinforcing learning.
4.  **Receive AI-generated explanations** on stylistic features to deepen understanding.
 
_Business Value_
 
*   **Enhances Visitor Engagement** – Transforms passive observation into interactive exploration.
*   **Educational & Gamified Experience** – Visitors actively learn about artists through play. 
*   **Data-Driven Insights** – Visitor interactions inform exhibit improvements and preferences.
*   **Potential Monetization** – AI-generated artworks can be sold as prints or digital souvenirs.

_Target Users & Profitability Strategy_

Our primary target users are young adult visitors (ages 18–30), including college students, digital-native tourists, and casual museum-goers who seek interactive, tech-driven experiences. This demographic is highly engaged on social media and motivated by shareable, gamified content. By offering personalized AI-generated art transformations and a challenge-based interaction, we turn passive viewers into active participants. These users are also more likely to purchase stylized digital prints or NFT-style collectibles of their transformed photos—providing a clear monetization path. Additionally, the museum gains valuable user analytics on engagement trends, helping to optimize future exhibits. This system not only enhances educational value but also opens a revenue stream through digital merchandise, driving long-term profitability and deeper brand engagement for The Met.
 
_Effectiveness & Model Monitoring_
 
*   **Success Metric:** Visitors correctly identifying artists more often over time.
*   **User Feedback Loop:** If accuracy is low, retrain models to improve style transformations.
*   **Re-training Triggers:** Poor user engagement, incorrect classifications, or visitor feedback indicating confusion.
 
This system modernizes **art appreciation through AI**, making it interactive, educational, and engaging while driving business value for The Met.


### Contributors

| Name                            | Responsible for | Link to their commits in this repo |
|---------------------------------|-----------------|------------------------------------|
| All team members|Project idea, value proposition, ML problem setup (data, target variable), approach for each part, overall integration | N/A |
| Aryaman Dev     |Model serving and monitoring                 |                                    |
| Mona Mei        |Model training   |   [Link](https://github.com/M0n4GPT/MLOps-project-demo/tree/main/ModelTraining)    |
| Shruti Karmarkar| Data Pipelining             |   [Link](https://github.com/M0n4GPT/Vision-to-Vintage-AIs-Take-on-Classical-Art/tree/main/Data%20Pipelining)                                  |
| Varijaksh Katti | Continuous X              |   [Link](https://github.com/M0n4GPT/Vision-to-Vintage-AIs-Take-on-Classical-Art/tree/main/Continuous%20X)                               |



### System diagram


![image](https://github.com/user-attachments/assets/0f8e0253-56a6-4493-b1b6-14eb9ba3c6fd)

    

### Summary of outside materials


Here’s a structured table for summarizing the outside materials used in our project:

|              | How it was created | Conditions of use |
|--------------|--------------------|-------------------|
|**Best Artworks of All Time** |Large-scale dataset of artworks with metadata across 1,000+ artists.[Link](https://www.kaggle.com/datasets/ikarus777/best-artworks-of-all-time)|      Public Kaggle dataset – for non-commercial, research, and educational use. |
|**Random Image Sample Dataset** |This Dataset comprises of 3000 Random Pictures of 150 X 150 pixels. It contains mountains, cities, greenries, icelands, forest etc. [Link](https://www.kaggle.com/datasets/pankajkumar2002/random-image-sample-dataset)| Public Kaggle dataset – educational use; some artworks may be under copyright.|
|**Style-Transfer-GAN Repo**| GitHub implementation of GAN-based style transfer for artistic image generation.  [Link](https://github.com/temilaj/Style-Transfer-GAN) |MIT License – free for research and commercial use with attribution.|
|**VGG-19 Model**|Pre-trained convolutional neural network (CNN) used for style transfer. [Link](https://pytorch.org/vision/stable/models.html)|Open-source under **MIT License**, can be used for academic research.|
|**CLIP (Contrastive Language–Image Pretraining)**|Foundation model by OpenAI that connects images and text for classification. [Link](https://openai.com/research/clip)|Open-source for **non-commercial research**; commercial usage requires permission.|
|**Neural Style Transfer (NST)** |PyTorch-based repo for classic neural style transfer techniques. [Link](https://github.com/NikSchaefer/neural-style-transfer?tab=MIT-1-ov-file)| MIT License – open-source, can be freely used and modified.|
|**STGAN (Style Transfer GAN)** |Advanced GAN-based model for unpaired artistic style transfer. [Link](https://github.com/nipdep/STGAN)|Research-oriented GitHub repo – usage under open-source license with attribution.|

### Summary of infrastructure requirements

Here’s a table summarizing the anticipated **infrastructure requirements** for our project:

| Requirement     | How many/when                                     | Justification |
|-----------------|---------------------------------------------------|---------------|
| `m1.medium` VMs | 3 for entire project duration                     |For hosting the backend API and data pipeline services, including user interface handling and model serving. Moderate compute power needed for image processing and interaction.|
| `gpu_mi100` or `compute_liqid` with two GPUs  |6-hour block twice a week                      | For training the deep learning models (Style Transfer and Artist Classification) requiring GPU acceleration for high throughput and speed. For the “Ray” section.|
| Floating IPs    | 1 for the entire project duration, 1 for sporadic use |To support external access to the cloud-based API and services during development/testing and occasional live sessions (public demo).|
|Persistent Storage      | 500GB for the project duration (scalable)   | For storing large image datasets (e.g., museum artwork), user-uploaded images, processed results, and logs. Essential for persistent data handling across sessions. |
|Object Storage (e.g., S3)|1TB for training data and intermediate outputs|Cloud storage for dataset storage (CIFAR, WikiArt, Met dataset) and model checkpoints. Ensures efficient retrieval and scalability.|
|Compute-Intensive Server|2-3 instances of high-performance servers (GPU-enabled)|Needed for high-load processing during inference tasks for style transformation and real-time interaction.|
|Load Balancer|1 for the entire project duration|To balance the traffic between multiple backend servers during peak user activity (e.g., high foot traffic at the museum).|

This infrastructure setup supports the different phases of the project, including data processing, model training, deployment, and real-time user interactions.

### Detailed design plan

<!-- In each section, you should describe (1) your strategy, (2) the relevant parts of the 
diagram, (3) justification for your strategy, (4) relate back to lecture material, 
(5) include specific numbers. -->



#### Model training and training platforms

<!-- Make sure to clarify how you will satisfy the Unit 4 and Unit 5 requirements, 
and which optional "difficulty" points you are attempting. -->



##### Training Strategy (Unit 4)
Our model training pipeline is designed for scalability and efficiency. Given that our project focuses on art style transfer and artist classification, to satisfy the requirements, we will:

- **Train and re-train**: We will train both a style transfer model and an artist classification model from scratch, and re-train them periodically using new user-submitted artwork. This ensures adaptability to evolving data in production environments.
- **Modeling**: We use a CNN-based architecture (VGG-19) for style transfer and the CLIP (Contrastive Language–Image Pretraining) model for artist classification, justified through performance comparisons and experiment analysis.

To support large model training (extra “difficulty points”):
- We will use **Distributed Data Parallel (DDP)** for efficient multi-GPU training, reducing time to convergence.
- We will use **Fully Sharded Data Parallel (FSDP)** to enable training of larger models by sharding model parameters across devices.
- We will experiment with **batch sizes ranging from 8 to 64** to explore their impact on model convergence and GPU memory efficiency. And try to find an efficient training strategy to fit on a low-end GPU.

Experiments metrics will include:
- Comparing single-GPU vs. multi-GPU (DDP and FSDP) training performance.
- Measuring training time, accuracy, and convergence speed under different batch sizes and training strategies.
- Plotting training time vs. number of GPUs to illustrate scalability.

##### Model training infrastructure and platform (Unit 5)

**Experiment Tracking**: To log and analyze training experiments, we will host an **MLFlow tracking server** on Chameleon. Our system will:

- Log model parameters, optimizer settings, and architectural choices for both models.
- Track metrics such as **content loss**, **style loss**, and **classification accuracy** for experiment comparison.
- Record results from different training strategies (DDP vs. FSDP, batch sizes) to identify optimal configurations.
- Register and version models, enabling reproducible training and easy retraining based on production data.


<!--We will:
- **Start and configure the MLFlow tracking server**.
- **Access dashboards for real-time monitoring**.
- **Start a Jupyter server** for interactive experiment analysis.
- **Log training runs from both PyTorch and Lightning models**.
- **Compare experiments and use MLFlow outside of training runs**.
- **Stop the MLFlow system when needed**.

This allows us to retrain models effectively based on new artistic datasets and evolving user preferences.
-->

**Training Job Scheduling**: We will deploy a **Ray cluster** on Chameleon to schedule and execute training jobs. Key functionalities include:

- Submitting and managing **parallel training jobs** across multiple GPUs (e.g., NVIDIA V100 or A100).
- Dynamically scaling resources for efficient GPU utilization.
- Running long-duration training jobs with **fault tolerance and checkpointing** using **Ray Train**.

We will configure Ray Train with (extra “difficulty points”):
- **FailureConfig** for resilience against node failure.
- **Remote checkpointing** to persistent storage.
- Multiple workers and fractional GPU usage to parallelize style transfer fine-tuning.

<!--We will:
- **Start and configure the Ray cluster on NVIDIA GPUs**.
- **Start a Jupyter container** to manage job submissions.
- **Access the Ray cluster dashboard** for monitoring.
- **Submit training jobs with Ray Train and handle infeasible jobs**.
- **Implement Ray Train fault tolerance using FailureConfig**.
- **Stop the Ray system when needed**.
-->

We will schedule **Hyperparameter Tuning** jobs (extra “difficulty points”) using **Ray Tune**, which allows:

- **Automated tuning** with advanced algorithms (e.g., Bayesian optimization, ASHA) to refine **style transfer parameters**.
- **Efficient resource allocation** to test different hyperparameter sets concurrently, such as finding the optimal style weight for preserving both artistic details and content structure.
- **Logging in MLFlow** to track the best configurations for both style transfer and artist classification.

<!--
We will:
- **Use Ray Tune for hyperparameter optimization**.
- **Leverage new Ray Tune features for improved efficiency**.
- **Optimize parameters related to stroke consistency, color preservation, and feature extraction in style transfer models**.
-->

##### Infrastructure Requirements for This Part
- **GPU Cluster**: Multi-GPU setup for DDP/FSDP experiments, ensuring scalable training for high-resolution images.
- **Persistent Storage**: To store training datasets and model checkpoints, preserving both original artworks and transformed outputs.
- **Chameleon Cloud**: Hosting MLFlow and Ray cluster, providing an adaptable research environment.
- **Ray Cluster**: To distribute training and tuning jobs efficiently, supporting multiple concurrent style transformations.



#### Model serving and monitoring platforms

##### Core Serving Implementation
**FastAPI Endpoint for Style Transfer**:

```
@app.post("/transform")
async def style_transfer(image: UploadFile):
# Input validation (ML Test Score Data 1)
validate_image_size(image.file)
```

###### Sequential processing pipeline
content = yolo_model(image.file)   # Object detection
style = style_selector(content)    # Content-aware selection
output = cyclegan.transform(image.file, style)  # Style application
return StreamingResponse(output, media_type="image/jpeg")


**Performance Requirements**:
- P99 Latency: <200ms (online inference)
- Throughput: 45 req/sec (batch processing)
- Concurrency: 500 simultaneous users (Kubernetes HPA)

**Optimizations**:
| Type | Technique | Expected Impact |
|------|-----------|--------|
| Model | FP16 Quantization | ~35% size reduction |
| System | Redis Caching | ~85% cache hit rate |
| System | Kubernetes HPA | ~2-10 pod scaling |

##### Monitoring & Evaluation
**MLFlow Tracking**:
```
with mlflow.start_run():
mlflow.log_metric("style_transfer_latency", latency)
mlflow.log_artifact("eval_results.json")
```


**Evaluation Pipeline**:
1. **Offline Testing**:

```
test_suite = [
("negation_handling", test_negation_scenarios),
("cultural_bias", check_style_fairness)
]
```

2. **Load Testing**:

```
locust -f load_test.py --headless -u 500 -r 50 --host http://staging-api
```

3. **Canary Deployment**:

```
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
spec:
http:
- route:
- destination: style-transfer-v1
weight: 95
- destination: style-transfer-v2
weight: 5
```

**Business Metrics**:
| Metric | Target | Current |
|--------|--------|---------|
| Artist Recognition | ~75% | 68% |
| Engagement Time | ~240s | 210s |

<!--
Satisfies Unit 6:
- FastAPI endpoint serving
- Model optimizations (quantization)
- System optimizations (Redis, HPA)

Satisfies Unit 7:
- MLFlow experiment tracking
- Load testing with Locust
- Istio canary deployments
-->

#### Data pipeline
This section provides a detailed walkthrough of the data pipelining component developed for the AI Art Experience project, in alignment with the Unit 8 requirements. It outlines how we provisioned persistent storage, built offline and online data pipelines, and ensured production-readiness on Chameleon Cloud. Each part of the pipeline—from data extraction and preprocessing to storage organization and simulation of real-time data—is linked to specific scripts and artifacts in this repository to ensure transparency and reproducibility.

**Persistent Storage**
To ensure durability and availability of critical application components, we provisioned persistent storage using two approaches:
1] Block Storage (Deployed on KVM@TACC)

Mount Point: /mnt/project35
* Purpose: Serves as a reliable storage layer for essential application services such as:
* MLflow experiment tracking data
* PostgreSQL metadata
* Model checkpoint files and logs
* This storage is mounted as a persistent volume on the Chameleon KVM instance, ensuring that all data is retained across VM shutdowns or reboots.

The following files define and document the block storage configuration:
docker-compose-block.yaml: Docker Compose configuration that sets up MLflow, MinIO, Jupyter, and PostgreSQL with persistent volumes.
block.md: Supplementary notes explaining the volume setup, mounting process, and troubleshooting steps.

* [docker-compose-block.yaml] (https://github.com/M0n4GPT/Vision-to-Vintage-AIs-Take-on-Classical-Art/blob/main/Data%20Pipelining/docker/docker-compose-block.yaml)
* [block.md] (https://github.com/M0n4GPT/Vision-to-Vintage-AIs-Take-on-Classical-Art/blob/main/Data%20Pipelining/snippets/block.md)

**Object Storage (Deployed via MinIO on Baremetal):**
We utilized Chameleon’s object storage, mounted via rclone, to host all large-scale datasets used for training and evaluating our neural style transfer model.

🔹 Mount Details
* Mounted Path: /mnt/project35
* Remote Alias: chi_tacc:object-persist-project35
* Mount Method: rclone FUSE mount from Chameleon’s object store to the local filesystem of the training node, allowing seamless access during both preprocessing and model training stages.

🔹 Purpose
* The object storage serves as the central data repository for all image assets required by the project.
*It is used to store:
1] Style datasets (paintings by 50 artists)
* Each contains subfolders for individual artist names (e.g., train/monet/, val/van_gogh/). [Link to the object store](https://chi.tacc.chameleoncloud.org/project/containers/container/object-persist-project35)

2] Random input images (used for training and simulating inference)
* We have used another dataset with random images which is stored inside the random_inputs folder. Inside this folder the images inside random_train and random_val are used for training purposes and random_test is used for simulating production data.
* [Link to all the yaml file for creating persistant storage](https://github.com/M0n4GPT/Vision-to-Vintage-AIs-Take-on-Classical-Art/tree/main/Data%20Pipelining/docker)
* [Link to the snippets folder with .md files](https://github.com/M0n4GPT/Vision-to-Vintage-AIs-Take-on-Classical-Art/tree/main/Data%20Pipelining/snippets)
* [Link to object storage setup](https://github.com/M0n4GPT/Vision-to-Vintage-AIs-Take-on-Classical-Art/tree/main/Data%20Pipelining/object_storage_setup)

**Offline Data Pipeline**
Dataset
* Source: [Best Artwork of all time] (https://www.kaggle.com/datasets/ikarus777/best-artworks-of-all-time) This dataset contains 50 folders with the painting of different artists
* Source: [Random Image Sample] (https://www.kaggle.com/datasets/pankajkumar2002/random-image-sample-dataset) This dataset has 3000 random images
* Format: ZIP 
* Lineage: Downloaded and extracted in the pipeline using kaggle CLI.

Production Data Saving Setup: To enable feedback-loop data collection, we implemented the following steps:
1] Created a production bucket in MinIO
* We added a sidecar container (minio-init) in docker-compose-production.yaml to programmatically create the bucket on startup using the MinIO CLI.
* [Link to Production Data yaml file](https://github.com/M0n4GPT/Vision-to-Vintage-AIs-Take-on-Classical-Art/blob/main/Data%20Pipelining/docker/docker-compose-production.yaml)
* [More details in Production Data.md file](https://github.com/M0n4GPT/Vision-to-Vintage-AIs-Take-on-Classical-Art/blob/main/Data%20Pipelining/snippets/Offline%20Data.md)

2] Updated app.py in Vision-to-Vintage App
* Added environment variables to access MinIO (MINIO_URL, MINIO_USER, MINIO_PASSWORD).
* Integrated boto3 to connect to the object store.
* After stylization, we uploaded each image to the production bucket with tags for predicted style and timestamp.
* [Link to the app.py](https://github.com/M0n4GPT/Vision-to-Vintage-AIs-Take-on-Classical-Art/blob/mona-feature-update/ModelTraining/vision-to-vintage-app/app.py)


**Pipeline Script:** [docker files link with etl pipeline](https://github.com/M0n4GPT/Vision-to-Vintage-AIs-Take-on-Classical-Art/tree/main/Data%20Pipelining/docker)

This Docker Compose configuration defines a containerized ETL pipeline designed to automate the preprocessing and organization of the artwork dataset prior to training. The pipeline ensures reproducibility and simplifies deployment on Chameleon Cloud.

🔹 Key Functions Performed by the Pipeline:
1] Extraction:
* Automatically unzips the raw dataset downloaded from Kaggle.
* Handles nested folder structures to ensure all artist folders are isolated.
* Stratified Splitting:
  For each artist folder, images are randomly divided into:
  train/artist_name/ (70%)
  val/artist_name/ (15%)
  test/artist_name/ (15%)
* Splitting ensures consistent distribution of data across splits without leaking validation/test data into training.

2] Directory Reorganization:
* Reconstructs the entire dataset into a consistent hierarchical format based on artist names, compatible with PyTorch-style ImageFolder loaders.

3] Data Upload:
* The processed dataset is uploaded to Chameleon’s object storage using rclone, which syncs the local /processed_dataset/ folder with the mounted path /mnt/project35/.

* Preprocessing Steps Embedded in the Pipeline:
a) Resizing:
All images are resized to a standard resolution of 256x256 pixels for compatibility with the input shape expected by the model.

b) Normalization:
Pixel values are normalized using standard image preprocessing techniques (e.g., dividing by 255 and applying mean-std normalization if needed during model loading).

c) Artist-Wise Splitting:
Ensures no data leakage by treating each artist’s dataset independently. This guarantees that styles seen during training do not bleed into evaluation sets.

 **Online Data Pipeline**
To mimic real-time usage of the application, we implemented a script that continuously sends image data to the deployed inference endpoint, replicating a production environment.

Simulated Production Data Script
 * [Script](https://github.com/M0n4GPT/Vision-to-Vintage-AIs-Take-on-Classical-Art/tree/main/Data%20Pipelining/Simulate%20Online%20Data)
   
Functionality:
* The script loops through the images stored in the random_test folder (located in the random_inputs/ directory on object storage).
* At configurable intervals (e.g., every 5 seconds), it sends a new image via an HTTP POST request to the model’s REST API.
* This simulates user-generated image uploads during real-world usage and triggers inference in a time-distributed manner.

Format:
* Written in Python, the script uses the requests library to POST image files.
* API expects base64-encoded image payloads formatted in JSON.
* This design helps stress-test the serving pipeline and verify response behavior under ongoing usage.

**Data Dashboard**
The dashboard provides a visual overview of the datasets stored in object storage, offering insights into data quality, class distribution, and structure validation.
* Technology Used: Built with Plotly Dash, this interactive dashboard is hosted on a Chameleon VM and visualizes dataset metadata.
* Dashboard Location: [Dashboard Folder](https://github.com/M0n4GPT/Vision-to-Vintage-AIs-Take-on-Classical-Art/tree/main/Data%20Pipelining/Data%20Dashboard)
* Runs on:  Access the dashboard by navigating to [link](http://129.114.25.100:8050) in your web browser.
* Key Features:
     Displays the distribution of images across train, val, and test folders for each artist
     Verifies image resolution uniformity
     Tracks total number of samples in random input sets vs. style datasets
     
* Benefit:
     Enables researchers and admins to audit data quality before and during training
     Quickly identify class imbalance, data corruption, or misplacement across splits

