# Vision to Vintage: Continuous X (DevOps)

Welcome to the DevOps module of our project **Vision to Vintage: AI's Take on Classical Art**. This guide walks you through the infrastructure, automation, and deployment pipeline implemented for this system, following the lifecycle from provisioning to production. All files referenced are located in the [`Continuous_X/`](./Continuous_X/) directory of this repository.

---

## 📁 Project File Structure (within Continuous_X/)

```
Continuous_X/
├── ansible/                      # Ansible playbooks for configuring VMs and installing Kubernetes
├── kubespray/                   # Kubespray fork for Kubernetes cluster deployment
├── inventory/                   # Kubespray inventory and group_vars
├── terraform/                   # Terraform scripts to provision infrastructure on Chameleon
├── k8s/                         # K8s manifests and service configurations
└── README.md                    # This guide
```

---

## 🚀 Step 1: Provision Infrastructure (Terraform)

We use **Terraform** to provision 3 bare metal instances on Chameleon Cloud.

### Files:
- [`terraform/`](./Continuous_X/terraform/) — contains `main.tf`, `variables.tf`, and `outputs.tf`

### Instructions:

1. Authenticate with Chameleon OpenStack:
```bash
source openrc.sh  # Your Chameleon OpenStack credentials
```
2. Initialize and apply Terraform:
```bash
cd terraform
terraform init
terraform apply
```
3. Note down the floating IP and internal IPs from the output. These will be used in Ansible inventory.

> ⚠️ This setup avoids ClickOps by tracking all provisioning in version control.

---

## 🛠 Step 2: Configure the VMs with Ansible

We automate configuration with **Ansible**, skipping manual installs.

### Files:
- [`ansible/pre_k8s_configure.yml`](./Continuous_X/ansible/pre_k8s_configure.yml) — disables firewall, sets Docker daemon
- [`ansible/inventory.yml`](./Continuous_X/ansible/inventory.yml) — maps IPs and hosts

### Instructions:

1. Set your Ansible config (WSL/Linux terminal):
```bash
export ANSIBLE_CONFIG=./ansible/ansible.cfg
```

2. Verify SSH connectivity:
```bash
ansible -i ansible/inventory.yml all -m ping
```

3. Run the pre-K8s config:
```bash
ansible-playbook -i ansible/inventory.yml ansible/pre_k8s_configure.yml
```

---

## ☸️ Step 3: Install Kubernetes with Kubespray

We use a customized fork of **Kubespray** to install a production-ready Kubernetes cluster.

### Files:
- [`kubespray/`](./Continuous_X/kubespray/) — includes Kubespray roles and playbooks
- [`inventory/mycluster/hosts.yaml`](./Continuous_X/inventory/mycluster/hosts.yaml)
- [`group_vars/all.yml`](./Continuous_X/inventory/mycluster/group_vars/all.yml)

### Instructions:

1. Install dependencies:
```bash
cd kubespray
pip install --user -r requirements.txt
```

2. Edit `hosts.yaml` to reflect your actual VM IPs.

3. Run the installer:
```bash
ansible-playbook -i ../inventory/mycluster/hosts.yaml --become cluster.yml
```

4. On success, use `kubectl` to check cluster:
```bash
kubectl get nodes
```

---

## 🧠 Continuous Training + CI/CD (Outline)

### Tools Used:
- Argo Workflows for retraining pipelines
- MLflow for experiment tracking
- Docker + GitHub Actions for CI/CD (see [`k8s/`](./Continuous_X/k8s/))

> Each training run triggers evaluation, packaging, and deployment to staging.

---

## 🚦 Staged Deployment Architecture

Our cluster supports **3 environments**:
- `staging` — new models land here first
- `canary` — exposed to partial traffic for online eval
- `production` — after passing evaluation

### Promotion Flow:
1. New model → staging (auto)
2. Passed offline eval → canary (manual trigger)
3. Passed live eval → promote to prod (via Helm)

---

## 🔁 Immutable + Cloud-Native Principles

- All infra defined in code (`terraform/`, `ansible/`, `k8s/`)
- All services containerized in Docker
- Zero manual configuration after launch

---

## 📦 Running on Your Own Chameleon Account

### Prerequisites:
- Chameleon OpenStack account
- Chameleon CLI credentials (`openrc.sh`)
- SSH key uploaded to Chameleon

### Full Launch Sequence:
```bash
# Provision infra
cd terraform
terraform apply

# Configure VMs
cd ../ansible
ansible-playbook -i inventory.yml pre_k8s_configure.yml

# Deploy K8s
cd ../kubespray
ansible-playbook -i ../inventory/mycluster/hosts.yaml --become cluster.yml
```

Then deploy your services using `kubectl` or `helm`.

---

## 👤 Author: Unit 3 - DevOps
**Varijaksh Katti (Group 35)**

Responsibilities:
- Infrastructure-as-Code (Terraform + Ansible)
- K8s provisioning (Kubespray)
- CI/CD, automation, and staged deployment strategy
- Cloud-native compliance

---

## 📎 References
- [Lab 3 - Build MLOps pipeline (PDF)](../Lab%203%20-%20Build%20MLops%20pipeline.pdf)
- [Kubespray Docs](https://github.com/kubernetes-sigs/kubespray)
- [Chameleon Cloud Docs](https://www.chameleoncloud.org/docs/)

---

