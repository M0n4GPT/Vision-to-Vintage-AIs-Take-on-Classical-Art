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
