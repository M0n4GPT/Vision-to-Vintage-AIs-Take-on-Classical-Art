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
| Shruti Karmarkar|                 |                                    |
| Varijaksh Katti |                 |                                    |



### System diagram

<!-- Overall digram of system. Doesn't need polish, does need to show all the pieces. 
Must include: all the hardware, all the containers/software platforms, all the models, 
all the data. -->
_1\. User Interaction (Frontend)_
* **Web Interface**
    *   Users upload or select a photo 
    *   Display of stylized images 
    *   Interactive quiz (Guess the Artist) 
    *   Feedback collection via touchscreen kiosks
 
_2\. Backend Processing & AI Models_
* **Data Pipeline (Preprocessing & Storage)**
    *   **Kafka Stream** (500 msg/sec throughput)
    *   **Spark Structured Streaming** (exactly-once processing)
    *   **Delta Lake** (30-day versioning)
    *   **Expectations** (~95% schema compliance)
* **Machine Learning Models**
    *   **Object Detection Model** (YOLOv8)
    *   **Style Transfer Model** (CycleGAN with FP16 quantization) Applies the artist’s style based on detected subject
    *   **Artist Classification Model** (CLIP+VGG19 ensemble) Predicts which artist matches the style
    *   **FP16 Quantization** (~35% model size reduction expected)
    *   **SHAP Explainer** (Highlights key style features to justify classification)
* **Containers & Deployment**
    *   Hosted on **Cloud (Chameleon)**
    *   Backend API (FastAPI)
    *   Models served using **TensorFlow Serving / TorchServe**
    *   Database for storing user interactions & feedback
 
_3\. Model serving & Monitoring_
* **FastAPI Endpoint**
    *   Input validation (ML Test Score Data 1)
    *   Sequential processing pipeline
    *   P99 Latency: <200ms (online inference)
* **Performance Optimization**
    *   Redis Caching for common style transformations (~85% expected hit rate)
    *   Kubernetes HPA (2-10 pod scaling)
    *   FP16 Quantization (35% model size reduction) 
* **Monitoring & Evaluation**
    *   MLFlow for experiment tracking
    *   Prometheus for metrics collection
    *   Grafana for visualization dashboards
    *   Locust for load testing (500 concurrent users)
    *   Istio Canary Deployments

_4\. Continuous X Pipeline_ 
*  **CI/CD**
    *   GitHub Actions for automated workflows
    *   Unit Tests
*  **Infrastructure Management**
    *   Terraform for infrastructure-as-code
    *   Kubernetes Deployment for container orchestration
*  **Automated Retraining**
    *   Accuracy-based triggers 
 
_5\. Hardware Components & Infrastructure_ 
* **On-Site Hardware (Museum Kiosk Setup)**
    *   Touchscreen kiosks for museum visitors
    *   High-performance GPU server for real-time inference (if processing is done on-premise with permission)
    *   Edge computing capabilities for faster inference at museum locations
*  **Chameleon Cloud**
    *   1TB S3 Storage
    *   Kubernetes Cluster
    *   50GB Redis Cluster
    

### Summary of outside materials

<!-- In a table, a row for each dataset, foundation model. 
Name of data/model, conditions under which it was created (ideally with links/references), 
conditions under which it may be used. -->
Here’s a structured table for summarizing the outside materials used in our project:

|              | How it was created | Conditions of use |
|--------------|--------------------|-------------------|
|**CIFAR-10 / CIFAR-100** |Created by the **Canadian Institute for Advanced Research**, containing labeled images for object detection and classification. [Link](https://www.cs.toronto.edu/~kriz/cifar.html)|      Open-source under the **MIT License**; freely usable for research and educational purposes. |
|**Metropolitan Museum Open Access Collection** |High-resolution public domain images of artworks from The Met’s collection. [Link](https://www.metmuseum.org/about-the-met/policies-and-documents/open-access)| **Creative Commons Zero (CC0)**—can be freely used, modified, and distributed.|
|**WikiArt Dataset**| Large dataset of artwork images with metadata, scraped from WikiArt. [GitHub](https://github.com/cs-chan/ArtGAN),  [kaggle](https://www.kaggle.com/datasets/antoinegruson/-wikiart-all-images-120k-link/data)| Publicly available, but usage requires compliance with **WikiArt's terms**. |
| **Best Artworks of All Time Dataset**   |Collection of paintings of the 50 most influential artists of all time. [Link](https://www.kaggle.com/datasets/ikarus777/best-artworks-of-all-time)|Licensed under CC BY-NC-SA 4.0, allowing non-commercial use with attribution. |
| **COCO Dataset**   |Large-scale object detection dataset for training image recognition models. [Link](https://cocodataset.org/)|Freely available for **non-commercial research and educational use**. |
|**VGG-19 Model**|Pre-trained convolutional neural network (CNN) used for style transfer. [Link](https://pytorch.org/vision/stable/models.html)|Open-source under **MIT License**, can be used for academic research.|
|**CLIP (Contrastive Language–Image Pretraining)**|Foundation model by OpenAI that connects images and text for classification. [Link](https://openai.com/research/clip)|Open-source for **non-commercial research**; commercial usage requires permission.|
|**Neural Style Transfer**|Open-source implementation of Neural Style Transfer using a GAN using the technique outlined in [A Neural Algorithm of Artistic Style](https://arxiv.org/abs/1508.06576). [Link](https://github.com/NikSchaefer/neural-style-transfer)|Open-source under **MIT License**, can be used for academic research.|
|**STGAN**|Open-source implementation of Neural artistic traslator using novel cGAN architechure. [Link](https://github.com/nipdep/STGAN)|Open-source under **MIT License**, can be used for academic research.|


### Summary of infrastructure requirements

<!-- Itemize all your anticipated requirements: What (`m1.medium` VM, `gpu_mi100`), 
how much/when, justification. Include compute, floating IPs, persistent storage. 
The table below shows an example, it is not a recommendation. -->

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



##### Training Strategy
Our model training pipeline is designed for scalability and efficiency. Given that our project focuses on art style transfer and artist classification, we will use:

- **Distributed Data Parallel (DDP)** for efficient multi-GPU training, ensuring faster convergence for high-resolution style transfer models.
- **Fully Sharded Data Parallel (FSDP)** to enable large model training by sharding model parameters across GPUs, crucial for handling complex artistic transformations.
- **Optimized batch sizing** to balance memory constraints and computational efficiency, considering the high pixel resolution of artistic datasets.

We will conduct experiments comparing training time and performance using:
- Single-GPU vs. Multi-GPU training (with DDP and FSDP) to evaluate the impact on style transfer efficiency.
- Effect of batch size variations on convergence speed and model accuracy, specifically for artist classification tasks. We will experiment with batch sizes ranging **from 8 to 64**, measuring the impact on training time and model performance (accuracy and convergence speed).

##### Experiment Tracking
To log and analyze training experiments, we will host an **MLFlow tracking server** on Chameleon. Our logging will include:

- Model parameters (architecture, hyperparameters, and optimizer) relevant for optimizing artistic style transformations and classification.
- Training metrics such as **content loss, style loss, and classification accuracy** to assess both the effectiveness of style transfer and model precision in identifying artists.
- Comparative results from different training strategies and style transfer configurations.
- Registered models for version control and reusability, allowing for continuous improvement based on user feedback from our interactive platform.

<!--We will:
- **Start and configure the MLFlow tracking server**.
- **Access dashboards for real-time monitoring**.
- **Start a Jupyter server** for interactive experiment analysis.
- **Log training runs from both PyTorch and Lightning models**.
- **Compare experiments and use MLFlow outside of training runs**.
- **Stop the MLFlow system when needed**.

This allows us to retrain models effectively based on new artistic datasets and evolving user preferences.
-->

##### Training Job Scheduling
We will deploy a **Ray cluster** to schedule and distribute training jobs across multiple GPUs. The Ray cluster will be configured with at least **2 GPUs** (NVIDIA V100 or A100), ensuring enough parallel computation for large-scale model training.

- **Parallelized execution of multiple training experiments**, such as training different style transfer models concurrently.
- **Dynamic resource allocation** to optimize GPU utilization, ensuring efficient processing of various artistic styles.
- **Checkpointing and fault tolerance** using Ray Train, critical for long-running style adaptation tasks.
- **Ray Train with multiple workers and fractional GPUs**, allowing multiple style transformations to be fine-tuned simultaneously.

<!--We will:
- **Start and configure the Ray cluster on NVIDIA GPUs**.
- **Start a Jupyter container** to manage job submissions.
- **Access the Ray cluster dashboard** for monitoring.
- **Submit training jobs with Ray Train and handle infeasible jobs**.
- **Implement Ray Train fault tolerance using FailureConfig**.
- **Stop the Ray system when needed**.
-->

##### Hyperparameter Tuning
For hyperparameter optimization, we will use **Ray Tune**, which allows:

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

##### Architecture & Implementation
```
Delta Lake Pipeline (Lab 5)
(spark.readStream
.format("kafka")
.option("kafka.bootstrap.servers", "kafka:9092")
.load()
.writeStream
.format("delta")
.trigger(processingTime="1m")
.toTable("visitor_interactions"))
```

**Key Components**:
1. **Persistent Storage**: 1TB S3 bucket (Chameleon Lab 8)
2. **Data Validation**: Great Expectations 98% schema compliance
3. **Versioning**: Delta Lake 30-day history

**Data Flow**:
1. **Batch Ingestion**: 400GB/day from Met/WikiArt
2. **Stream Processing**: 500 msg/sec via Kafka
3. **Feature Store**: Feast for style embeddings

<!--
Satisfies Unit 8:
- ACID-compliant Delta Lake
- GDPR-compliant data handling
- Structured/unstructured data management
-->

#### Continuous X (Unit 3)

##### CI/CD Pipeline
```
name: ML Pipeline
on: [push]
jobs:
build:
runs-on: ubuntu-latest
steps:
- name: Unit Tests
run: pytest tests/unit/

deploy:
needs: build
runs-on: ubuntu-latest
steps:
- name: Deploy to Staging
run: kubectl apply -f k8s/staging/
```

**Core Features**:
- **Terraform Infrastructure**:
```
resource "kubernetes_deployment" "style_transfer" {
metadata { name = "style-transfer" }
spec { replicas = 3 }
}
```

- **Prometheus Alerts**: P99 latency >250ms triggers rollback
- **Daily Builds**: 12min average pipeline runtime

**Automated Retraining**:
```
if accuracy < 0.6:
trigger_retraining(feedback_data)
```

<!--
Satisfies Unit 3:
- GitHub Actions CI/CD
- Immutable infrastructure
- Staged deployments
-->
