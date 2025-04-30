
# Cloud Computing on Chameleon project35
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

The repository includes the following materials:

```
  -   uploads/
  -   static/
  -   templates/
  -   model.pth
  -   app.py
  -   requirements.txt
  -   Dockerfile
```



where

- `static` and `templates` are directories containing the HTML, CSS, and JavaScript files used to implement the front-end interface.
- `uploads/` is the folder where user-uploaded content images and generated stylized images are stored temporarily.
- `model.pth` is the trained TensorFlow style transfer model checkpoint.
- `app.py` implements the Flask web application that serves the model and handles image processing.
- `requirements.txt` specifies the Python packages required to run the application.
- `Dockerfile` provides the build instructions for containerizing the entire web application using Docker.


Use this file to build a container image as follows: we run

```bash
# run on node1 host
docker build -t vision-to-vintage-app:0.0.1 vision-to-vintage
```

which builds the image from the directory `vision-to-vintage`, gives the image the name `vision-to-vintage-app`, and gives it the tag `0.0.1` (typically this is a version number).
Run the container with

```bash
# run on node1 host
docker run -d -p 80:8000 vision-to-vintage-app:0.0.1
```

Put

```
http://129.114.25.100
```

in the address bar of any browser and try the service.

