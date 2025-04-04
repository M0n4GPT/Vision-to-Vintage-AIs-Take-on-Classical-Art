# Continuous X Proposal  
*(Unit 3: Continuous Integration, Continuous Delivery, and Continuous Training)*

---

## Overview

This section outlines our approach to **Continuous Integration (CI)**, **Continuous Delivery (CD)**, and **Continuous Training (CT)** for the *Vision to Vintage* project.  
We implement fully automated pipelines to ensure fast iteration, safe deployments, and continuous model improvements based on real-world data, following industry-standard MLOps practices.

Our Continuous X system covers:
- Infrastructure-as-Code (IaC)
- Cloud-native service deployment
- CI/CD pipelines for service promotion
- Automated model retraining based on monitoring feedback

All infrastructure and workflows are hosted on **Chameleon Cloud** and managed via **GitHub Actions**, **Terraform**, and **Kubernetes**.

---

## Infrastructure-as-Code (IaC)

- All infrastructure configurations are managed declaratively and stored in GitHub.
- **Terraform** is used for resource provisioning on Chameleon Cloud.
- **Kubernetes** manifests define service deployments (model serving API, ETL pipeline, monitoring services).
- **Immutable Infrastructure**: No manual changes to deployed instances; updates occur through Git and automated pipelines.
- **Containerization**: All services (FastAPI API, data pipelines, dashboards) are Dockerized for portable and versioned deployment.

---

## Cloud-Native Architecture

- **Microservices**: Each service (inference, ETL, dashboard) is deployed independently using Kubernetes.
- **Containerized Services**: All workloads run in Docker containers orchestrated by Kubernetes.
- **Auto-scaling**: Kubernetes Horizontal Pod Autoscaler (HPA) dynamically adjusts serving resources.
- **Immutable Deployments**: New versions are deployed through GitOps workflows with no manual intervention.

---

## Continuous Integration (CI)

The **GitHub Actions CI pipeline** is triggered on every code push or pull request:

1. **Code Testing**:
   - Run automated unit tests using Pytest to validate new code.
2. **Build Phase**:
   - Build Docker images for model serving, data pipeline, and monitoring dashboards.
3. **Container Registry Push**:
   - Push built images to a container registry for versioning and deployment.
4. **Deployment to Staging**:
   - Deploy services to the **staging** environment using Kubernetes manifests.

This ensures early bug detection, fast feedback, and consistent deployment artifacts.

---

## Continuous Delivery (CD)

Our deployment follows a **staged promotion strategy**:

1. **Staging Deployment**:
   - Deploy updated services to a staging namespace for testing.
   - Perform automated offline model evaluation and load testing (Locust).

2. **Canary Deployment**:
   - Use **Istio VirtualService** to route 5% of real traffic to the new service version while 95% goes to the stable version.
   - Monitor live performance metrics such as P99 latency, throughput, and error rates.

3. **Production Promotion**:
   - If canary tests pass, promote the new version to full production rollout.

**Rollback Mechanism**:
- Monitor with **Prometheus**.
- If P99 latency exceeds 250ms or critical failures are detected, trigger an **automatic rollback** to the previous version.

---

## Continuous Training (CT)

We implement **automated model retraining** based on real-world monitoring feedback:

1. **Data Collection**:
   - Save 10% of production images and user feedback in persistent object storage.

2. **Model Retraining**:
   - Trigger retraining jobs on a Ray cluster if:
     - Model accuracy falls below 60%.
     - Data drift or model degradation is detected by Evidently AI.
   - Train using distributed methods like DDP and FSDP to handle large models efficiently.

3. **Evaluation and Registration**:
   - Run offline evaluation tests after retraining.
   - If models meet quality thresholds, register them in **MLFlow** and deploy to staging.

4. **Version Control**:
   - Version all models, artifacts, and training metadata in **MLFlow** for reproducibility.

---

## Monitoring Stack

Our monitoring infrastructure includes:

| **Tool** | **Purpose** |
|:---------|:------------|
| **Prometheus** | Collects system metrics (latency, resource utilization). |
| **Grafana** | Visualizes system health, business KPIs, and real-time dashboards. |
| **MLFlow** | Tracks experiments, model metrics, and artifacts. |
| **Evidently AI** | Monitors data drift and model degradation. |

These tools provide full observability over system health, model behavior, and data quality.

---

## Summary

By implementing Continuous Integration, Delivery, and Training, we ensure that the *Vision to Vintage* system is:

- **Reliable**: Bugs and failures are caught early through CI pipelines.
- **Scalable**: Auto-scaling microservices manage variable user load.
- **Adaptable**: Continuous retraining keeps models fresh and aligned with real-world data.
- **Resilient**: Canary deployments, monitoring, and rollback mechanisms maintain system stability.
