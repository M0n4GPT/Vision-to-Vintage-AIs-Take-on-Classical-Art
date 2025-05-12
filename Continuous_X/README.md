# Vision to Vintage: Continuous X (DevOps)

Welcome to the DevOps module of our project **Vision to Vintage: AI's Take on Classical Art**. This guide is designed as a hands-on workbook for reproducing our end-to-end infrastructure, CI/CD, and deployment system using cloud-native tools and GitOps workflows. You can walk through the instructions line-by-line to deploy everything from scratch on Chameleon Cloud.

---

## Project File Structure (within `Continuous_X/`)

```
Continuous_X/
├── ansible/              # Ansible playbooks and inventory for configuring VMs
├── k8s/                  # Kubernetes manifests for model serving and workflows
├── tf/                   # Terraform configs to provision infrastructure
├── workflows/            # Argo Workflows for retraining and CI/CD pipelines
├── LICENSE               # Project license
└── README.md             # This DevOps workbook
```

---

## Requirements

Before running any steps in this guide, make sure your local development environment (or Chameleon Jupyter terminal, if applicable) includes the following tools installed:

- **Terraform** (>= v1.0): for provisioning infrastructure  
  Installation: https://developer.hashicorp.com/terraform/downloads

- **Ansible** (>= 2.9): for remote system configuration  
  Installation:  
  ```bash
  pip install --user ansible
  ```

- **Python 3.8+** with `pip`: for Ansible and Kubespray dependencies  
  Recommended to create a virtual environment:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

- **kubectl**: for interacting with the Kubernetes cluster  
  Installation: https://kubernetes.io/docs/tasks/tools/

- **OpenStack CLI tools**: for authenticating with Chameleon  
  Requires sourcing the `openrc.sh` file available from your Chameleon Dashboard

Optional (but recommended):
- **Argo CLI**: for interacting with Argo Workflows  
  Installation: https://argo-workflows.readthedocs.io/en/stable/cli_installation/

Ensure your SSH key is uploaded to Chameleon and available locally.

---

## 1. Provision Infrastructure using Terraform

Three bare metal instances are provisioned on Chameleon Cloud using Terraform. This approach ensures the infrastructure is reproducible and maintained under version control.

### Files in `tf/`:
- `main.tf`, `provider.tf`, and `versions.tf` define the infrastructure and provider.
- `variables.tf` and `terraform.tfvars` handle input values.
- `outputs.tf` provides instance IPs post-deployment.

Users should update variable files with their project-specific OpenStack settings and credentials.

---

## 2. Configure VMs with Ansible

Ansible is used to automate system-level configurations across provisioned VMs. This includes disabling firewalls, setting up Docker, and preparing for Kubernetes installation.

### Files in `ansible/`:
- `inventory.yml` lists the IP addresses of your nodes.
- `pre_k8s_configure.yml` configures Docker and disables firewall.
- `post_k8s_configure.yml` initializes kubeconfig, adds ArgoCD, dashboard, and post-K8s tools.
- `ansible.cfg` customizes SSH connection settings.

Edit `inventory.yml` to match the actual IPs of your nodes.

---

## 3. Install Kubernetes with Kubespray (via Clone)

We use Kubespray to deploy Kubernetes in a reproducible and secure way.

To set it up:
- Clone the Kubespray repo into `ansible/k8s/`
- Install Python requirements from `requirements.txt`
- Copy the sample inventory and populate it with your node IPs and roles

This approach avoids tracking large generated files in our own repository and allows always using the latest stable version of Kubespray.

---

## 4. Continuous Training and CI/CD Pipeline

The CI/CD pipeline is designed to retrain models, evaluate them, and deploy containers automatically to Kubernetes.

### Files in `workflows/`:
- `train_model.yaml`, `evaluate_model.yaml`, and `deploy.yaml` define retraining, evaluation, and deployment workflows respectively.

These YAMLs are used with Argo Workflows. Users may need to update paths to datasets or image repositories according to their setup.

---

## 5. Staged Deployment (Staging → Canary → Production)

The system is deployed using staged environments:
- **Staging** is the first target for CI/CD.
- **Canary** is for traffic-splitting and live monitoring.
- **Production** serves stable, validated versions.

This separation allows for safe promotion and rollback mechanisms using Helm and ArgoCD.

---

## 6. Cloud-Native and GitOps Principles

- Infrastructure is provisioned and configured using code
- Deployments are immutable and driven by Git
- All components are containerized
- The architecture favors modular microservices
- Promotion is governed by automation pipelines

---

## Author – Unit 3: DevOps
**Varijaksh Katti (Group 35)**

### Responsibilities:
- Provisioning via Terraform  
- System configuration via Ansible  
- Kubernetes setup via Kubespray  
- CI/CD orchestration using Argo Workflows *(in progress)*  
- Enabling GitOps and staged deployment *(to be finalized)*

---

## References
- Lab 3: MLOps Pipeline (PDF)  
- Kubespray GitHub: https://github.com/kubernetes-sigs/kubespray  
- Argo Workflows Docs: https://argo-workflows.readthedocs.io  
- Chameleon Cloud Docs: https://www.chameleoncloud.org/docs/
