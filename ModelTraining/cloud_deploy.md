
# Cloud Computing on Chameleon project35 -- Start the web application
Style Transfer Web Service Deployment on Chameleon

## Completed Tasks

- Successfully created and configured a VM on Chameleon (KVM@TACC site).
- Floating IP has been allocated and SSH access to the VM has been confirmed.
- Docker has been installed on the VM.
- Project source code cloned into the VM from GitHub.
- Dockerfile has been created and tested to package the style transfer web app.


## Implementation Details

* **Compute resources**: one virtual machine instances.
* **Network resources**: 
  * the VM is attached to an Internet-connected network.
  * the VM is also be attached to a "private" network that we provision, on which the virtual machine instances can communicate with one another. We use the subnet on this network: 192.168.1.0/24. 
  * We get a publicly routable "floating IP: 129.114.25.100" address for one of the VM instances.


###  Provision resources using the GUI

I provisioned resources using the OpenStack graphical user interface, which is called Horizon, to provision our resources. Click "Experiment" > "KVM@TACC"

On the left side of the interface, expand the "Network" menu
* Choose the "Networks" option
* our private network is named as "private_cloud_net_project35" on the list.

Creating details:

* On the first ("Network") tab, specify the network name as <code>private_cloud_net_project35</code> . Leave other settings at their defaults, and click "Next".
* On the second ("Subnet") tab, specify the subnet name as <code>private_cloud_subnet_project35</code> . Specify the subnet address as `192.168.1.0/24`. Check the "Disable gateway" box. Leave other settings at their defaults, and click "Next".
* On the third ("Subnet Details") tab, leave all settings at their default values. Click "Create".

### Provision a port on our "private" network

Create a port on our "private" network, and later we will attach a compute instance to it. Creating details:

* On the left side of the interface, expand the "Network" menu
* Choose the "Networks" option
* Click on the <code>private_cloud_subnet_project35</code> network created earlier.
* Choose the "Ports" tab from the options on the top.
* Click "Create Port".

I've set up the port as follows:

* Leave "Name" blank
* In the "Specify IP address or subnet" menu, choose "Fixed IP address"
* Then, in the "Fixed IP Address" field, put `192.168.1.11`
* Un-check the box next to "Port Security"
* Leave other settings at their default values
* Click "Create".

### Provision the VM instance

* On the left side of the interface, expand the "Compute" menu
* Choose the "Instances" option
* Our Instance is named as "node1-project35" on the list

Creating details:

* On the first ("Details") tab, set the instance name to  <code>node1-project35</code> . Leave other settings at their default values, and click "Next".
* In the second ("Source") tab, choose `CC-Ubuntu24.04`. Click "Next".
* In the third ("Flavor") tab, use `m1.medium` . Click "Next".
* In the fourth ("Networks") tab, we will attach the instance to a network provided by the infrastructure provider which is connected to the Internet.
  * From the "Available" list, click on the arrow next to `sharednet1`. It will appear as item 1 in the "Allocated" list. 
  * Click "Next".
* In the fifth ("Ports") tab, use the port we just created to attach the instance to the private network we created earlier. 
  * From the "Available" list, find the port you created earlier. 
  * Click "Next".
* In the sixth ("Security Groups") tab, `allow-ssh` and `allow-http-80`
  * Click "Next".
* In the seventh ("Key Pair") tab, find the SSH key associated with our laptop on the "Available" list. Named as "`id_rsa_chameleon_35`" Click on the arrow next to it to move it to the "Allocated" section. 
* In the eighth ("Customization") tab, paste the following into the text input field:

```
#cloud-config
runcmd:
  - echo "127.0.1.1 $(hostname)" >> /etc/hosts
  - su cc -c /usr/local/bin/cc-load-public-keys
```

Then "Launch Instance" (the remaining tabs are not required).


### Provision a floating IP

I provisioned and attached a "floating IP", our assigned floating ip is: `129.114.25.100` .creating details:

* On the left side of the interface, expand the "Network" menu
* Choose the "Floating IPs" option
* Click "Allocate IP to project"
* In the "Pool" menu, choose "public"
* In the "Description" field, write: <code>Cloud IP for project35</code>.
* Click "Allocate IP"
* Then, choose "Associate" next to "your" IP in the list.
* In the "Port" menu, choose the port associated with our instance on the `shared1` network, with an IP address of the form `10.56.X.X`.
* Click "Associate".


### Access your instance over SSH

First we have a shared public key(`id_rsa_chameleon_35.pub`) and private key(`id_rsa_chameleon_35`) pair to every group member. The public key was uploaded to everyone's chameleon account on site KVM@TACC, CHI@TACC, and CHI@UC and the private key is saved inside everyone's local folder (`/Users/your-username/.ssh/` in default). 

Now, access the instance over SSH. From local terminal, run

```
ssh -i ~/.ssh/id_rsa_chameleon_35 cc@129.114.25.100
```

confirm that you can access the compute instance. Run

```
hostnamectl
```

inside this SSH session to see details about the host.

Also, run
```
echo "127.0.0.1 $(hostname)" | sudo tee -a /etc/hosts
```

inside the SSH session


### Deploy a service in a Docker container

Install a container engine

First, [install the Docker engine](https://docs.docker.com/engine/install/ubuntu/). On `node1`, run

```bash
# run on node1 host
sudo apt-get update
sudo apt-get -y install ca-certificates curl

sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

# Install packages
sudo apt-get -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Before we can run `docker` commands as an unprivileged user, we need to add the user to the `docker` group:

```bash
# run on node1 host
sudo groupadd -f docker; sudo usermod -aG docker $USER
```

then, end the SSH session (`exit`) and open a new one for the change to be reflected. 

Open a new SSH session, run 

```bash
# run on node1 host
id
```

can see a  group named `docker` listed in the output, indicating that the `cc` user is part of the `docker` group. 

```bash
# run on node1 host
docker run hello-world
```

see a "Hello from Docker!" message.

### Build and serve a container for a machine learning model

Then I built our own container, and used it to serve our machine learning model.

The premise of this service is: We are developing an online creative platform focused on artistic photo transformations. We are testing a new model you have developed that automatically applies different artistic styles to user-uploaded images, allowing users to transform their photos into artworks inspired by various visual styles. We have built a simple web application with which to test our model and gather feedback from users on the quality of the style transfer results.

The source code for our web application is at: [M0n4GPT/vision-to-vintage](https://github.com/M0n4GPT/vision-to-vintage). Retrieve it on node1 with

```bash
# run on node1 host
git clone https://github.com/M0n4GPT/vision-to-vintage vision-to-vintage
```

The repository has two folder, open the /web/ folder, it includes the following materials:

```
  -   uploads/
  -   static/
  -   templates/
  -   models/
  -   app.py
  -   app_torch.py
  -   requirements.txt
  -   Dockerfile
```



where

- `static` and `templates` are directories containing the HTML, CSS, and JavaScript files used to implement the front-end interface.
- `uploads/` is the folder where user-uploaded content images and generated stylized images are stored temporarily.
- `models/` include different versions of the trained style transfer model checkpoint.
- `app.py` implements the Flask web application that serves the model and handles image processing.
- `requirements.txt` specifies the Python packages required to run the application.
- `Dockerfile` provides the build instructions for containerizing the entire web application using Docker.


Use this file to build a container image as follows: we run

```bash
# run on node1 host
docker build -t vision-to-vintage-app:0.0.1 vision-to-vintage/web
```

which builds the image from the directory `vision-to-vintage`, gives the image the name `vision-to-vintage-app`, and gives it the tag `0.0.1` (typically this is a version number).
Run the container with

```bash
# run on node1 host
# docker run -d -p 80:8000 vision-to-vintage-app:0.0.1
docker run -d   --name vision_app   -p 9090:9090   --restart=always   --memory=2g   vision-to-vintage-app:0.0.1
```

Put

```
http://129.114.25.100:9090
```

in the address bar of any browser and try the service.

##  Model Overview

| Model Name          | Style Classes | Training Method         | GPU Usage    |
|---------------------|---------------|--------------------------|--------------|
| `stylizer10_ddp.pt` | 10            | DDP  | 2 GPUs       |
| `stylizer50_6.pt`   | 50            | Single-GPU               | 1 GPU        |
| `stylizer50_7.pt`   | 50            | DDP                      | 2 GPUs       |

---

##  Model Architecture

All three models share the same architecture based on [VGG19](https://arxiv.org/abs/1409.1556) for encoding and a custom decoder. The overall structure is:

###  Encoder
- Based on pretrained `torchvision.models.vgg19.features`
- Frozen during training

###  AdaIN Layer
Adaptive Instance Normalization is applied to blend the content and style feature maps:
```python
t = (c_feat - mean(c_feat)) / std(c_feat) * std(s_feat) + mean(s_feat)
```
### Decoder
```python
Sequential(
    Conv2d(512, 256, kernel_size=3, padding=1), ReLU(),
    Upsample(scale_factor=2),
    Conv2d(256, 128, kernel_size=3, padding=1), ReLU(),
    Upsample(scale_factor=2),
    Conv2d(128, 64,  kernel_size=3, padding=1), ReLU(),
    Upsample(scale_factor=2),
    Conv2d(64, 32,   kernel_size=3, padding=1), ReLU(),
    Upsample(scale_factor=2),
    Upsample(scale_factor=2),
    Conv2d(32, 3,    kernel_size=3, padding=1)
)
```



## Issue with VM and the solution

After the VM instance running for a few hours(43327.034081seconds/~12 hours), the VM encountered serious disk I/O errors. The filesystem was remounted as read-only, and services like SSH stopped working.
The log file looks something like this:


<div style="max-height:250px; overflow-y:auto; background:#f6f8fa; padding:10px; border:1px solid #ddd; border-radius:5px;">

<pre><code>
<14>Apr 25 07:39:05 cloud-init: #############################################################
<14>Apr 25 07:39:05 cloud-init: -----BEGIN SSH HOST KEY FINGERPRINTS-----
<14>Apr 25 07:39:05 cloud-init: 256 SHA256:16MkCkZ9CfTzudwh8y17xAh3uxM/D9nl+hinR1DmKRU root@node1-project35 (ECDSA)
<14>Apr 25 07:39:05 cloud-init: 256 SHA256:Jt9NeGm6TddYWpqJf8Ag9ozBTxRoCb/NNJZHK5lPpqs root@node1-project35 (ED25519)
<14>Apr 25 07:39:05 cloud-init: 3072 SHA256:3oEee04Zjyz8YuqhqN6y9FZ7qXapo/oO8gfux+P7xA8 root@node1-project35 (RSA)
<14>Apr 25 07:39:05 cloud-init: -----END SSH HOST KEY FINGERPRINTS-----
<14>Apr 25 07:39:05 cloud-init: #############################################################
-----BEGIN SSH HOST KEY KEYS-----
ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBDIhQbwEc2peFU6RewnLj0Q5eAQB8h9FkFQID5zFGuQofMTMEm2wB2f+QEQDYLD9P5scCOCbUjCcjPzL0TxLZJs= root@node1-project35
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILygpX+5llSnaPPNK4z6bAx8zqdTbHcceXlLENa+C1YY root@node1-project35
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDMzGmXK6frG2G4jhTxVNi7U18d/JWXeVqoaBpa55aVVWgsIxS2R3u9CjS60YntVXs+Ht5iqRsm4oJdZ0ixtUhZ9GCafq1mGrOBLGRx45dLNZw7mjkuXVcrQ0zHvWfaCcbUFt62fJqXbfBh+DLaX+zFH3lEiPvOyrjNggWC7szAe+sspO/cZJIa5H/Tgja4UEVl29V3PGvRtGPYG9GwUMpaKGc3abkNsQaI27+KBO9mOQcBDQtBLDWpvxpn1DHcFgw7V+AM91qYIDj6LLyZWZZaGOkoVbUqqW0j0kB6oUWOcVQp8HuVxnhfM4Q8YKMFkOcEv0V/LLKupWC7zxoQh7gOb6c1QHOYnNMtLMjzpxAys8ISumHbpVOe4noL/TtFN2XY2A9UsEUnX0kYy1dF3E98+zFLiYT7XWfxIlPlxsIeti4cfzuuvz7CdEMFIzjDG2ymOiDgV1/pqdUoLEfdGZXY97DZBzR2RiU6K12z4HYuPuMh1yPyMFl9CPOmk8tKiAk= root@node1-project35
-----END SSH HOST KEY KEYS-----
[   31.830950] cloud-init[1276]: Cloud-init v. 24.3.1-0ubuntu0~24.04.2 finished at Fri, 25 Apr 2025 07:39:05 +0000. Datasource DataSourceOpenStackLocal [net,ver=2].  Up 31.82 seconds
[43327.034081] I/O error, dev vda, sector 5650768 op 0x1:(WRITE) flags 0x9800 phys_seg 1 prio class 2
[43327.038279] Aborting journal on device vda3-8.
[43327.039611] EXT4-fs error (device vda3): ext4_journal_check_start:84: comm rs:main Q:Reg: Detected aborted journal
[43327.039635] EXT4-fs error (device vda3): ext4_journal_check_start:84: comm systemd-journal: Detected aborted journal
[43327.047046] I/O error, dev vda, sector 5601280 op 0x1:(WRITE) flags 0x9800 phys_seg 1 prio class 2
[43327.048365] Buffer I/O error on dev vda3, logical block 557056, lost sync page write
[43327.049578] JBD2: I/O error when updating journal superblock for vda3-8.
[43327.054271] I/O error, dev vda, sector 1144832 op 0x1:(WRITE) flags 0x3800 phys_seg 1 prio class 0
[43327.055824] Buffer I/O error on dev vda3, logical block 0, lost sync page write
[43327.057015] EXT4-fs (vda3): I/O error while writing superblock
[43327.057081] EXT4-fs (vda3): previous I/O error to superblock detected
[43327.057947] EXT4-fs (vda3): Remounting filesystem read-only
[43327.064223] I/O error, dev vda, sector 1144832 op 0x1:(WRITE) flags 0x3800 phys_seg 1 prio class 0
[43327.065879] Buffer I/O error on dev vda3, logical block 0, lost sync page write
[43327.067285] EXT4-fs (vda3): I/O error while writing superblock
[70910.964530] systemd-journald[300]: Failed to rotate /var/log/journal/b3e723676cd4458880f8165504d6f386/system.journal: Read-only file system
[70910.966747] systemd-journald[300]: Failed to rotate /var/log/journal/b3e723676cd4458880f8165504d6f386/user-1000.journal: Read-only file system
[70910.968331] systemd-journald[300]: Failed to write entry to /var/log/journal/b3e723676cd4458880f8165504d6f386/system.journal (23 items, 836 bytes) despite vacuuming, ignoring: Input/output error
[70931.158691] systemd-journald[300]: Failed to rotate /var/log/journal/b3e723676cd4458880f8165504d6f386/system.journal: Read-only file system
[70931.162183] systemd-journald[300]: Failed to write entry to /var/log/journal/b3e723676cd4458880f8165504d6f386/system.journal (23 items, 705 bytes) despite vacuuming, ignoring: Input/output error
[70985.356020] systemd-journald[300]: Failed to rotate /var/log/journal/b3e723676cd4458880f8165504d6f386/system.journal: Read-only file system (Dropped 41 similar message(s))
[70985.360192] systemd-journald[300]: Failed to rotate /var/log/journal/b3e723676cd4458880f8165504d6f386/user-1000.journal: Read-only file system
[70985.363645] systemd-journald[300]: Failed to write entry to /var/log/journal/b3e723676cd4458880f8165504d6f386/system.journal (23 items, 705 bytes) despite vacuuming, ignoring: Input/output error (Dropped 20 similar message(s))
</code></pre>

</div>

It's because of the outage at KVM@TACC specifically related to block storage/hard disks. After the issue was resolved, rebooting the VM instance, and restart by:
```bash
# run on node1 host
# docker run -d -p 80:8000 vision-to-vintage-app:0.0.1
docker run -d   --name vision_app   -p 9090:9090   --restart=always   --memory=2g   vision-to-vintage-app:0.0.1
```
The service should now be running normally.
