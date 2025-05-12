# Vision to Vintage: Continuous X (DevOps)

Welcome to the DevOps module of our project **Vision to Vintage: AI's Take on Classical Art**. This guide is designed as a hands-on workbook for reproducing our end-to-end infrastructure, CI/CD, and deployment system using cloud-native tools and GitOps workflows. You can walk through the instructions line-by-line to deploy everything from scratch on Chameleon Cloud.

---

##  Final File Structure (within `Continuous_X/`)

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

##  1. Provision Infrastructure using Terraform

We provision three bare metal instances on [Chameleon Cloud](https://www.chameleoncloud.org/) using [Terraform](https://www.terraform.io/). This ensures the infrastructure is version-controlled and reproducible.

###  Files: [`tf/`](./tf)
- `main.tf`: defines OpenStack compute instances and networking
- `variables.tf`: contains variable declarations
- `outputs.tf`: exposes floating IPs
- `terraform.tfvars`: sets variable values for the deployment
- `provider.tf`: connects to the OpenStack provider
- `versions.tf`: sets Terraform version constraints

###  Instructions:
```bash
# Authenticate with OpenStack
source openrc.sh

# Move into the Terraform directory
cd tf

# Initialize and apply
terraform init
terraform apply
```

After execution, you'll get the instance IPs which are required for Ansible inventory.

---

##  2. Configure VMs with Ansible

Once the VMs are provisioned, we configure them using [Ansible](https://www.ansible.com/) playbooks.

###  Files: [`ansible/`](./ansible)
- `inventory.yml`: maps node hostnames and IPs
- `ansible.cfg`: configures SSH proxy jump and inventory path
- `general/hello_host.yaml`: sample hello-world playbook for connection test
- `pre_k8s_configure.yml`: disables firewalld and sets Docker daemon config
- `post_k8s_configure.yml`: sets up kubeconfig, dashboard, ArgoCD, Argo Workflows

###  Instructions:
```bash
# Set config and verify connection
export ANSIBLE_CONFIG=./ansible/ansible.cfg
ansible -i ansible/inventory.yml all -m ping

# Pre-K8s system setup
ansible-playbook -i ansible/inventory.yml ansible/pre_k8s_configure.yml
```

---

##  3. Install Kubernetes with Kubespray (via Clone)

We use [Kubespray](https://github.com/kubernetes-sigs/kubespray) to install a production-grade Kubernetes cluster.

###  Instructions:
```bash
# Clone Kubespray into the expected folder
cd ansible/k8s
git clone https://github.com/kubernetes-sigs/kubespray.git
cd kubespray
pip install --user -r requirements.txt

# Copy your inventory (edit IPs as needed)
cp -rfp inventory/sample inventory/mycluster
vim inventory/mycluster/hosts.yaml  # Set your node IPs

# Run the cluster installer
ansible-playbook -i inventory/mycluster/hosts.yaml --become cluster.yml
```

You now have a working Kubernetes cluster.

---

##  4. Continuous Training + CI/CD Pipeline

We use a combination of Argo Workflows, MLflow, and GitHub Actions to orchestrate retraining, evaluation, containerization, and staged deployment.

###  Files: [`workflows/`](./workflows)
- `train_model.yaml`: defines retraining steps
- `evaluate_model.yaml`: calculates metrics and logs to MLflow
- `deploy.yaml`: builds Docker image and updates staging

###  CI/CD Trigger:
- Git push to the `staging` branch
- Scheduled retraining
- External trigger (e.g. new labeled data)

###  Sample Flow:
```bash
# Submit Argo Workflow from CLI
argo submit workflows/train_model.yaml --namespace argo --watch
```

---

##  5. Staged Deployment (Staging → Canary → Production)

We implement three deployment stages in our K8s cluster:

- **Staging**: auto-deploy on push or retrain
- **Canary**: partial rollout for online evaluation
- **Production**: full promotion after evaluation success

Promotion is handled via Helm or custom ArgoCD workflows.

>  No service is manually promoted or edited in-place — everything flows through Git.

---

##  6. Cloud-Native & GitOps Principles

✔ **Infrastructure-as-Code**: Terraform + Ansible defined in `tf/` and `ansible/`  
✔ **Immutable Deployments**: Changes only made through Git commits  
✔ **Containers Everywhere**: All services containerized and deployed via K8s  
✔ **Microservices**: ML, UI, inference, and dashboards are independent pods  
✔ **CI/CD Pipelines**: Retraining → Evaluation → Docker Build → Deployment  
✔ **Staged Environments**: Dev, canary, prod modeled using Helm & ArgoCD  

---

##  7. Running the Project on Chameleon Cloud

###  Prerequisites:
- Chameleon OpenStack account
- `openrc.sh` credentials
- SSH key added to OpenStack dashboard

###  Full Launch Commands:
```bash
# Provision infrastructure
cd tf
terraform apply

# Pre-K8s setup
cd ../ansible
ansible-playbook -i inventory.yml pre_k8s_configure.yml

# Install Kubernetes via Kubespray
cd k8s
git clone https://github.com/kubernetes-sigs/kubespray.git
cd kubespray
ansible-playbook -i inventory/mycluster/hosts.yaml --become cluster.yml

# Post-K8s setup (dashboard, ArgoCD)
cd ../../../ansible
ansible-playbook -i inventory.yml post_k8s_configure.yml
```

You're now ready to deploy and monitor model workflows.

---

##  Author – Unit 3: DevOps
**Varijaksh Katti(Group 35)**

###  Responsibilities:
- Provisioning via Terraform  
- System configuration via Ansible  
- Kubernetes setup via Kubespray  
- CI/CD orchestration using Argo Workflows  *(in progress)*
- Enabling GitOps and staged deployment  *(to be finalized)*

---

##  References
- [Lab 3: MLOps Pipeline (PDF)](../Lab%203%20-%20Build%20MLops%20pipeline.pdf)  
- [Kubespray GitHub](https://github.com/kubernetes-sigs/kubespray)  
- [Argo Workflows Docs](https://argo-workflows.readthedocs.io)  
- [Chameleon Cloud Docs](https://www.chameleoncloud.org/docs/)  

---

For presentation walkthroughs or questions, reach out via GitHub Issues or during your assigned demo slot.
