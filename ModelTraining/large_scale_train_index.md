# Model Training on Chameleon

## Launch and set up AMD MI100 server - with python-chi

```python
from chi import server, context, lease
import os, time

context.version = "1.0" 
context.choose_project()
context.choose_site(default="CHI@TACC")
```

```
VBox(children=(Dropdown(description='Select Project', options=('CHI-251409',), value='CHI-251409'), Output()))
VBox(children=(Dropdown(description='Select Site', options=('CHI@TACC', 'CHI@UC', 'CHI@EVL', 'CHI@NCAR', 'CHI@…
```

```python
l = lease.get_lease(f"train_infra_project35_1") 
l.show()
```

```
HTML(value='\n        <h2>Lease Details</h2>\n        <table>\n            <tr><th>Name</th><td>train_infra_pr…


Lease Details:
Name: train_infra_project35_1
ID: 9d920b57-f316-4da9-8cec-31f8fee8e537
Status: ACTIVE
Start Date: 2025-05-07 18:00:00
End Date: 2025-05-07 23:55:00
User ID: b47b677115e1dbbb5a28b1e0aba16c88c2a1b3f108f89e257536d6d2c5a56379
Project ID: d3c6e101843a4ba79e665ebf59b521a2

Node Reservations:
ID: 4fa08b4c-a34e-494d-9cb0-40243d3a1c75, Status: active, Min: 1, Max: 1

Floating IP Reservations:

Network Reservations:

Events:
```

```python
username = os.getenv('USER') # all exp resources will have this prefix
s = server.Server(
    f"node-{username}", 
    reservation_id=l.node_reservations[0]["id"],
    image_name="CC-Ubuntu24.04-hwe"
)
s.submit(idempotent=True)
```

Waiting for server node-mltrain-netID_nyu_edu's status to become ACTIVE. This typically takes 10 minutes, but can take up to 20 minutes.

<div style="max-height:300px; overflow:auto; background:#f9f9f9; line-height: 1.2; boder:1px solid #ccc; padding:0px; font-family:monospace;font-size: 9px; white-space:pre;">

```
HBox(children=(Label(value=''), IntProgress(value=0, bar_style='success')))


Server has moved to status ACTIVE
```

</div>

<table style='border-collapse: collapse; width: 100%;'><tr style='background-color: #f2f2f2;'><th style='border: 1px solid #ddd; padding: 8px;'>Attribute</th><th style='border: 1px solid #ddd; padding: 8px;'>node-mltrain_netID_nyu_edu</th></tr><tr><td style='border: 1px solid #ddd; padding: 8px;'>Id</td><td style='border: 1px solid #ddd; padding: 8px;'>47cd9b1f-11f8-495c-9293-e3df5a5f94ed</td></tr><tr><td style='border: 1px solid #ddd; padding: 8px;'>Status</td><td style='border: 1px solid #ddd; padding: 8px;'>ACTIVE</td></tr><tr><td style='border: 1px solid #ddd; padding: 8px;'>Image Name</td><td style='border: 1px solid #ddd; padding: 8px;'>CC-Ubuntu24.04-hwe</td></tr><tr><td style='border: 1px solid #ddd; padding: 8px;'>Flavor Name</td><td style='border: 1px solid #ddd; padding: 8px;'>baremetal</td></tr><tr><td style='border: 1px solid #ddd; padding: 8px;'>Addresses</td><td style='border: 1px solid #ddd; padding: 8px;'><strong>sharednet1:</strong><br>&nbsp;&nbsp;IP: 10.52.3.95 (v4)<br>&nbsp;&nbsp;Type: fixed<br>&nbsp;&nbsp;MAC: 34:80:0d:de:52:98<br></td></tr><tr><td style='border: 1px solid #ddd; padding: 8px;'>Network Name</td><td style='border: 1px solid #ddd; padding: 8px;'>sharednet1</td></tr><tr><td style='border: 1px solid #ddd; padding: 8px;'>Created At</td><td style='border: 1px solid #ddd; padding: 8px;'>2025-05-07T18:22:21Z</td></tr><tr><td style='border: 1px solid #ddd; padding: 8px;'>Keypair</td><td style='border: 1px solid #ddd; padding: 8px;'>netID_nyu_edu-jupyter</td></tr><tr><td style='border: 1px solid #ddd; padding: 8px;'>Reservation Id</td><td style='border: 1px solid #ddd; padding: 8px;'>4fa08b4c-a34e-494d-9cb0-40243d3a1c75</td></tr><tr><td style='border: 1px solid #ddd; padding: 8px;'>Host Id</td><td style='border: 1px solid #ddd; padding: 8px;'>9acf860df16fe3cd915f9522cd52cf171577a815ef5c486f67a143e3</td></tr><tr><td style='border: 1px solid #ddd; padding: 8px;'>Host Status</td><td style='border: 1px solid #ddd; padding: 8px;'>None</td></tr><tr><td style='border: 1px solid #ddd; padding: 8px;'>Hypervisor Hostname</td><td style='border: 1px solid #ddd; padding: 8px;'>af43f51c-49c9-40fb-a923-d87748de9be8</td></tr><tr><td style='border: 1px solid #ddd; padding: 8px;'>Is Locked</td><td style='border: 1px solid #ddd; padding: 8px;'>False</td></tr></table>

```python
s.associate_floating_ip()
```

```python
s.refresh()
s.check_connectivity()
```

<div style="max-height:300px; overflow:auto; background:#f9f9f9; line-height: 1.2; boder:1px solid #ccc; padding:0px; font-family:monospace;font-size: 9px; white-space:pre;">

```
Checking connectivity to 129.114.108.92 port 22.



HBox(children=(Label(value=''), IntProgress(value=0, bar_style='success')))


Connection successful
```

</div>

```python
s.refresh()
s.show(type="widget")
```

<table style='border-collapse: collapse; width: 100%;'><tr style='background-color: #f2f2f2;'><th style='border: 1px solid #ddd; padding: 8px;'>Attribute</th><th style='border: 1px solid #ddd; padding: 8px;'>node-mltrain-netID_nyu_edu</th></tr><tr><td style='border: 1px solid #ddd; padding: 8px;'>Id</td><td style='border: 1px solid #ddd; padding: 8px;'>47cd9b1f-11f8-495c-9293-e3df5a5f94ed</td></tr><tr><td style='border: 1px solid #ddd; padding: 8px;'>Status</td><td style='border: 1px solid #ddd; padding: 8px;'>ACTIVE</td></tr><tr><td style='border: 1px solid #ddd; padding: 8px;'>Image Name</td><td style='border: 1px solid #ddd; padding: 8px;'>CC-Ubuntu24.04-hwe</td></tr><tr><td style='border: 1px solid #ddd; padding: 8px;'>Flavor Name</td><td style='border: 1px solid #ddd; padding: 8px;'>baremetal</td></tr><tr><td style='border: 1px solid #ddd; padding: 8px;'>Addresses</td><td style='border: 1px solid #ddd; padding: 8px;'><strong>sharednet1:</strong><br>&nbsp;&nbsp;IP: 10.52.3.95 (v4)<br>&nbsp;&nbsp;Type: fixed<br>&nbsp;&nbsp;MAC: 34:80:0d:de:52:98<br>&nbsp;&nbsp;IP: 129.114.108.92 (v4)<br>&nbsp;&nbsp;Type: floating<br>&nbsp;&nbsp;MAC: 34:80:0d:de:52:98<br></td></tr><tr><td style='border: 1px solid #ddd; padding: 8px;'>Network Name</td><td style='border: 1px solid #ddd; padding: 8px;'>sharednet1</td></tr><tr><td style='border: 1px solid #ddd; padding: 8px;'>Created At</td><td style='border: 1px solid #ddd; padding: 8px;'>2025-05-07T18:22:21Z</td></tr><tr><td style='border: 1px solid #ddd; padding: 8px;'>Keypair</td><td style='border: 1px solid #ddd; padding: 8px;'>netID_nyu_edu-jupyter</td></tr><tr><td style='border: 1px solid #ddd; padding: 8px;'>Reservation Id</td><td style='border: 1px solid #ddd; padding: 8px;'>4fa08b4c-a34e-494d-9cb0-40243d3a1c75</td></tr><tr><td style='border: 1px solid #ddd; padding: 8px;'>Host Id</td><td style='border: 1px solid #ddd; padding: 8px;'>9acf860df16fe3cd915f9522cd52cf171577a815ef5c486f67a143e3</td></tr><tr><td style='border: 1px solid #ddd; padding: 8px;'>Host Status</td><td style='border: 1px solid #ddd; padding: 8px;'>None</td></tr><tr><td style='border: 1px solid #ddd; padding: 8px;'>Hypervisor Hostname</td><td style='border: 1px solid #ddd; padding: 8px;'>af43f51c-49c9-40fb-a923-d87748de9be8</td></tr><tr><td style='border: 1px solid #ddd; padding: 8px;'>Is Locked</td><td style='border: 1px solid #ddd; padding: 8px;'>False</td></tr></table>

### Retrieve code and notebooks on the instance

```python
s.execute("git clone --recurse-submodules https://github.com/M0n4GPT/vision-to-vintage")
```

```
/opt/conda/lib/python3.10/site-packages/paramiko/client.py:889: UserWarning: Unknown ssh-ed25519 host key for 129.114.108.92: b'e688cac65758d647def4d43b3772d2a8'
  warnings.warn(
Cloning into 'vision-to-vintage'...





<Result cmd='git clone --recurse-submodules https://github.com/M0n4GPT/vision-to-vintage' exited=0>
```

```python
s.execute("mv vision-to-vintage/style_transfer ./style_transfer")
s.execute("rm -rf vision-to-vintage")
```

```
<Result cmd='rm -rf vision-to-vintage' exited=0>
```

### Set up Docker

To use common deep learning frameworks like Tensorflow or PyTorch, and ML training platforms like MLFlow and Ray, run containers that have all the prerequisite libraries necessary for these frameworks. Here, we set up the container framework.

```python
s.execute("curl -sSL https://get.docker.com/ | sudo sh")
s.execute("sudo groupadd -f docker; sudo usermod -aG docker $USER")
```

<div style="max-height:300px; overflow:auto; background:#f9f9f9; line-height: 1.2; boder:1px solid #ccc; padding:0px; font-family:monospace;font-size: 9px; white-space:pre;">

```
# Executing docker install script, commit: 53a22f61c0628e58e1d6680b49e82993d304b449


+ sh -c apt-get -qq update >/dev/null
+ sh -c DEBIAN_FRONTEND=noninteractive apt-get -y -qq install ca-certificates curl >/dev/null
+ sh -c install -m 0755 -d /etc/apt/keyrings
+ sh -c curl -fsSL "https://download.docker.com/linux/ubuntu/gpg" -o /etc/apt/keyrings/docker.asc
+ sh -c chmod a+r /etc/apt/keyrings/docker.asc
+ sh -c echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu noble stable" > /etc/apt/sources.list.d/docker.list
+ sh -c apt-get -qq update >/dev/null
+ sh -c DEBIAN_FRONTEND=noninteractive apt-get -y -qq install docker-ce docker-ce-cli containerd.io docker-compose-plugin docker-ce-rootless-extras docker-buildx-plugin >/dev/null

Running kernel seems to be up-to-date.

The processor microcode seems to be up-to-date.

No services need to be restarted.

No containers need to be restarted.

No user sessions are running outdated binaries.

No VM guests are running outdated hypervisor (qemu) binaries on this host.
+ sh -c docker version


Client: Docker Engine - Community
 Version:           28.1.1
 API version:       1.49
 Go version:        go1.23.8
 Git commit:        4eba377
 Built:             Fri Apr 18 09:52:14 2025
 OS/Arch:           linux/amd64
 Context:           default

Server: Docker Engine - Community
 Engine:
  Version:          28.1.1
  API version:      1.49 (minimum version 1.24)
  Go version:       go1.23.8
  Git commit:       01f442b
  Built:            Fri Apr 18 09:52:14 2025
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          1.7.27
  GitCommit:        05044ec0a9a75232cad458027ca83437aae3f4da
 runc:
  Version:          1.2.5
  GitCommit:        v1.2.5-0-g59923ef
 docker-init:
  Version:          0.19.0
  GitCommit:        de40ad0

================================================================================

To run Docker as a non-privileged user, consider setting up the
Docker daemon in rootless mode for your user:

    dockerd-rootless-setuptool.sh install

Visit https://docs.docker.com/go/rootless/ to learn about rootless mode.


To run the Docker daemon as a fully privileged service, but granting non-root
users access, refer to https://docs.docker.com/go/daemon-access/

WARNING: Access to the remote API on a privileged Docker daemon is equivalent
         to root access on the host. Refer to the 'Docker daemon attack surface'
         documentation for details: https://docs.docker.com/go/attack-surface/

================================================================================






<Result cmd='sudo groupadd -f docker; sudo usermod -aG docker $USER' exited=0>
```

</div>

### Set up the AMD GPU

Before we can use the AMD GPUs, we also need to set up the driver using the amdgpu-install utility.

```python
s.execute("sudo apt update; wget https://repo.radeon.com/amdgpu-install/6.3.3/ubuntu/noble/amdgpu-install_6.3.60303-1_all.deb")
s.execute("sudo apt -y install ./amdgpu-install_6.3.60303-1_all.deb; sudo apt update")
```

<div style="max-height:300px; overflow:auto; background:#f9f9f9; line-height: 1.2; boder:1px solid #ccc; padding:0px; font-family:monospace;font-size: 9px; white-space:pre;">

```
WARNING: apt does not have a stable CLI interface. Use with caution in scripts.



Hit:1 https://download.docker.com/linux/ubuntu noble InRelease
Hit:2 http://security.ubuntu.com/ubuntu noble-security InRelease
Get:3 http://nova.clouds.archive.ubuntu.com/ubuntu noble InRelease [256 kB]
Hit:4 http://nova.clouds.archive.ubuntu.com/ubuntu noble-updates InRelease
Hit:5 http://nova.clouds.archive.ubuntu.com/ubuntu noble-backports InRelease
Fetched 256 kB in 1s (249 kB/s)
Reading package lists...
Building dependency tree...
Reading state information...
145 packages can be upgraded. Run 'apt list --upgradable' to see them.


--2025-05-07 18:35:51--  https://repo.radeon.com/amdgpu-install/6.3.3/ubuntu/noble/amdgpu-install_6.3.60303-1_all.deb
Resolving repo.radeon.com (repo.radeon.com)... 23.221.22.215, 23.221.22.214, 2600:1404:6400:25::17de:f148, ...
Connecting to repo.radeon.com (repo.radeon.com)|23.221.22.215|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 16984 (17K) [application/octet-stream]
Saving to: ‘amdgpu-install_6.3.60303-1_all.deb’

     0K .......... ......                                     100% 33.1M=0s

2025-05-07 18:35:51 (33.1 MB/s) - ‘amdgpu-install_6.3.60303-1_all.deb’ saved [16984/16984]


WARNING: apt does not have a stable CLI interface. Use with caution in scripts.



Reading package lists...
Building dependency tree...
Reading state information...
Recommended packages:
  dialog
The following NEW packages will be installed:
  amdgpu-install
0 upgraded, 1 newly installed, 0 to remove and 145 not upgraded.
Need to get 0 B/17.0 kB of archives.
After this operation, 74.8 kB of additional disk space will be used.
Get:1 /home/cc/amdgpu-install_6.3.60303-1_all.deb amdgpu-install all 6.3.60303-2119913.24.04 [17.0 kB]


debconf: unable to initialize frontend: Dialog
debconf: (Dialog frontend will not work on a dumb terminal, an emacs shell buffer, or without a controlling terminal.)
debconf: falling back to frontend: Readline
debconf: unable to initialize frontend: Readline
debconf: (This frontend requires a controlling tty.)
debconf: falling back to frontend: Teletype
dpkg-preconfigure: unable to re-open stdin: 


Selecting previously unselected package amdgpu-install.
(Reading database ... 93276 files and directories currently installed.)
Preparing to unpack .../amdgpu-install_6.3.60303-1_all.deb ...
Unpacking amdgpu-install (6.3.60303-2119913.24.04) ...
Setting up amdgpu-install (6.3.60303-2119913.24.04) ...


debconf: unable to initialize frontend: Dialog
debconf: (Dialog frontend will not work on a dumb terminal, an emacs shell buffer, or without a controlling terminal.)
debconf: falling back to frontend: Readline
debconf: unable to initialize frontend: Readline
debconf: (This frontend requires a controlling tty.)
debconf: falling back to frontend: Teletype

Running kernel seems to be up-to-date.

The processor microcode seems to be up-to-date.

No services need to be restarted.

No containers need to be restarted.

No user sessions are running outdated binaries.

No VM guests are running outdated hypervisor (qemu) binaries on this host.

WARNING: apt does not have a stable CLI interface. Use with caution in scripts.



Get:1 https://repo.radeon.com/amdgpu/6.3.3/ubuntu noble InRelease [5435 B]
Get:2 https://repo.radeon.com/rocm/apt/6.3.3 noble InRelease [2605 B]
Hit:3 https://download.docker.com/linux/ubuntu noble InRelease
Get:4 https://repo.radeon.com/amdgpu/6.3.3/ubuntu noble/main i386 Packages [12.2 kB]
Get:5 https://repo.radeon.com/amdgpu/6.3.3/ubuntu noble/main amd64 Packages [14.1 kB]
Get:6 https://repo.radeon.com/rocm/apt/6.3.3 noble/main amd64 Packages [60.0 kB]
Hit:7 http://security.ubuntu.com/ubuntu noble-security InRelease
Get:8 http://nova.clouds.archive.ubuntu.com/ubuntu noble InRelease [256 kB]
Hit:9 http://nova.clouds.archive.ubuntu.com/ubuntu noble-updates InRelease
Hit:10 http://nova.clouds.archive.ubuntu.com/ubuntu noble-backports InRelease
Fetched 350 kB in 1s (339 kB/s)
Reading package lists...
Building dependency tree...
Reading state information...
145 packages can be upgraded. Run 'apt list --upgradable' to see them.





<Result cmd='sudo apt -y install ./amdgpu-install_6.3.60303-1_all.deb; sudo apt update' exited=0>
```

</div>

```python
s.execute("amdgpu-install -y --usecase=dkms")
s.execute("sudo apt -y install rocm-smi")
s.execute("sudo usermod -aG video,render $USER")
```

<div style="max-height:300px; overflow:auto; background:#f9f9f9; line-height: 1.2; boder:1px solid #ccc; padding:0px; font-family:monospace;font-size: 9px; white-space:pre;">

```
Hit:1 https://download.docker.com/linux/ubuntu noble InRelease
Hit:2 https://repo.radeon.com/amdgpu/6.3.3/ubuntu noble InRelease
Get:3 http://nova.clouds.archive.ubuntu.com/ubuntu noble InRelease [256 kB]
Hit:4 https://repo.radeon.com/rocm/apt/6.3.3 noble InRelease
Hit:5 http://security.ubuntu.com/ubuntu noble-security InRelease
Get:6 http://nova.clouds.archive.ubuntu.com/ubuntu noble-updates InRelease [126 kB]
Get:7 http://nova.clouds.archive.ubuntu.com/ubuntu noble-backports InRelease [126 kB]
Get:8 http://nova.clouds.archive.ubuntu.com/ubuntu noble-updates/main amd64 Packages [1066 kB]
Get:9 http://nova.clouds.archive.ubuntu.com/ubuntu noble-updates/main amd64 Components [161 kB]
Get:10 http://nova.clouds.archive.ubuntu.com/ubuntu noble-updates/universe amd64 Packages [1061 kB]
Get:11 http://nova.clouds.archive.ubuntu.com/ubuntu noble-updates/universe amd64 Components [376 kB]
Get:12 http://nova.clouds.archive.ubuntu.com/ubuntu noble-updates/restricted amd64 Components [212 B]
Get:13 http://nova.clouds.archive.ubuntu.com/ubuntu noble-updates/multiverse amd64 Packages [21.7 kB]
Get:14 http://nova.clouds.archive.ubuntu.com/ubuntu noble-updates/multiverse amd64 Components [940 B]
Get:15 http://nova.clouds.archive.ubuntu.com/ubuntu noble-backports/main amd64 Components [7064 B]
Get:16 http://nova.clouds.archive.ubuntu.com/ubuntu noble-backports/universe amd64 Components [16.4 kB]
Get:17 http://nova.clouds.archive.ubuntu.com/ubuntu noble-backports/restricted amd64 Components [216 B]
Get:18 http://nova.clouds.archive.ubuntu.com/ubuntu noble-backports/multiverse amd64 Components [212 B]
Fetched 3219 kB in 1s (3122 kB/s)
Reading package lists...
Reading package lists...
Building dependency tree...
Reading state information...
linux-headers-6.11.0-17-generic is already the newest version (6.11.0-17.17~24.04.2).
linux-headers-6.11.0-17-generic set to manually installed.
The following additional packages will be installed:
  amdgpu-dkms-firmware autoconf automake autotools-dev m4
Suggested packages:
  autoconf-archive gnu-standards autoconf-doc libtool gettext m4-doc
The following NEW packages will be installed:
  amdgpu-dkms amdgpu-dkms-firmware autoconf automake autotools-dev m4
0 upgraded, 6 newly installed, 0 to remove and 145 not upgraded.
Need to get 27.9 MB of archives.
After this operation, 620 MB of additional disk space will be used.
Get:1 https://repo.radeon.com/amdgpu/6.3.3/ubuntu noble/main amd64 amdgpu-dkms-firmware all 1:6.10.5.60303-2119913.24.04 [15.1 MB]
Get:2 http://nova.clouds.archive.ubuntu.com/ubuntu noble/main amd64 m4 amd64 1.4.19-4build1 [244 kB]
Get:3 https://repo.radeon.com/amdgpu/6.3.3/ubuntu noble/main amd64 amdgpu-dkms all 1:6.10.5.60303-2119913.24.04 [11.6 MB]
Get:4 http://nova.clouds.archive.ubuntu.com/ubuntu noble/main amd64 autoconf all 2.71-3 [339 kB]
Get:5 http://nova.clouds.archive.ubuntu.com/ubuntu noble/main amd64 autotools-dev all 20220109.1 [44.9 kB]
Get:6 http://nova.clouds.archive.ubuntu.com/ubuntu noble/main amd64 automake all 1:1.16.5-1.3ubuntu1 [558 kB]


debconf: unable to initialize frontend: Dialog
debconf: (Dialog frontend will not work on a dumb terminal, an emacs shell buffer, or without a controlling terminal.)
debconf: falling back to frontend: Readline
debconf: unable to initialize frontend: Readline
debconf: (This frontend requires a controlling tty.)
debconf: falling back to frontend: Teletype
dpkg-preconfigure: unable to re-open stdin: 


Fetched 27.9 MB in 0s (56.0 MB/s)
Selecting previously unselected package m4.
(Reading database ... 93294 files and directories currently installed.)
Preparing to unpack .../0-m4_1.4.19-4build1_amd64.deb ...
Unpacking m4 (1.4.19-4build1) ...
Selecting previously unselected package autoconf.
Preparing to unpack .../1-autoconf_2.71-3_all.deb ...
Unpacking autoconf (2.71-3) ...
Selecting previously unselected package autotools-dev.
Preparing to unpack .../2-autotools-dev_20220109.1_all.deb ...
Unpacking autotools-dev (20220109.1) ...
Selecting previously unselected package automake.
Preparing to unpack .../3-automake_1%3a1.16.5-1.3ubuntu1_all.deb ...
Unpacking automake (1:1.16.5-1.3ubuntu1) ...
Selecting previously unselected package amdgpu-dkms-firmware.
Preparing to unpack .../4-amdgpu-dkms-firmware_1%3a6.10.5.60303-2119913.24.04_all.deb ...
Unpacking amdgpu-dkms-firmware (1:6.10.5.60303-2119913.24.04) ...
Selecting previously unselected package amdgpu-dkms.
Preparing to unpack .../5-amdgpu-dkms_1%3a6.10.5.60303-2119913.24.04_all.deb ...
Unpacking amdgpu-dkms (1:6.10.5.60303-2119913.24.04) ...
Setting up m4 (1.4.19-4build1) ...
Setting up autotools-dev (20220109.1) ...
Setting up autoconf (2.71-3) ...
Setting up amdgpu-dkms-firmware (1:6.10.5.60303-2119913.24.04) ...
Setting up automake (1:1.16.5-1.3ubuntu1) ...
update-alternatives: using /usr/bin/automake-1.16 to provide /usr/bin/automake (automake) in auto mode
Setting up amdgpu-dkms (1:6.10.5.60303-2119913.24.04) ...
debconf: unable to initialize frontend: Dialog
debconf: (Dialog frontend will not work on a dumb terminal, an emacs shell buffer, or without a controlling terminal.)
debconf: falling back to frontend: Readline
debconf: unable to initialize frontend: Readline
debconf: (This frontend requires a controlling tty.)
debconf: falling back to frontend: Teletype
Loading new amdgpu-6.10.5-2119913.24.04 DKMS files...
Building for 6.11.0-17-generic
Building for architecture x86_64
Building initial module for 6.11.0-17-generic
Done.
Forcing installation of amdgpu

amdgpu.ko.zst:
Running module version sanity check.
 - Original module
 - Installation
   - Installing to /lib/modules/6.11.0-17-generic/updates/dkms/

amdttm.ko.zst:
Running module version sanity check.
 - Original module
 - Installation
   - Installing to /lib/modules/6.11.0-17-generic/updates/dkms/

amdkcl.ko.zst:
Running module version sanity check.
 - Original module
 - Installation
   - Installing to /lib/modules/6.11.0-17-generic/updates/dkms/

amd-sched.ko.zst:
Running module version sanity check.
 - Original module
 - Installation
   - Installing to /lib/modules/6.11.0-17-generic/updates/dkms/

amddrm_ttm_helper.ko.zst:
Running module version sanity check.
 - Original module
 - Installation
   - Installing to /lib/modules/6.11.0-17-generic/updates/dkms/

amddrm_buddy.ko.zst:
Running module version sanity check.
 - Original module
 - Installation
   - Installing to /lib/modules/6.11.0-17-generic/updates/dkms/

amdxcp.ko.zst:
Running module version sanity check.
 - Original module
 - Installation
   - Installing to /lib/modules/6.11.0-17-generic/updates/dkms/
depmod...
update-initramfs: Generating /boot/initrd.img-6.11.0-17-generic
Processing triggers for man-db (2.12.0-4build2) ...
Processing triggers for install-info (7.1-3build2) ...


debconf: unable to initialize frontend: Dialog
debconf: (Dialog frontend will not work on a dumb terminal, an emacs shell buffer, or without a controlling terminal.)
debconf: falling back to frontend: Readline
debconf: unable to initialize frontend: Readline
debconf: (This frontend requires a controlling tty.)
debconf: falling back to frontend: Teletype

Running kernel seems to be up-to-date.

The processor microcode seems to be up-to-date.

No services need to be restarted.

No containers need to be restarted.

No user sessions are running outdated binaries.

No VM guests are running outdated hypervisor (qemu) binaries on this host.

WARNING: apt does not have a stable CLI interface. Use with caution in scripts.



Reading package lists...
Building dependency tree...
Reading state information...
The following additional packages will be installed:
  librocm-smi64-1
The following NEW packages will be installed:
  librocm-smi64-1 rocm-smi
0 upgraded, 2 newly installed, 0 to remove and 145 not upgraded.
Need to get 362 kB of archives.
After this operation, 1744 kB of additional disk space will be used.
Get:1 http://nova.clouds.archive.ubuntu.com/ubuntu noble/universe amd64 librocm-smi64-1 amd64 5.7.0-1 [309 kB]
Get:2 http://nova.clouds.archive.ubuntu.com/ubuntu noble/universe amd64 rocm-smi amd64 5.7.0-1 [52.9 kB]


debconf: unable to initialize frontend: Dialog
debconf: (Dialog frontend will not work on a dumb terminal, an emacs shell buffer, or without a controlling terminal.)
debconf: falling back to frontend: Readline
debconf: unable to initialize frontend: Readline
debconf: (This frontend requires a controlling tty.)
debconf: falling back to frontend: Teletype
dpkg-preconfigure: unable to re-open stdin: 


Fetched 362 kB in 1s (368 kB/s)
Selecting previously unselected package librocm-smi64-1.
(Reading database ... 97702 files and directories currently installed.)
Preparing to unpack .../librocm-smi64-1_5.7.0-1_amd64.deb ...
Unpacking librocm-smi64-1 (5.7.0-1) ...
Selecting previously unselected package rocm-smi.
Preparing to unpack .../rocm-smi_5.7.0-1_amd64.deb ...
Unpacking rocm-smi (5.7.0-1) ...
Setting up librocm-smi64-1 (5.7.0-1) ...
Setting up rocm-smi (5.7.0-1) ...
Processing triggers for man-db (2.12.0-4build2) ...
Processing triggers for libc-bin (2.39-0ubuntu8.4) ...


debconf: unable to initialize frontend: Dialog
debconf: (Dialog frontend will not work on a dumb terminal, an emacs shell buffer, or without a controlling terminal.)
debconf: falling back to frontend: Readline
debconf: unable to initialize frontend: Readline
debconf: (This frontend requires a controlling tty.)
debconf: falling back to frontend: Teletype

Running kernel seems to be up-to-date.

The processor microcode seems to be up-to-date.

No services need to be restarted.

No containers need to be restarted.

No user sessions are running outdated binaries.

No VM guests are running outdated hypervisor (qemu) binaries on this host.





<Result cmd='sudo usermod -aG video,render $USER' exited=0>
```

</div>

```python
s.execute("sudo reboot")
time.sleep(30)
```

```python
s.refresh()
s.check_connectivity()
```

```
Checking connectivity to 129.114.108.92 port 22.



HBox(children=(Label(value=''), IntProgress(value=0, bar_style='success')))


Connection successful
```

```python
s.execute("rocm-smi")
```

```
========================= ROCm System Management Interface =========================
=================================== Concise Info ===================================
GPU  Temp (DieEdge)  AvgPwr  SCLK    MCLK     Fan  Perf  PwrCap  VRAM%  GPU%  
0    24.0c           34.0W   300Mhz  1200Mhz  0%   auto  290.0W    0%   0%    
1    22.0c           34.0W   300Mhz  1200Mhz  0%   auto  290.0W    0%   0%    
====================================================================================
=============================== End of ROCm SMI Log ================================





<Result cmd='rocm-smi' exited=0>
```

and verify that you can see the GPU(s).

also install nvtop

```python
s.execute("sudo apt -y install cmake libncurses-dev libsystemd-dev libudev-dev libdrm-dev libgtest-dev")
s.execute("git clone https://github.com/Syllo/nvtop")
s.execute("mkdir -p nvtop/build && cd nvtop/build && cmake .. -DAMDGPU_SUPPORT=ON && sudo make install")
```

<div style="max-height:300px; overflow:auto; background:#f9f9f9; line-height: 1.2; boder:1px solid #ccc; padding:0px; font-family:monospace;font-size: 9px; white-space:pre;">

```
WARNING: apt does not have a stable CLI interface. Use with caution in scripts.



Reading package lists...
Building dependency tree...
Reading state information...
The following additional packages will be installed:
  cmake-data googletest libdrm-amdgpu1 libdrm-intel1 libdrm-nouveau2
  libdrm-radeon1 libjsoncpp25 libnss-systemd libpam-systemd libpciaccess-dev
  libpciaccess0 librhash0 libsystemd-shared libsystemd0 libudev1 systemd
  systemd-dev systemd-resolved systemd-sysv udev
Suggested packages:
  cmake-doc cmake-format elpa-cmake-mode ninja-build ncurses-doc
  systemd-container systemd-homed systemd-userdbd systemd-boot libqrencode4
  libtss2-rc0
The following NEW packages will be installed:
  cmake cmake-data googletest libdrm-amdgpu1 libdrm-dev libdrm-intel1
  libdrm-nouveau2 libdrm-radeon1 libgtest-dev libjsoncpp25 libncurses-dev
  libpciaccess-dev libpciaccess0 librhash0 libsystemd-dev libudev-dev
The following packages will be upgraded:
  libnss-systemd libpam-systemd libsystemd-shared libsystemd0 libudev1 systemd
  systemd-dev systemd-resolved systemd-sysv udev
10 upgraded, 16 newly installed, 0 to remove and 135 not upgraded.
Need to get 25.3 MB of archives.
After this operation, 64.9 MB of additional disk space will be used.
Get:1 http://nova.clouds.archive.ubuntu.com/ubuntu noble-updates/main amd64 systemd-dev all 255.4-1ubuntu8.6 [104 kB]
Get:2 http://nova.clouds.archive.ubuntu.com/ubuntu noble-updates/main amd64 systemd-resolved amd64 255.4-1ubuntu8.6 [296 kB]
Get:3 http://nova.clouds.archive.ubuntu.com/ubuntu noble-updates/main amd64 libsystemd-shared amd64 255.4-1ubuntu8.6 [2073 kB]
Get:4 http://nova.clouds.archive.ubuntu.com/ubuntu noble-updates/main amd64 libsystemd0 amd64 255.4-1ubuntu8.6 [433 kB]
Get:5 http://nova.clouds.archive.ubuntu.com/ubuntu noble-updates/main amd64 systemd-sysv amd64 255.4-1ubuntu8.6 [11.9 kB]
Get:6 http://nova.clouds.archive.ubuntu.com/ubuntu noble-updates/main amd64 libnss-systemd amd64 255.4-1ubuntu8.6 [159 kB]
Get:7 http://nova.clouds.archive.ubuntu.com/ubuntu noble-updates/main amd64 libpam-systemd amd64 255.4-1ubuntu8.6 [235 kB]
Get:8 http://nova.clouds.archive.ubuntu.com/ubuntu noble-updates/main amd64 systemd amd64 255.4-1ubuntu8.6 [3471 kB]
Get:9 http://nova.clouds.archive.ubuntu.com/ubuntu noble-updates/main amd64 udev amd64 255.4-1ubuntu8.6 [1873 kB]
Get:10 http://nova.clouds.archive.ubuntu.com/ubuntu noble-updates/main amd64 libudev1 amd64 255.4-1ubuntu8.6 [175 kB]
Get:11 http://nova.clouds.archive.ubuntu.com/ubuntu noble/main amd64 libjsoncpp25 amd64 1.9.5-6build1 [82.8 kB]
Get:12 http://nova.clouds.archive.ubuntu.com/ubuntu noble/main amd64 librhash0 amd64 1.4.3-3build1 [129 kB]
Get:13 http://nova.clouds.archive.ubuntu.com/ubuntu noble/main amd64 cmake-data all 3.28.3-1build7 [2155 kB]
Get:14 http://nova.clouds.archive.ubuntu.com/ubuntu noble/main amd64 cmake amd64 3.28.3-1build7 [11.2 MB]
Get:15 http://nova.clouds.archive.ubuntu.com/ubuntu noble/universe amd64 googletest all 1.14.0-1 [521 kB]
Get:16 http://nova.clouds.archive.ubuntu.com/ubuntu noble-updates/main amd64 libdrm-amdgpu1 amd64 2.4.122-1~ubuntu0.24.04.1 [20.7 kB]
Get:17 http://nova.clouds.archive.ubuntu.com/ubuntu noble/main amd64 libpciaccess0 amd64 0.17-3build1 [18.6 kB]
Get:18 http://nova.clouds.archive.ubuntu.com/ubuntu noble-updates/main amd64 libdrm-intel1 amd64 2.4.122-1~ubuntu0.24.04.1 [63.8 kB]
Get:19 http://nova.clouds.archive.ubuntu.com/ubuntu noble-updates/main amd64 libdrm-radeon1 amd64 2.4.122-1~ubuntu0.24.04.1 [20.8 kB]
Get:20 http://nova.clouds.archive.ubuntu.com/ubuntu noble-updates/main amd64 libdrm-nouveau2 amd64 2.4.122-1~ubuntu0.24.04.1 [17.7 kB]
Get:21 http://nova.clouds.archive.ubuntu.com/ubuntu noble/main amd64 libpciaccess-dev amd64 0.17-3build1 [22.0 kB]
Get:22 http://nova.clouds.archive.ubuntu.com/ubuntu noble-updates/main amd64 libdrm-dev amd64 2.4.122-1~ubuntu0.24.04.1 [310 kB]
Get:23 http://nova.clouds.archive.ubuntu.com/ubuntu noble/universe amd64 libgtest-dev amd64 1.14.0-1 [268 kB]
Get:24 http://nova.clouds.archive.ubuntu.com/ubuntu noble/main amd64 libncurses-dev amd64 6.4+20240113-1ubuntu2 [384 kB]
Get:25 http://nova.clouds.archive.ubuntu.com/ubuntu noble-updates/main amd64 libsystemd-dev amd64 255.4-1ubuntu8.6 [1238 kB]
Get:26 http://nova.clouds.archive.ubuntu.com/ubuntu noble-updates/main amd64 libudev-dev amd64 255.4-1ubuntu8.6 [22.0 kB]


debconf: unable to initialize frontend: Dialog
debconf: (Dialog frontend will not work on a dumb terminal, an emacs shell buffer, or without a controlling terminal.)
debconf: falling back to frontend: Readline
debconf: unable to initialize frontend: Readline
debconf: (This frontend requires a controlling tty.)
debconf: falling back to frontend: Teletype
dpkg-preconfigure: unable to re-open stdin: 


Fetched 25.3 MB in 2s (12.0 MB/s)
(Reading database ... 97717 files and directories currently installed.)
Preparing to unpack .../systemd-dev_255.4-1ubuntu8.6_all.deb ...
Unpacking systemd-dev (255.4-1ubuntu8.6) over (255.4-1ubuntu8.5) ...
Preparing to unpack .../systemd-resolved_255.4-1ubuntu8.6_amd64.deb ...
Unpacking systemd-resolved (255.4-1ubuntu8.6) over (255.4-1ubuntu8.5) ...
Preparing to unpack .../libsystemd-shared_255.4-1ubuntu8.6_amd64.deb ...
Unpacking libsystemd-shared:amd64 (255.4-1ubuntu8.6) over (255.4-1ubuntu8.5) ...
Preparing to unpack .../libsystemd0_255.4-1ubuntu8.6_amd64.deb ...
Unpacking libsystemd0:amd64 (255.4-1ubuntu8.6) over (255.4-1ubuntu8.5) ...
Setting up libsystemd0:amd64 (255.4-1ubuntu8.6) ...
(Reading database ... 97717 files and directories currently installed.)
Preparing to unpack .../0-systemd-sysv_255.4-1ubuntu8.6_amd64.deb ...
Unpacking systemd-sysv (255.4-1ubuntu8.6) over (255.4-1ubuntu8.5) ...
Preparing to unpack .../1-libnss-systemd_255.4-1ubuntu8.6_amd64.deb ...
Unpacking libnss-systemd:amd64 (255.4-1ubuntu8.6) over (255.4-1ubuntu8.5) ...
Preparing to unpack .../2-libpam-systemd_255.4-1ubuntu8.6_amd64.deb ...
Unpacking libpam-systemd:amd64 (255.4-1ubuntu8.6) over (255.4-1ubuntu8.5) ...
Preparing to unpack .../3-systemd_255.4-1ubuntu8.6_amd64.deb ...
Unpacking systemd (255.4-1ubuntu8.6) over (255.4-1ubuntu8.5) ...
Preparing to unpack .../4-udev_255.4-1ubuntu8.6_amd64.deb ...
Unpacking udev (255.4-1ubuntu8.6) over (255.4-1ubuntu8.5) ...
Preparing to unpack .../5-libudev1_255.4-1ubuntu8.6_amd64.deb ...
Unpacking libudev1:amd64 (255.4-1ubuntu8.6) over (255.4-1ubuntu8.5) ...
Setting up libudev1:amd64 (255.4-1ubuntu8.6) ...
Selecting previously unselected package libjsoncpp25:amd64.
(Reading database ... 97717 files and directories currently installed.)
Preparing to unpack .../00-libjsoncpp25_1.9.5-6build1_amd64.deb ...
Unpacking libjsoncpp25:amd64 (1.9.5-6build1) ...
Selecting previously unselected package librhash0:amd64.
Preparing to unpack .../01-librhash0_1.4.3-3build1_amd64.deb ...
Unpacking librhash0:amd64 (1.4.3-3build1) ...
Selecting previously unselected package cmake-data.
Preparing to unpack .../02-cmake-data_3.28.3-1build7_all.deb ...
Unpacking cmake-data (3.28.3-1build7) ...
Selecting previously unselected package cmake.
Preparing to unpack .../03-cmake_3.28.3-1build7_amd64.deb ...
Unpacking cmake (3.28.3-1build7) ...
Selecting previously unselected package googletest.
Preparing to unpack .../04-googletest_1.14.0-1_all.deb ...
Unpacking googletest (1.14.0-1) ...
Selecting previously unselected package libdrm-amdgpu1:amd64.
Preparing to unpack .../05-libdrm-amdgpu1_2.4.122-1~ubuntu0.24.04.1_amd64.deb ...
Unpacking libdrm-amdgpu1:amd64 (2.4.122-1~ubuntu0.24.04.1) ...
Selecting previously unselected package libpciaccess0:amd64.
Preparing to unpack .../06-libpciaccess0_0.17-3build1_amd64.deb ...
Unpacking libpciaccess0:amd64 (0.17-3build1) ...
Selecting previously unselected package libdrm-intel1:amd64.
Preparing to unpack .../07-libdrm-intel1_2.4.122-1~ubuntu0.24.04.1_amd64.deb ...
Unpacking libdrm-intel1:amd64 (2.4.122-1~ubuntu0.24.04.1) ...
Selecting previously unselected package libdrm-radeon1:amd64.
Preparing to unpack .../08-libdrm-radeon1_2.4.122-1~ubuntu0.24.04.1_amd64.deb ...
Unpacking libdrm-radeon1:amd64 (2.4.122-1~ubuntu0.24.04.1) ...
Selecting previously unselected package libdrm-nouveau2:amd64.
Preparing to unpack .../09-libdrm-nouveau2_2.4.122-1~ubuntu0.24.04.1_amd64.deb ...
Unpacking libdrm-nouveau2:amd64 (2.4.122-1~ubuntu0.24.04.1) ...
Selecting previously unselected package libpciaccess-dev:amd64.
Preparing to unpack .../10-libpciaccess-dev_0.17-3build1_amd64.deb ...
Unpacking libpciaccess-dev:amd64 (0.17-3build1) ...
Selecting previously unselected package libdrm-dev:amd64.
Preparing to unpack .../11-libdrm-dev_2.4.122-1~ubuntu0.24.04.1_amd64.deb ...
Unpacking libdrm-dev:amd64 (2.4.122-1~ubuntu0.24.04.1) ...
Selecting previously unselected package libgtest-dev:amd64.
Preparing to unpack .../12-libgtest-dev_1.14.0-1_amd64.deb ...
Unpacking libgtest-dev:amd64 (1.14.0-1) ...
Selecting previously unselected package libncurses-dev:amd64.
Preparing to unpack .../13-libncurses-dev_6.4+20240113-1ubuntu2_amd64.deb ...
Unpacking libncurses-dev:amd64 (6.4+20240113-1ubuntu2) ...
Selecting previously unselected package libsystemd-dev:amd64.
Preparing to unpack .../14-libsystemd-dev_255.4-1ubuntu8.6_amd64.deb ...
Unpacking libsystemd-dev:amd64 (255.4-1ubuntu8.6) ...
Selecting previously unselected package libudev-dev:amd64.
Preparing to unpack .../15-libudev-dev_255.4-1ubuntu8.6_amd64.deb ...
Unpacking libudev-dev:amd64 (255.4-1ubuntu8.6) ...
Setting up libpciaccess0:amd64 (0.17-3build1) ...
Setting up libncurses-dev:amd64 (6.4+20240113-1ubuntu2) ...
Setting up libdrm-nouveau2:amd64 (2.4.122-1~ubuntu0.24.04.1) ...
Setting up libpciaccess-dev:amd64 (0.17-3build1) ...
Setting up libdrm-radeon1:amd64 (2.4.122-1~ubuntu0.24.04.1) ...
Setting up libdrm-intel1:amd64 (2.4.122-1~ubuntu0.24.04.1) ...
Setting up systemd-dev (255.4-1ubuntu8.6) ...
Setting up googletest (1.14.0-1) ...
Setting up libsystemd-shared:amd64 (255.4-1ubuntu8.6) ...
Setting up libjsoncpp25:amd64 (1.9.5-6build1) ...
Setting up libudev-dev:amd64 (255.4-1ubuntu8.6) ...
Setting up librhash0:amd64 (1.4.3-3build1) ...
Setting up cmake-data (3.28.3-1build7) ...
Setting up libsystemd-dev:amd64 (255.4-1ubuntu8.6) ...
Setting up libdrm-amdgpu1:amd64 (2.4.122-1~ubuntu0.24.04.1) ...
Setting up libdrm-dev:amd64 (2.4.122-1~ubuntu0.24.04.1) ...
Setting up libgtest-dev:amd64 (1.14.0-1) ...
Setting up systemd (255.4-1ubuntu8.6) ...
Setting up udev (255.4-1ubuntu8.6) ...
Setting up cmake (3.28.3-1build7) ...
Setting up systemd-resolved (255.4-1ubuntu8.6) ...
Setting up systemd-sysv (255.4-1ubuntu8.6) ...
Setting up libnss-systemd:amd64 (255.4-1ubuntu8.6) ...
Setting up libpam-systemd:amd64 (255.4-1ubuntu8.6) ...
debconf: unable to initialize frontend: Dialog
debconf: (Dialog frontend will not work on a dumb terminal, an emacs shell buffer, or without a controlling terminal.)
debconf: falling back to frontend: Readline
debconf: unable to initialize frontend: Readline
debconf: (This frontend requires a controlling tty.)
debconf: falling back to frontend: Teletype
Processing triggers for libc-bin (2.39-0ubuntu8.4) ...
Processing triggers for man-db (2.12.0-4build2) ...
Processing triggers for dbus (1.14.10-4ubuntu4.1) ...
Processing triggers for initramfs-tools (0.142ubuntu25.4) ...
update-initramfs: Generating /boot/initrd.img-6.11.0-17-generic


debconf: unable to initialize frontend: Dialog
debconf: (Dialog frontend will not work on a dumb terminal, an emacs shell buffer, or without a controlling terminal.)
debconf: falling back to frontend: Readline
debconf: unable to initialize frontend: Readline
debconf: (This frontend requires a controlling tty.)
debconf: falling back to frontend: Teletype

Running kernel seems to be up-to-date.

The processor microcode seems to be up-to-date.

Restarting services...
 systemctl restart firewalld.service multipathd.service polkit.service rpcbind.service rsyslog.service ssh.service systemd-hostnamed.service udisks2.service

Service restarts being deferred:
 systemctl restart ModemManager.service
 /etc/needrestart/restart.d/dbus.service
 systemctl restart docker.service
 systemctl restart networkd-dispatcher.service
 systemctl restart systemd-logind.service
 systemctl restart unattended-upgrades.service

No containers need to be restarted.

User sessions running outdated binaries:
 cc @ session #1: login[3954]
 cc @ session #2: login[4005]
 cc @ session #5: apt[4493], sshd[4470]
 cc @ user manager service: systemd[4399]

No VM guests are running outdated hypervisor (qemu) binaries on this host.
Cloning into 'nvtop'...


-- The C compiler identification is GNU 13.3.0
-- The CXX compiler identification is GNU 13.3.0
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working C compiler: /usr/bin/cc - skipped
-- Detecting C compile features
-- Detecting C compile features - done
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: /usr/bin/c++ - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Setting build type to 'Release' as none was specified.
-- Looking for cbreak in /usr/lib/x86_64-linux-gnu/libncursesw.so
-- Looking for cbreak in /usr/lib/x86_64-linux-gnu/libncursesw.so - found
-- Found Curses: /usr/lib/x86_64-linux-gnu/libncursesw.so  
-- Performing Test HAS_REALLOCARRAY
-- Performing Test HAS_REALLOCARRAY - Success
-- Found UDev: /usr/lib/x86_64-linux-gnu/libudev.so (found version "") 
-- Libudev stable: FALSE
-- Found Systemd: /usr/lib/x86_64-linux-gnu/libsystemd.so (found version "") 
-- Could NOT find PkgConfig (missing: PKG_CONFIG_EXECUTABLE) 
-- Found Libdrm: /usr/lib/x86_64-linux-gnu/libdrm.so  
-- Found libdrm; Enabling support
-- Performing Test compiler_has-Wall
-- Performing Test compiler_has-Wall - Success
-- Performing Test compiler_has-Wextra
-- Performing Test compiler_has-Wextra - Success
-- Performing Test compiler_has-Waddress
-- Performing Test compiler_has-Waddress - Success
-- Performing Test compiler_has-Waggressive-loop-optimizations
-- Performing Test compiler_has-Waggressive-loop-optimizations - Success
-- Performing Test compiler_has-Wbad-function-cast
-- Performing Test compiler_has-Wbad-function-cast - Success
-- Performing Test compiler_has-Wmissing-declarations
-- Performing Test compiler_has-Wmissing-declarations - Success
-- Performing Test compiler_has-Wmissing-parameter-type
-- Performing Test compiler_has-Wmissing-parameter-type - Success
-- Performing Test compiler_has-Wmissing-prototypes
-- Performing Test compiler_has-Wmissing-prototypes - Success
-- Performing Test compiler_has-Wnested-externs
-- Performing Test compiler_has-Wnested-externs - Success
-- Performing Test compiler_has-Wold-style-declaration
-- Performing Test compiler_has-Wold-style-declaration - Success
-- Performing Test compiler_has-Wold-style-definition
-- Performing Test compiler_has-Wold-style-definition - Success
-- Performing Test compiler_has-Wstrict-prototypes
-- Performing Test compiler_has-Wstrict-prototypes - Success
-- Performing Test compiler_has-Wpointer-sign
-- Performing Test compiler_has-Wpointer-sign - Success
-- Performing Test compiler_has-Wdouble-promotion
-- Performing Test compiler_has-Wdouble-promotion - Success
-- Performing Test compiler_has-Wuninitialized
-- Performing Test compiler_has-Wuninitialized - Success
-- Performing Test compiler_has-Winit-self
-- Performing Test compiler_has-Winit-self - Success
-- Performing Test compiler_has-Wstrict-aliasing
-- Performing Test compiler_has-Wstrict-aliasing - Success
-- Performing Test compiler_has-Wsuggest-attribute-const
-- Performing Test compiler_has-Wsuggest-attribute-const - Success
-- Performing Test compiler_has-Wtrampolines
-- Performing Test compiler_has-Wtrampolines - Success
-- Performing Test compiler_has-Wfloat-equal
-- Performing Test compiler_has-Wfloat-equal - Success
-- Performing Test compiler_has-Wshadow
-- Performing Test compiler_has-Wshadow - Success
-- Performing Test compiler_has-Wunsafe-loop-optimizations
-- Performing Test compiler_has-Wunsafe-loop-optimizations - Success
-- Performing Test compiler_has-Wfloat-conversion
-- Performing Test compiler_has-Wfloat-conversion - Success
-- Performing Test compiler_has-Wlogical-op
-- Performing Test compiler_has-Wlogical-op - Success
-- Performing Test compiler_has-Wnormalized
-- Performing Test compiler_has-Wnormalized - Success
-- Performing Test compiler_has-Wdisabled-optimization
-- Performing Test compiler_has-Wdisabled-optimization - Success
-- Performing Test compiler_has-Whsa
-- Performing Test compiler_has-Whsa - Success
-- Performing Test compiler_has-Wunused-result
-- Performing Test compiler_has-Wunused-result - Success
-- Performing Test compiler_has-Werror-implicit-function-declaration
-- Performing Test compiler_has-Werror-implicit-function-declaration - Success
-- Performing Test compiler_has-Wformat
-- Performing Test compiler_has-Wformat - Success
-- Performing Test compiler_has-Wformat-security
-- Performing Test compiler_has-Wformat-security - Success
-- Performing Test linker_has-Wl_-z_relro
-- Performing Test linker_has-Wl_-z_relro - Success
-- Found GTest: /usr/lib/x86_64-linux-gnu/cmake/GTest/GTestConfig.cmake (found version "1.14.0")  
-- Configuring done (3.7s)
-- Generating done (0.0s)
-- Build files have been written to: /home/cc/nvtop/build
[  3%] Building C object src/CMakeFiles/nvtop.dir/nvtop.c.o
[  6%] Building C object src/CMakeFiles/nvtop.dir/interface.c.o
[ 10%] Building C object src/CMakeFiles/nvtop.dir/interface_layout_selection.c.o
[ 13%] Building C object src/CMakeFiles/nvtop.dir/interface_options.c.o
[ 16%] Building C object src/CMakeFiles/nvtop.dir/interface_setup_win.c.o
[ 20%] Building C object src/CMakeFiles/nvtop.dir/interface_ring_buffer.c.o
[ 23%] Building C object src/CMakeFiles/nvtop.dir/extract_gpuinfo.c.o
[ 26%] Building C object src/CMakeFiles/nvtop.dir/time.c.o
[ 30%] Building C object src/CMakeFiles/nvtop.dir/plot.c.o
[ 33%] Building C object src/CMakeFiles/nvtop.dir/ini.c.o
[ 36%] Building C object src/CMakeFiles/nvtop.dir/get_process_info_linux.c.o
[ 40%] Building C object src/CMakeFiles/nvtop.dir/extract_processinfo_fdinfo.c.o
[ 43%] Building C object src/CMakeFiles/nvtop.dir/info_messages_linux.c.o
[ 46%] Building C object src/CMakeFiles/nvtop.dir/extract_gpuinfo_nvidia.c.o
[ 50%] Building C object src/CMakeFiles/nvtop.dir/device_discovery_linux.c.o
[ 53%] Building C object src/CMakeFiles/nvtop.dir/extract_gpuinfo_amdgpu.c.o
[ 56%] Building C object src/CMakeFiles/nvtop.dir/extract_gpuinfo_amdgpu_utils.c.o
[ 60%] Building C object src/CMakeFiles/nvtop.dir/extract_gpuinfo_msm.c.o
[ 63%] Building C object src/CMakeFiles/nvtop.dir/extract_gpuinfo_msm_utils.c.o
[ 66%] Building C object src/CMakeFiles/nvtop.dir/extract_gpuinfo_intel.c.o
[ 70%] Building C object src/CMakeFiles/nvtop.dir/extract_gpuinfo_intel_i915.c.o
[ 73%] Building C object src/CMakeFiles/nvtop.dir/extract_gpuinfo_intel_xe.c.o
[ 76%] Building C object src/CMakeFiles/nvtop.dir/extract_gpuinfo_v3d.c.o
[ 80%] Building C object src/CMakeFiles/nvtop.dir/extract_gpuinfo_v3d_utils.c.o
[ 83%] Building C object src/CMakeFiles/nvtop.dir/extract_gpuinfo_panfrost.c.o
[ 86%] Building C object src/CMakeFiles/nvtop.dir/extract_gpuinfo_panfrost_utils.c.o
[ 90%] Building C object src/CMakeFiles/nvtop.dir/extract_gpuinfo_panthor.c.o
[ 93%] Building C object src/CMakeFiles/nvtop.dir/extract_gpuinfo_panthor_utils.c.o
[ 96%] Building C object src/CMakeFiles/nvtop.dir/extract_gpuinfo_mali_common.c.o
[100%] Linking C executable nvtop
[100%] Built target nvtop
Install the project...
-- Install configuration: "Release"
-- Installing: /usr/local/bin/nvtop
-- Set non-toolchain portion of runtime path of "/usr/local/bin/nvtop" to "/usr/local/lib"
-- Installing: /usr/local/share/man/man1/nvtop.1
-- Installing: /usr/local/share/icons/hicolor/scalable/apps/nvtop.svg
-- Installing: /usr/local/share/applications/nvtop.desktop
-- Installing: /usr/local/share/metainfo/io.github.syllo.nvtop.metainfo.xml





<Result cmd='mkdir -p nvtop/build && cd nvtop/build && cmake .. -DAMDGPU_SUPPORT=ON && sudo make install' exited=0>
```

</div>

### Build a container image - for MLFlow section

Finally, build a container image in which to work in the MLFlow section, that has:

- a Jupyter notebook server
- Pytorch and Pytorch Lightning
- ROCm, which allows deep learning frameworks like Pytorch to use the AMD GPU accelerator
- and MLFlow

The Dockerfile for this image is at: [Dockerfile.jupyter-torch-mlflow-rocm](https://github.com/M0n4GPT/vision-to-vintage/blob/master/style_transfer/docker/Dockerfile.jupyter-torch-mlflow-rocm)

Building this container will take a **very long** time (ROCm is huge).

```python
s.execute("docker build -t jupyter-mlflow -f style_transfer/docker/Dockerfile.jupyter-torch-mlflow-rocm .")
```

<div style="max-height:300px; overflow:auto; background:#f9f9f9; line-height: 1.2; boder:1px solid #ccc; padding:0px; font-family:monospace;font-size: 9px; white-space:pre;">

```
#0 building with "default" instance using docker driver

#1 [internal] load build definition from Dockerfile.jupyter-torch-mlflow-rocm
#1 transferring dockerfile: 1.16kB done
#1 DONE 0.0s

#2 [internal] load metadata for quay.io/jupyter/scipy-notebook:latest
#2 DONE 0.8s

#3 [internal] load .dockerignore
#3 transferring context: 2B done
#3 DONE 0.0s

#4 [1/5] FROM quay.io/jupyter/scipy-notebook:latest@sha256:38b74c0b58d1e004bb979f5a221f5730578f9aca7f6878c1689f4a193c4793cc
#4 resolve quay.io/jupyter/scipy-notebook:latest@sha256:38b74c0b58d1e004bb979f5a221f5730578f9aca7f6878c1689f4a193c4793cc done
#4 sha256:38b74c0b58d1e004bb979f5a221f5730578f9aca7f6878c1689f4a193c4793cc 743B / 743B done
#4 sha256:33fe43ff4ffc27673f783d85a90aa649ec18870589bbce3ded03d5ca65e62351 18.52kB / 18.52kB done
#4 sha256:ac0c285abb482df6684de5a61b4577fc5cc5fafe8cd1280ebf52d8909d121599 4.19MB / 30.59MB 0.3s
#4 sha256:0cec0952d04b35f63c37822bc4a9d3a83ae200dd5331aba8ef73c7e266ae1559 6.99kB / 6.99kB done
#4 sha256:495e9b1f57cf2c6d6d8e97a2b579177065820753648fd7c66c9800bebd1d617f 0B / 687B 0.2s
#4 sha256:96c932f29ab238a89357a1ed3185a558d6195bed23a42e3f7c8eec419dfec130 0B / 11.43MB 0.3s
#4 sha256:ac0c285abb482df6684de5a61b4577fc5cc5fafe8cd1280ebf52d8909d121599 12.59MB / 30.59MB 0.4s
#4 sha256:96c932f29ab238a89357a1ed3185a558d6195bed23a42e3f7c8eec419dfec130 8.39MB / 11.43MB 0.4s
#4 sha256:ac0c285abb482df6684de5a61b4577fc5cc5fafe8cd1280ebf52d8909d121599 15.73MB / 30.59MB 0.5s
#4 sha256:96c932f29ab238a89357a1ed3185a558d6195bed23a42e3f7c8eec419dfec130 11.43MB / 11.43MB 0.4s done
#4 sha256:4f4fb700ef54461cfa02571ae0db9a0dc1e0cdb5577484a6d75e68dc38e8acc1 0B / 32B 0.6s
#4 sha256:ac0c285abb482df6684de5a61b4577fc5cc5fafe8cd1280ebf52d8909d121599 29.36MB / 30.59MB 0.7s
#4 sha256:4f4fb700ef54461cfa02571ae0db9a0dc1e0cdb5577484a6d75e68dc38e8acc1 32B / 32B 0.7s done
#4 sha256:fc343ee71338677d48439d05e9265f06bc4b409394a57c9ffd5933cf18255f8e 0B / 1.91kB 0.8s
#4 sha256:ac0c285abb482df6684de5a61b4577fc5cc5fafe8cd1280ebf52d8909d121599 30.59MB / 30.59MB 0.8s done
#4 extracting sha256:ac0c285abb482df6684de5a61b4577fc5cc5fafe8cd1280ebf52d8909d121599
#4 sha256:64e5e0365c94a627970f434d61707b28f09883a6d96b20b11045327b198b058e 0B / 1.30kB 0.9s
#4 sha256:a4e265e924b90950a9956a87468511dbda3b5b1d9ae0ff6370d836bc0eacc639 0B / 4.95kB 0.9s
#4 sha256:495e9b1f57cf2c6d6d8e97a2b579177065820753648fd7c66c9800bebd1d617f 687B / 687B 0.8s done
#4 sha256:e2c2fd07bff9b5e62262d6231b3abb856133a44f45c3806e9d9752134cf63703 0B / 150B 1.0s
#4 sha256:fc343ee71338677d48439d05e9265f06bc4b409394a57c9ffd5933cf18255f8e 1.91kB / 1.91kB 1.0s done
#4 sha256:a4e265e924b90950a9956a87468511dbda3b5b1d9ae0ff6370d836bc0eacc639 4.95kB / 4.95kB 1.0s done
#4 sha256:e2c2fd07bff9b5e62262d6231b3abb856133a44f45c3806e9d9752134cf63703 150B / 150B 1.1s done
#4 sha256:0c4f60182985297bf3f375af289387227dcd1129c7b869169c866061d1295331 0B / 276B 1.1s
#4 sha256:a63b9b1262fd109c8b07b98c065c461c4b49684d004f61fe9f5527b389641655 0B / 93.62MB 1.1s
#4 sha256:0c4f60182985297bf3f375af289387227dcd1129c7b869169c866061d1295331 276B / 276B 1.2s done
#4 sha256:48ce0bc44f140feaaaa1f12bec743b6b1c82db711bec4e87e8fdce827662ef08 0B / 4.69kB 1.2s
#4 sha256:a63b9b1262fd109c8b07b98c065c461c4b49684d004f61fe9f5527b389641655 12.58MB / 93.62MB 1.3s
#4 sha256:64e5e0365c94a627970f434d61707b28f09883a6d96b20b11045327b198b058e 1.30kB / 1.30kB 1.3s done
#4 sha256:a63b9b1262fd109c8b07b98c065c461c4b49684d004f61fe9f5527b389641655 35.24MB / 93.62MB 1.4s
#4 sha256:02f4d656889f2dbed3d743adfde6c76292d67044c2246c3cbfb2907057b19d20 0B / 182B 1.4s
#4 sha256:a63b9b1262fd109c8b07b98c065c461c4b49684d004f61fe9f5527b389641655 57.04MB / 93.62MB 1.5s
#4 sha256:02f4d656889f2dbed3d743adfde6c76292d67044c2246c3cbfb2907057b19d20 182B / 182B 1.5s done
#4 sha256:87e622d6d8d55a86300ced6f377975763570aef1ac0928c6524e219def035e5f 0B / 478B 1.5s
#4 sha256:a63b9b1262fd109c8b07b98c065c461c4b49684d004f61fe9f5527b389641655 80.74MB / 93.62MB 1.6s
#4 sha256:48ce0bc44f140feaaaa1f12bec743b6b1c82db711bec4e87e8fdce827662ef08 4.69kB / 4.69kB 1.6s done
#4 sha256:b7900f8fafa1225b8fd8408b50edcf7757a7f07f76bd464225b6b6189ea848de 0B / 41.18MB 1.6s
#4 sha256:a63b9b1262fd109c8b07b98c065c461c4b49684d004f61fe9f5527b389641655 93.62MB / 93.62MB 1.7s
#4 sha256:87e622d6d8d55a86300ced6f377975763570aef1ac0928c6524e219def035e5f 478B / 478B 1.6s done
#4 sha256:274f1c4884281f93b4442023e134b67fcf3bcea500a426d4b68c7f3b813c6e4b 0B / 97.52MB 1.7s
#4 sha256:a63b9b1262fd109c8b07b98c065c461c4b49684d004f61fe9f5527b389641655 93.62MB / 93.62MB 1.9s done
#4 sha256:b7900f8fafa1225b8fd8408b50edcf7757a7f07f76bd464225b6b6189ea848de 20.97MB / 41.18MB 1.8s
#4 sha256:cd0bdba38181c5c59ee6745978fec0ea7ae78ed70e89075bbc1c6fc25f4488ce 0B / 1.17kB 1.9s
#4 sha256:b7900f8fafa1225b8fd8408b50edcf7757a7f07f76bd464225b6b6189ea848de 41.18MB / 41.18MB 2.0s
#4 sha256:274f1c4884281f93b4442023e134b67fcf3bcea500a426d4b68c7f3b813c6e4b 12.58MB / 97.52MB 2.0s
#4 sha256:b7900f8fafa1225b8fd8408b50edcf7757a7f07f76bd464225b6b6189ea848de 41.18MB / 41.18MB 2.0s done
#4 sha256:274f1c4884281f93b4442023e134b67fcf3bcea500a426d4b68c7f3b813c6e4b 33.77MB / 97.52MB 2.1s
#4 sha256:cd0bdba38181c5c59ee6745978fec0ea7ae78ed70e89075bbc1c6fc25f4488ce 1.17kB / 1.17kB 2.0s done
#4 sha256:42d093ca080778bcd543d6c28c5d6ba84ab9828cc27c3afbbec36d606ce2be1d 0B / 1.69kB 2.1s
#4 sha256:1389a59ee1103041d8ba9ef1eba0693f205803ef609b288407aa48d6ca0e1ba6 0B / 1.68kB 2.1s
#4 sha256:274f1c4884281f93b4442023e134b67fcf3bcea500a426d4b68c7f3b813c6e4b 55.86MB / 97.52MB 2.2s
#4 sha256:42d093ca080778bcd543d6c28c5d6ba84ab9828cc27c3afbbec36d606ce2be1d 1.69kB / 1.69kB 2.2s
#4 sha256:274f1c4884281f93b4442023e134b67fcf3bcea500a426d4b68c7f3b813c6e4b 76.55MB / 97.52MB 2.3s
#4 sha256:42d093ca080778bcd543d6c28c5d6ba84ab9828cc27c3afbbec36d606ce2be1d 1.69kB / 1.69kB 2.2s done
#4 sha256:1389a59ee1103041d8ba9ef1eba0693f205803ef609b288407aa48d6ca0e1ba6 1.68kB / 1.68kB 2.2s done
#4 sha256:fcc5e6a41fda939c85db54112a0dd554c1d4ad04ee5ddd35c01b0ba229cecce9 0B / 1.38kB 2.3s
#4 sha256:96e0030bb2d295bb1b5cafd150606852d99f1ff92b307f0d46e9bd913a3d78e8 0B / 243.89MB 2.3s
#4 sha256:274f1c4884281f93b4442023e134b67fcf3bcea500a426d4b68c7f3b813c6e4b 97.52MB / 97.52MB 2.5s
#4 sha256:fcc5e6a41fda939c85db54112a0dd554c1d4ad04ee5ddd35c01b0ba229cecce9 1.38kB / 1.38kB 2.4s done
#4 sha256:ed621a90b0fc0b0de0fb6da8a971e9a75b42f200fa6bac6246c1b21d2eafbac3 0B / 433B 2.5s
#4 sha256:274f1c4884281f93b4442023e134b67fcf3bcea500a426d4b68c7f3b813c6e4b 97.52MB / 97.52MB 2.7s done
#4 sha256:96e0030bb2d295bb1b5cafd150606852d99f1ff92b307f0d46e9bd913a3d78e8 22.02MB / 243.89MB 2.7s
#4 sha256:ed621a90b0fc0b0de0fb6da8a971e9a75b42f200fa6bac6246c1b21d2eafbac3 433B / 433B 2.7s done
#4 sha256:56b77bbcf0531e8cd9e5a631dc47cc74f0809b4d583d36c3bccb8e2f1ed761f5 0B / 2.81kB 2.7s
#4 sha256:a3c27f64127b606ad37cac8467a931cabe3ae3aec42bcab37bfdb099030fdf7f 0B / 313.77MB 2.7s
#4 sha256:96e0030bb2d295bb1b5cafd150606852d99f1ff92b307f0d46e9bd913a3d78e8 34.60MB / 243.89MB 2.9s
#4 sha256:56b77bbcf0531e8cd9e5a631dc47cc74f0809b4d583d36c3bccb8e2f1ed761f5 2.81kB / 2.81kB 2.9s done
#4 sha256:a3c27f64127b606ad37cac8467a931cabe3ae3aec42bcab37bfdb099030fdf7f 17.16MB / 313.77MB 2.9s
#4 sha256:dbe0a72ef98aac36a26f9ac382a8738611e684604bf4a440a03e23994ee359ec 0B / 397.15MB 2.9s
#4 sha256:a3c27f64127b606ad37cac8467a931cabe3ae3aec42bcab37bfdb099030fdf7f 56.62MB / 313.77MB 3.1s
#4 sha256:a3c27f64127b606ad37cac8467a931cabe3ae3aec42bcab37bfdb099030fdf7f 78.64MB / 313.77MB 3.2s
#4 sha256:dbe0a72ef98aac36a26f9ac382a8738611e684604bf4a440a03e23994ee359ec 32.51MB / 397.15MB 3.2s
#4 extracting sha256:ac0c285abb482df6684de5a61b4577fc5cc5fafe8cd1280ebf52d8909d121599 2.4s done
#4 sha256:96e0030bb2d295bb1b5cafd150606852d99f1ff92b307f0d46e9bd913a3d78e8 51.38MB / 243.89MB 3.3s
#4 sha256:a3c27f64127b606ad37cac8467a931cabe3ae3aec42bcab37bfdb099030fdf7f 102.76MB / 313.77MB 3.3s
#4 sha256:dbe0a72ef98aac36a26f9ac382a8738611e684604bf4a440a03e23994ee359ec 56.28MB / 397.15MB 3.3s
#4 extracting sha256:96c932f29ab238a89357a1ed3185a558d6195bed23a42e3f7c8eec419dfec130
#4 sha256:a3c27f64127b606ad37cac8467a931cabe3ae3aec42bcab37bfdb099030fdf7f 125.83MB / 313.77MB 3.4s
#4 sha256:dbe0a72ef98aac36a26f9ac382a8738611e684604bf4a440a03e23994ee359ec 82.84MB / 397.15MB 3.4s
#4 sha256:96e0030bb2d295bb1b5cafd150606852d99f1ff92b307f0d46e9bd913a3d78e8 71.30MB / 243.89MB 3.6s
#4 sha256:a3c27f64127b606ad37cac8467a931cabe3ae3aec42bcab37bfdb099030fdf7f 177.21MB / 313.77MB 3.6s
#4 sha256:dbe0a72ef98aac36a26f9ac382a8738611e684604bf4a440a03e23994ee359ec 134.78MB / 397.15MB 3.6s
#4 sha256:a3c27f64127b606ad37cac8467a931cabe3ae3aec42bcab37bfdb099030fdf7f 200.28MB / 313.77MB 3.7s
#4 sha256:dbe0a72ef98aac36a26f9ac382a8738611e684604bf4a440a03e23994ee359ec 157.29MB / 397.15MB 3.7s
#4 sha256:96e0030bb2d295bb1b5cafd150606852d99f1ff92b307f0d46e9bd913a3d78e8 90.18MB / 243.89MB 3.8s
#4 sha256:a3c27f64127b606ad37cac8467a931cabe3ae3aec42bcab37bfdb099030fdf7f 225.44MB / 313.77MB 3.8s
#4 sha256:dbe0a72ef98aac36a26f9ac382a8738611e684604bf4a440a03e23994ee359ec 180.36MB / 397.15MB 3.8s
#4 sha256:a3c27f64127b606ad37cac8467a931cabe3ae3aec42bcab37bfdb099030fdf7f 242.22MB / 313.77MB 3.9s
#4 sha256:dbe0a72ef98aac36a26f9ac382a8738611e684604bf4a440a03e23994ee359ec 204.47MB / 397.15MB 3.9s
#4 sha256:dbe0a72ef98aac36a26f9ac382a8738611e684604bf4a440a03e23994ee359ec 224.40MB / 397.15MB 4.0s
#4 sha256:a3c27f64127b606ad37cac8467a931cabe3ae3aec42bcab37bfdb099030fdf7f 277.87MB / 313.77MB 4.1s
#4 sha256:dbe0a72ef98aac36a26f9ac382a8738611e684604bf4a440a03e23994ee359ec 246.73MB / 397.15MB 4.1s
#4 sha256:96e0030bb2d295bb1b5cafd150606852d99f1ff92b307f0d46e9bd913a3d78e8 108.00MB / 243.89MB 4.2s
#4 sha256:a3c27f64127b606ad37cac8467a931cabe3ae3aec42bcab37bfdb099030fdf7f 298.84MB / 313.77MB 4.2s
#4 sha256:96e0030bb2d295bb1b5cafd150606852d99f1ff92b307f0d46e9bd913a3d78e8 129.37MB / 243.89MB 4.4s
#4 sha256:dbe0a72ef98aac36a26f9ac382a8738611e684604bf4a440a03e23994ee359ec 309.33MB / 397.15MB 4.4s
#4 sha256:96e0030bb2d295bb1b5cafd150606852d99f1ff92b307f0d46e9bd913a3d78e8 160.43MB / 243.89MB 4.6s
#4 sha256:dbe0a72ef98aac36a26f9ac382a8738611e684604bf4a440a03e23994ee359ec 348.13MB / 397.15MB 4.6s
#4 extracting sha256:96c932f29ab238a89357a1ed3185a558d6195bed23a42e3f7c8eec419dfec130 1.1s done
#4 extracting sha256:495e9b1f57cf2c6d6d8e97a2b579177065820753648fd7c66c9800bebd1d617f
#4 sha256:96e0030bb2d295bb1b5cafd150606852d99f1ff92b307f0d46e9bd913a3d78e8 207.62MB / 243.89MB 4.9s
#4 sha256:dbe0a72ef98aac36a26f9ac382a8738611e684604bf4a440a03e23994ee359ec 397.15MB / 397.15MB 4.9s
#4 extracting sha256:495e9b1f57cf2c6d6d8e97a2b579177065820753648fd7c66c9800bebd1d617f 0.1s done
#4 sha256:96e0030bb2d295bb1b5cafd150606852d99f1ff92b307f0d46e9bd913a3d78e8 237.37MB / 243.89MB 5.1s
#4 extracting sha256:4f4fb700ef54461cfa02571ae0db9a0dc1e0cdb5577484a6d75e68dc38e8acc1
#4 sha256:a3c27f64127b606ad37cac8467a931cabe3ae3aec42bcab37bfdb099030fdf7f 313.77MB / 313.77MB 5.1s done
#4 extracting sha256:4f4fb700ef54461cfa02571ae0db9a0dc1e0cdb5577484a6d75e68dc38e8acc1 0.1s done
#4 sha256:1263bd08ce5ae3aff6732538d318f1b51bd65e6176a39b98300ddef63aa38048 0B / 597.21kB 5.4s
#4 extracting sha256:fc343ee71338677d48439d05e9265f06bc4b409394a57c9ffd5933cf18255f8e
#4 extracting sha256:fc343ee71338677d48439d05e9265f06bc4b409394a57c9ffd5933cf18255f8e 0.1s done
#4 extracting sha256:64e5e0365c94a627970f434d61707b28f09883a6d96b20b11045327b198b058e 0.1s done
#4 extracting sha256:a4e265e924b90950a9956a87468511dbda3b5b1d9ae0ff6370d836bc0eacc639
#4 extracting sha256:a4e265e924b90950a9956a87468511dbda3b5b1d9ae0ff6370d836bc0eacc639 0.1s done
#4 sha256:96e0030bb2d295bb1b5cafd150606852d99f1ff92b307f0d46e9bd913a3d78e8 243.89MB / 243.89MB 6.4s done
#4 sha256:dbe0a72ef98aac36a26f9ac382a8738611e684604bf4a440a03e23994ee359ec 397.15MB / 397.15MB 6.5s done
#4 extracting sha256:e2c2fd07bff9b5e62262d6231b3abb856133a44f45c3806e9d9752134cf63703 0.0s done
#4 extracting sha256:0c4f60182985297bf3f375af289387227dcd1129c7b869169c866061d1295331 done
#4 sha256:4d76720bbbdf6da83f5a4462f53a02c385fa5bd57ae022ff0c3c43768aea3edc 0B / 11.00kB 6.5s
#4 extracting sha256:a63b9b1262fd109c8b07b98c065c461c4b49684d004f61fe9f5527b389641655
#4 sha256:4d76720bbbdf6da83f5a4462f53a02c385fa5bd57ae022ff0c3c43768aea3edc 11.00kB / 11.00kB 6.8s done
#4 sha256:1263bd08ce5ae3aff6732538d318f1b51bd65e6176a39b98300ddef63aa38048 597.21kB / 597.21kB 7.6s done
#4 extracting sha256:a63b9b1262fd109c8b07b98c065c461c4b49684d004f61fe9f5527b389641655 5.0s
#4 extracting sha256:a63b9b1262fd109c8b07b98c065c461c4b49684d004f61fe9f5527b389641655 8.7s done
#4 extracting sha256:48ce0bc44f140feaaaa1f12bec743b6b1c82db711bec4e87e8fdce827662ef08
#4 extracting sha256:48ce0bc44f140feaaaa1f12bec743b6b1c82db711bec4e87e8fdce827662ef08 done
#4 extracting sha256:02f4d656889f2dbed3d743adfde6c76292d67044c2246c3cbfb2907057b19d20 done
#4 extracting sha256:87e622d6d8d55a86300ced6f377975763570aef1ac0928c6524e219def035e5f done
#4 extracting sha256:b7900f8fafa1225b8fd8408b50edcf7757a7f07f76bd464225b6b6189ea848de 0.1s
#4 extracting sha256:b7900f8fafa1225b8fd8408b50edcf7757a7f07f76bd464225b6b6189ea848de 2.8s done
#4 extracting sha256:274f1c4884281f93b4442023e134b67fcf3bcea500a426d4b68c7f3b813c6e4b 0.1s
#4 extracting sha256:274f1c4884281f93b4442023e134b67fcf3bcea500a426d4b68c7f3b813c6e4b 5.2s
#4 extracting sha256:274f1c4884281f93b4442023e134b67fcf3bcea500a426d4b68c7f3b813c6e4b 11.0s
#4 extracting sha256:274f1c4884281f93b4442023e134b67fcf3bcea500a426d4b68c7f3b813c6e4b 16.1s
#4 extracting sha256:274f1c4884281f93b4442023e134b67fcf3bcea500a426d4b68c7f3b813c6e4b 21.4s
#4 extracting sha256:274f1c4884281f93b4442023e134b67fcf3bcea500a426d4b68c7f3b813c6e4b 22.2s done
#4 extracting sha256:cd0bdba38181c5c59ee6745978fec0ea7ae78ed70e89075bbc1c6fc25f4488ce
#4 extracting sha256:cd0bdba38181c5c59ee6745978fec0ea7ae78ed70e89075bbc1c6fc25f4488ce done
#4 extracting sha256:1389a59ee1103041d8ba9ef1eba0693f205803ef609b288407aa48d6ca0e1ba6 done
#4 extracting sha256:42d093ca080778bcd543d6c28c5d6ba84ab9828cc27c3afbbec36d606ce2be1d 0.0s done
#4 extracting sha256:96e0030bb2d295bb1b5cafd150606852d99f1ff92b307f0d46e9bd913a3d78e8
#4 extracting sha256:96e0030bb2d295bb1b5cafd150606852d99f1ff92b307f0d46e9bd913a3d78e8 5.1s
#4 extracting sha256:96e0030bb2d295bb1b5cafd150606852d99f1ff92b307f0d46e9bd913a3d78e8 10.1s
#4 extracting sha256:96e0030bb2d295bb1b5cafd150606852d99f1ff92b307f0d46e9bd913a3d78e8 15.3s
#4 extracting sha256:96e0030bb2d295bb1b5cafd150606852d99f1ff92b307f0d46e9bd913a3d78e8 20.4s
#4 extracting sha256:96e0030bb2d295bb1b5cafd150606852d99f1ff92b307f0d46e9bd913a3d78e8 23.3s done
#4 extracting sha256:fcc5e6a41fda939c85db54112a0dd554c1d4ad04ee5ddd35c01b0ba229cecce9
#4 extracting sha256:fcc5e6a41fda939c85db54112a0dd554c1d4ad04ee5ddd35c01b0ba229cecce9 0.0s done
#4 extracting sha256:ed621a90b0fc0b0de0fb6da8a971e9a75b42f200fa6bac6246c1b21d2eafbac3 done
#4 extracting sha256:56b77bbcf0531e8cd9e5a631dc47cc74f0809b4d583d36c3bccb8e2f1ed761f5 done
#4 extracting sha256:a3c27f64127b606ad37cac8467a931cabe3ae3aec42bcab37bfdb099030fdf7f
#4 extracting sha256:a3c27f64127b606ad37cac8467a931cabe3ae3aec42bcab37bfdb099030fdf7f 5.1s
#4 extracting sha256:a3c27f64127b606ad37cac8467a931cabe3ae3aec42bcab37bfdb099030fdf7f 10.1s
#4 extracting sha256:a3c27f64127b606ad37cac8467a931cabe3ae3aec42bcab37bfdb099030fdf7f 15.2s
#4 extracting sha256:a3c27f64127b606ad37cac8467a931cabe3ae3aec42bcab37bfdb099030fdf7f 16.6s done
#4 extracting sha256:dbe0a72ef98aac36a26f9ac382a8738611e684604bf4a440a03e23994ee359ec
#4 extracting sha256:dbe0a72ef98aac36a26f9ac382a8738611e684604bf4a440a03e23994ee359ec 5.0s
#4 extracting sha256:dbe0a72ef98aac36a26f9ac382a8738611e684604bf4a440a03e23994ee359ec 10.0s
#4 extracting sha256:dbe0a72ef98aac36a26f9ac382a8738611e684604bf4a440a03e23994ee359ec 15.2s
#4 extracting sha256:dbe0a72ef98aac36a26f9ac382a8738611e684604bf4a440a03e23994ee359ec 20.3s
#4 extracting sha256:dbe0a72ef98aac36a26f9ac382a8738611e684604bf4a440a03e23994ee359ec 25.4s
#4 extracting sha256:dbe0a72ef98aac36a26f9ac382a8738611e684604bf4a440a03e23994ee359ec 30.5s
#4 extracting sha256:dbe0a72ef98aac36a26f9ac382a8738611e684604bf4a440a03e23994ee359ec 35.6s
#4 extracting sha256:dbe0a72ef98aac36a26f9ac382a8738611e684604bf4a440a03e23994ee359ec 35.7s done
#4 extracting sha256:1263bd08ce5ae3aff6732538d318f1b51bd65e6176a39b98300ddef63aa38048
#4 extracting sha256:1263bd08ce5ae3aff6732538d318f1b51bd65e6176a39b98300ddef63aa38048 0.0s done
#4 extracting sha256:4d76720bbbdf6da83f5a4462f53a02c385fa5bd57ae022ff0c3c43768aea3edc 0.0s done
#4 DONE 118.0s

#5 [2/5] RUN wget https://repo.radeon.com/amdgpu-install/6.3/ubuntu/noble/amdgpu-install_6.3.60300-1_all.deb &&      apt-get update --yes &&     apt-get install --yes ./amdgpu-install_6.3.60300-1_all.deb
#5 0.232 --2025-05-07 18:44:59--  https://repo.radeon.com/amdgpu-install/6.3/ubuntu/noble/amdgpu-install_6.3.60300-1_all.deb
#5 0.255 Resolving repo.radeon.com (repo.radeon.com)... 23.221.22.215, 23.221.22.214, 2600:1404:6400:25::17de:f148, ...
#5 0.269 Connecting to repo.radeon.com (repo.radeon.com)|23.221.22.215|:443... connected.
#5 0.284 HTTP request sent, awaiting response... 200 OK
#5 0.300 Length: 16980 (17K) [application/octet-stream]
#5 0.302 Saving to: ‘amdgpu-install_6.3.60300-1_all.deb’
#5 0.302 
#5 0.302      0K .......... ......                                     100%  102M=0s
#5 0.302 
#5 0.302 2025-05-07 18:44:59 (102 MB/s) - ‘amdgpu-install_6.3.60300-1_all.deb’ saved [16980/16980]
#5 0.302 
#5 0.609 Get:1 http://security.ubuntu.com/ubuntu noble-security InRelease [126 kB]
#5 0.657 Get:2 http://archive.ubuntu.com/ubuntu noble InRelease [256 kB]
#5 1.179 Get:3 http://security.ubuntu.com/ubuntu noble-security/restricted amd64 Packages [1318 kB]
#5 1.246 Get:4 http://archive.ubuntu.com/ubuntu noble-updates InRelease [126 kB]
#5 1.392 Get:5 http://archive.ubuntu.com/ubuntu noble-backports InRelease [126 kB]
#5 1.541 Get:6 http://archive.ubuntu.com/ubuntu noble/universe amd64 Packages [19.3 MB]
#5 1.714 Get:7 http://security.ubuntu.com/ubuntu noble-security/universe amd64 Packages [1080 kB]
#5 1.775 Get:8 http://security.ubuntu.com/ubuntu noble-security/multiverse amd64 Packages [22.1 kB]
#5 1.776 Get:9 http://security.ubuntu.com/ubuntu noble-security/main amd64 Packages [1033 kB]
#5 2.461 Get:10 http://archive.ubuntu.com/ubuntu noble/multiverse amd64 Packages [331 kB]
#5 2.465 Get:11 http://archive.ubuntu.com/ubuntu noble/restricted amd64 Packages [117 kB]
#5 2.466 Get:12 http://archive.ubuntu.com/ubuntu noble/main amd64 Packages [1808 kB]
#5 2.487 Get:13 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 Packages [1353 kB]
#5 2.499 Get:14 http://archive.ubuntu.com/ubuntu noble-updates/universe amd64 Packages [1378 kB]
#5 2.586 Get:15 http://archive.ubuntu.com/ubuntu noble-updates/restricted amd64 Packages [1362 kB]
#5 2.601 Get:16 http://archive.ubuntu.com/ubuntu noble-updates/multiverse amd64 Packages [26.7 kB]
#5 2.601 Get:17 http://archive.ubuntu.com/ubuntu noble-backports/universe amd64 Packages [31.8 kB]
#5 2.601 Get:18 http://archive.ubuntu.com/ubuntu noble-backports/main amd64 Packages [48.0 kB]
#5 3.219 Fetched 29.9 MB in 3s (10.4 MB/s)
#5 3.219 Reading package lists...
#5 3.881 Reading package lists...
#5 4.544 Building dependency tree...
#5 4.663 Reading state information...
#5 4.782 The following additional packages will be installed:
#5 4.783   dialog libpopt0 rsync
#5 4.783 Suggested packages:
#5 4.783   openssh-server python3-braceexpand
#5 4.828 The following NEW packages will be installed:
#5 4.829   amdgpu-install dialog libpopt0 rsync
#5 4.857 0 upgraded, 4 newly installed, 0 to remove and 0 not upgraded.
#5 4.857 Need to get 768 kB/785 kB of archives.
#5 4.857 After this operation, 2258 kB of additional disk space will be used.
#5 4.857 Get:1 /home/jovyan/amdgpu-install_6.3.60300-1_all.deb amdgpu-install all 6.3.60300-2084815.24.04 [17.0 kB]
#5 5.080 Get:2 http://archive.ubuntu.com/ubuntu noble/main amd64 libpopt0 amd64 1.19+dfsg-1build1 [28.6 kB]
#5 5.323 Get:3 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 rsync amd64 3.2.7-1ubuntu1.2 [436 kB]
#5 5.747 Get:4 http://archive.ubuntu.com/ubuntu noble/universe amd64 dialog amd64 1.3-20240101-1 [303 kB]
#5 5.952 debconf: delaying package configuration, since apt-utils is not installed
#5 5.981 Fetched 768 kB in 1s (776 kB/s)
#5 6.007 Selecting previously unselected package libpopt0:amd64.
(Reading database ... 52749 files and directories currently installed.)
#5 6.033 Preparing to unpack .../libpopt0_1.19+dfsg-1build1_amd64.deb ...
#5 6.035 Unpacking libpopt0:amd64 (1.19+dfsg-1build1) ...
#5 6.074 Selecting previously unselected package rsync.
#5 6.079 Preparing to unpack .../rsync_3.2.7-1ubuntu1.2_amd64.deb ...
#5 6.082 Unpacking rsync (3.2.7-1ubuntu1.2) ...
#5 6.116 Selecting previously unselected package amdgpu-install.
#5 6.120 Preparing to unpack .../amdgpu-install_6.3.60300-1_all.deb ...
#5 6.121 Unpacking amdgpu-install (6.3.60300-2084815.24.04) ...
#5 6.146 Selecting previously unselected package dialog.
#5 6.150 Preparing to unpack .../dialog_1.3-20240101-1_amd64.deb ...
#5 6.151 Unpacking dialog (1.3-20240101-1) ...
#5 6.210 Setting up dialog (1.3-20240101-1) ...
#5 6.213 Setting up libpopt0:amd64 (1.19+dfsg-1build1) ...
#5 6.215 Setting up rsync (3.2.7-1ubuntu1.2) ...
#5 6.231 invoke-rc.d: could not determine current runlevel
#5 6.237 invoke-rc.d: policy-rc.d denied execution of start.
#5 6.307 Setting up amdgpu-install (6.3.60300-2084815.24.04) ...
#5 6.317 Processing triggers for libc-bin (2.39-0ubuntu8.4) ...
#5 DONE 8.8s

#6 [3/5] RUN amdgpu-install --usecase=rocm -y && rm *.deb
#6 1.000 Get:1 https://repo.radeon.com/amdgpu/6.3/ubuntu noble InRelease [5433 B]
#6 1.007 Get:2 https://repo.radeon.com/rocm/apt/6.3 noble InRelease [2603 B]
#6 1.068 Get:3 https://repo.radeon.com/amdgpu/6.3/ubuntu noble/main i386 Packages [12.2 kB]
#6 1.084 Get:4 https://repo.radeon.com/amdgpu/6.3/ubuntu noble/main amd64 Packages [14.1 kB]
#6 1.116 Get:5 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 Packages [59.9 kB]
#6 1.120 Hit:6 http://archive.ubuntu.com/ubuntu noble InRelease
#6 1.120 Hit:7 http://security.ubuntu.com/ubuntu noble-security InRelease
#6 1.226 Hit:8 http://archive.ubuntu.com/ubuntu noble-updates InRelease
#6 1.349 Hit:9 http://archive.ubuntu.com/ubuntu noble-backports InRelease
#6 1.416 Fetched 94.3 kB in 1s (179 kB/s)
#6 1.416 Reading package lists...
#6 2.075 Reading package lists...
#6 2.721 Building dependency tree...
#6 2.838 Reading state information...
#6 2.972 The following additional packages will be installed:
#6 2.972   amd-smi-lib amdgpu-core amdgpu-dkms-firmware autoconf automake autotools-dev
#6 2.972   busybox-initramfs comgr composablekernel-dev cpio dbus dbus-bin dbus-daemon
#6 2.972   dbus-session-bus-common dbus-system-bus-common dhcpcd-base dkms dmsetup
#6 2.972   dracut-install fakeroot file g++-13-multilib g++-multilib gcc-11-base
#6 2.972   gcc-13-multilib gcc-multilib gdb gir1.2-girepository-2.0 gir1.2-glib-2.0
#6 2.972   half hip-dev hip-doc hip-runtime-amd hip-samples hipblas hipblas-common-dev
#6 2.972   hipblas-dev hipblaslt hipblaslt-dev hipcc hipcub-dev hipfft hipfft-dev
#6 2.972   hipfort-dev hipify-clang hiprand hiprand-dev hipsolver hipsolver-dev
#6 2.972   hipsparse hipsparse-dev hipsparselt hipsparselt-dev hiptensor hiptensor-dev
#6 2.972   hsa-amd-aqlprofile hsa-rocr hsa-rocr-dev icu-devtools initramfs-tools
#6 2.972   initramfs-tools-bin initramfs-tools-core javascript-common klibc-utils kmod
#6 2.972   lib32asan8 lib32atomic1 lib32gcc-13-dev lib32gcc-s1 lib32gomp1 lib32itm1
#6 2.972   lib32quadmath0 lib32stdc++-13-dev lib32stdc++6 lib32ubsan1 libamd3
#6 2.972   libargon2-1 libasan6 libavcodec-dev libavformat-dev libavutil-dev
#6 2.972   libbabeltrace1 libc6-dbg libc6-dev-i386 libc6-dev-x32 libc6-i386 libc6-x32
#6 2.972   libcamd3 libccolamd3 libcholmod5 libcolamd3 libcryptsetup12
#6 2.972   libdebuginfod-common libdebuginfod1t64 libdevmapper1.02.1
#6 2.972   libdrm-amdgpu-amdgpu1 libdrm-amdgpu-common libdrm-amdgpu-dev
#6 2.972   libdrm-amdgpu-radeon1 libdrm-dev libdrm-nouveau2 libdrm2-amdgpu libdw1t64
#6 2.972   libelf-dev libexpat1-dev libfakeroot libfdisk1 libfile-copy-recursive-perl
#6 2.972   libfile-listing-perl libfile-which-perl libgcc-11-dev libgirepository-1.0-1
#6 2.972   libgl-dev libglx-dev libgpm2 libhttp-date-perl libicu-dev libipt2
#6 2.972   libjs-jquery libjs-sphinxdoc libjs-underscore libjson-c5 libklibc libkmod2
#6 2.972   libmagic-mgc libmagic1t64 libncurses-dev libncurses6 libnuma-dev libpci3
#6 2.972   libpciaccess-dev libpthread-stubs0-dev libpython3-dev libpython3.12-dev
#6 2.973   libpython3.12t64 libsource-highlight-common libsource-highlight4t64
#6 2.973   libstdc++-11-dev libsuitesparseconfig7 libswresample-dev libswscale-dev
#6 2.973   libsystemd-shared libtimedate-perl libtsan0 liburi-perl libx11-dev
#6 2.973   libx32asan8 libx32atomic1 libx32gcc-13-dev libx32gcc-s1 libx32gomp1
#6 2.973   libx32itm1 libx32quadmath0 libx32stdc++-13-dev libx32stdc++6 libx32ubsan1
#6 2.973   libxau-dev libxcb1-dev libxdmcp-dev libxml2-dev libzstd-dev linux-base
#6 2.973   linux-hwe-6.11-headers-6.11.0-17 lsb-release m4 mesa-common-dev migraphx
#6 2.973   migraphx-dev miopen-hip miopen-hip-dev mivisionx mivisionx-dev
#6 2.973   networkd-dispatcher openmp-extras-dev openmp-extras-runtime pci.ids pciutils
#6 2.973   python3-argcomplete python3-dbus python3-dev python3-gi python3-pip
#6 2.973   python3-pkg-resources python3-setuptools python3-wheel python3-yaml
#6 2.973   python3.12-dev rccl rccl-dev rocalution rocalution-dev rocblas rocblas-dev
#6 2.973   rocfft rocfft-dev rocm-cmake rocm-core rocm-dbgapi rocm-debug-agent
#6 2.973   rocm-developer-tools rocm-device-libs rocm-gdb rocm-hip-libraries
#6 2.973   rocm-hip-runtime rocm-hip-runtime-dev rocm-hip-sdk rocm-language-runtime
#6 2.973   rocm-llvm rocm-ml-libraries rocm-ml-sdk rocm-opencl rocm-opencl-dev
#6 2.973   rocm-opencl-runtime rocm-opencl-sdk rocm-openmp-sdk rocm-smi-lib rocm-utils
#6 2.973   rocminfo rocprim-dev rocprofiler rocprofiler-dev rocprofiler-plugins
#6 2.973   rocprofiler-register rocprofiler-sdk rocprofiler-sdk-roctx rocrand
#6 2.973   rocrand-dev rocsolver rocsolver-dev rocsparse rocsparse-dev rocthrust-dev
#6 2.973   roctracer roctracer-dev rocwmma-dev rpp rpp-dev systemd systemd-dev
#6 2.973   systemd-hwe-hwdb systemd-resolved systemd-timesyncd udev valgrind
#6 2.973   x11proto-dev xorg-sgml-doctools xtrans-dev zlib1g-dev zstd
#6 2.974 Suggested packages:
#6 2.974   autoconf-archive gnu-standards autoconf-doc libtool gettext libarchive-dev
#6 2.974   default-dbus-session-bus | dbus-session-bus menu lib32stdc++6-13-dbg
#6 2.974   libx32stdc++6-13-dbg gdb-doc gdbserver bash-completion apache2 | lighttpd
#6 2.974   | httpd gpm icu-doc ncurses-doc libstdc++-11-doc libbusiness-isbn-perl
#6 2.974   libregexp-ipv6-perl libwww-perl libx11-doc libxcb-doc pkg-config m4-doc iw
#6 2.974   | wireless-tools python-dbus-doc python-setuptools-doc systemd-container
#6 2.974   systemd-homed systemd-userdbd systemd-boot libip4tc2 libqrencode4
#6 2.974   libtss2-esys-3.0.2-0 libtss2-mu-4.0.1-0 libtss2-rc0 libtss2-tcti-device0
#6 2.974   polkitd valgrind-dbg valgrind-mpi kcachegrind alleyoop valkyrie
#6 3.283 The following NEW packages will be installed:
#6 3.283   amd-smi-lib amdgpu-core amdgpu-dkms amdgpu-dkms-firmware autoconf automake
#6 3.283   autotools-dev busybox-initramfs comgr composablekernel-dev cpio dbus
#6 3.283   dbus-bin dbus-daemon dbus-session-bus-common dbus-system-bus-common
#6 3.283   dhcpcd-base dkms dmsetup dracut-install fakeroot file g++-13-multilib
#6 3.283   g++-multilib gcc-11-base gcc-13-multilib gcc-multilib gdb
#6 3.283   gir1.2-girepository-2.0 gir1.2-glib-2.0 half hip-dev hip-doc hip-runtime-amd
#6 3.283   hip-samples hipblas hipblas-common-dev hipblas-dev hipblaslt hipblaslt-dev
#6 3.283   hipcc hipcub-dev hipfft hipfft-dev hipfort-dev hipify-clang hiprand
#6 3.283   hiprand-dev hipsolver hipsolver-dev hipsparse hipsparse-dev hipsparselt
#6 3.283   hipsparselt-dev hiptensor hiptensor-dev hsa-amd-aqlprofile hsa-rocr
#6 3.284   hsa-rocr-dev icu-devtools initramfs-tools initramfs-tools-bin
#6 3.284   initramfs-tools-core javascript-common klibc-utils kmod lib32asan8
#6 3.284   lib32atomic1 lib32gcc-13-dev lib32gcc-s1 lib32gomp1 lib32itm1 lib32quadmath0
#6 3.284   lib32stdc++-13-dev lib32stdc++6 lib32ubsan1 libamd3 libargon2-1 libasan6
#6 3.284   libavcodec-dev libavformat-dev libavutil-dev libbabeltrace1 libc6-dbg
#6 3.284   libc6-dev-i386 libc6-dev-x32 libc6-i386 libc6-x32 libcamd3 libccolamd3
#6 3.284   libcholmod5 libcolamd3 libcryptsetup12 libdebuginfod-common
#6 3.284   libdebuginfod1t64 libdevmapper1.02.1 libdrm-amdgpu-amdgpu1
#6 3.284   libdrm-amdgpu-common libdrm-amdgpu-dev libdrm-amdgpu-radeon1 libdrm-dev
#6 3.284   libdrm-nouveau2 libdrm2-amdgpu libdw1t64 libelf-dev libexpat1-dev
#6 3.284   libfakeroot libfdisk1 libfile-copy-recursive-perl libfile-listing-perl
#6 3.284   libfile-which-perl libgcc-11-dev libgirepository-1.0-1 libgl-dev libglx-dev
#6 3.284   libgpm2 libhttp-date-perl libicu-dev libipt2 libjs-jquery libjs-sphinxdoc
#6 3.284   libjs-underscore libjson-c5 libklibc libkmod2 libmagic-mgc libmagic1t64
#6 3.284   libncurses-dev libncurses6 libnuma-dev libpci3 libpciaccess-dev
#6 3.284   libpthread-stubs0-dev libpython3-dev libpython3.12-dev libpython3.12t64
#6 3.284   libsource-highlight-common libsource-highlight4t64 libstdc++-11-dev
#6 3.284   libsuitesparseconfig7 libswresample-dev libswscale-dev libsystemd-shared
#6 3.285   libtimedate-perl libtsan0 liburi-perl libx11-dev libx32asan8 libx32atomic1
#6 3.285   libx32gcc-13-dev libx32gcc-s1 libx32gomp1 libx32itm1 libx32quadmath0
#6 3.285   libx32stdc++-13-dev libx32stdc++6 libx32ubsan1 libxau-dev libxcb1-dev
#6 3.285   libxdmcp-dev libxml2-dev libzstd-dev linux-base
#6 3.285   linux-headers-6.11.0-17-generic linux-hwe-6.11-headers-6.11.0-17 lsb-release
#6 3.285   m4 mesa-common-dev migraphx migraphx-dev miopen-hip miopen-hip-dev mivisionx
#6 3.285   mivisionx-dev networkd-dispatcher openmp-extras-dev openmp-extras-runtime
#6 3.285   pci.ids pciutils python3-argcomplete python3-dbus python3-dev python3-gi
#6 3.285   python3-pip python3-pkg-resources python3-setuptools python3-wheel
#6 3.285   python3-yaml python3.12-dev rccl rccl-dev rocalution rocalution-dev rocblas
#6 3.285   rocblas-dev rocfft rocfft-dev rocm rocm-cmake rocm-core rocm-dbgapi
#6 3.285   rocm-debug-agent rocm-developer-tools rocm-device-libs rocm-gdb
#6 3.285   rocm-hip-libraries rocm-hip-runtime rocm-hip-runtime-dev rocm-hip-sdk
#6 3.285   rocm-language-runtime rocm-llvm rocm-ml-libraries rocm-ml-sdk rocm-opencl
#6 3.285   rocm-opencl-dev rocm-opencl-runtime rocm-opencl-sdk rocm-openmp-sdk
#6 3.285   rocm-smi-lib rocm-utils rocminfo rocprim-dev rocprofiler rocprofiler-dev
#6 3.285   rocprofiler-plugins rocprofiler-register rocprofiler-sdk
#6 3.285   rocprofiler-sdk-roctx rocrand rocrand-dev rocsolver rocsolver-dev rocsparse
#6 3.285   rocsparse-dev rocthrust-dev roctracer roctracer-dev rocwmma-dev rpp rpp-dev
#6 3.285   systemd systemd-dev systemd-hwe-hwdb systemd-resolved systemd-timesyncd udev
#6 3.285   valgrind x11proto-dev xorg-sgml-doctools xtrans-dev zlib1g-dev zstd
#6 3.410 0 upgraded, 252 newly installed, 0 to remove and 0 not upgraded.
#6 3.410 Need to get 2932 MB of archives.
#6 3.410 After this operation, 35.9 GB of additional disk space will be used.
#6 3.410 Get:1 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocm-core amd64 6.3.0.60300-39~24.04 [14.0 kB]
#6 3.420 Get:2 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 amd-smi-lib amd64 24.7.1.60300-39~24.04 [1414 kB]
#6 3.460 Get:3 https://repo.radeon.com/amdgpu/6.3/ubuntu noble/main amd64 amdgpu-core all 1:6.3.60300-2084815.24.04 [2228 B]
#6 3.460 Get:4 https://repo.radeon.com/amdgpu/6.3/ubuntu noble/main amd64 amdgpu-dkms-firmware all 1:6.10.5.60300-2084815.24.04 [15.0 MB]
#6 3.507 Get:5 http://archive.ubuntu.com/ubuntu noble/main amd64 libargon2-1 amd64 0~20190702+dfsg-4build1 [20.8 kB]
#6 3.574 Get:6 https://repo.radeon.com/amdgpu/6.3/ubuntu noble/main amd64 amdgpu-dkms all 1:6.10.5.60300-2084815.24.04 [11.6 MB]
#6 3.651 Get:7 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 comgr amd64 2.8.0.60300-39~24.04 [53.9 MB]
#6 3.753 Get:8 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libdevmapper1.02.1 amd64 2:1.02.185-3ubuntu3.2 [139 kB]
#6 4.020 Get:9 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 composablekernel-dev amd64 1.1.0.60300-39~24.04 [522 MB]
#6 4.043 Get:10 http://archive.ubuntu.com/ubuntu noble/main amd64 libjson-c5 amd64 0.17-1build1 [35.3 kB]
#6 4.082 Get:11 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libcryptsetup12 amd64 2:2.7.0-1ubuntu4.2 [266 kB]
#6 4.213 Get:12 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libfdisk1 amd64 2.39.3-9ubuntu6.2 [146 kB]
#6 4.249 Get:13 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libkmod2 amd64 31+20240202-2ubuntu7.1 [51.7 kB]
#6 4.259 Get:14 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libsystemd-shared amd64 255.4-1ubuntu8.6 [2073 kB]
#6 4.431 Get:15 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 systemd-dev all 255.4-1ubuntu8.6 [104 kB]
#6 4.436 Get:16 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 systemd amd64 255.4-1ubuntu8.6 [3471 kB]
#6 4.559 Get:17 http://archive.ubuntu.com/ubuntu noble/main amd64 lsb-release all 12.0-2 [6564 B]
#6 4.559 Get:18 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 kmod amd64 31+20240202-2ubuntu7.1 [101 kB]
#6 4.560 Get:19 http://archive.ubuntu.com/ubuntu noble/main amd64 dkms all 3.0.11-1ubuntu13 [51.5 kB]
#6 4.560 Get:20 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libdebuginfod-common all 0.190-1.1ubuntu0.1 [14.6 kB]
#6 4.561 Get:21 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 dbus-bin amd64 1.14.10-4ubuntu4.1 [39.3 kB]
#6 4.561 Get:22 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 dbus-session-bus-common all 1.14.10-4ubuntu4.1 [80.5 kB]
#6 4.562 Get:23 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 dbus-daemon amd64 1.14.10-4ubuntu4.1 [118 kB]
#6 4.563 Get:24 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 dbus-system-bus-common all 1.14.10-4ubuntu4.1 [81.6 kB]
#6 4.627 Get:25 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 dbus amd64 1.14.10-4ubuntu4.1 [24.3 kB]
#6 4.718 Get:26 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 dhcpcd-base amd64 1:10.0.6-1ubuntu3.1 [215 kB]
#6 4.720 Get:27 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 dmsetup amd64 2:1.02.185-3ubuntu3.2 [79.2 kB]
#6 4.720 Get:28 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 gir1.2-glib-2.0 amd64 2.80.0-6ubuntu3.2 [183 kB]
#6 4.722 Get:29 http://archive.ubuntu.com/ubuntu noble/main amd64 libgirepository-1.0-1 amd64 1.80.1-1 [81.9 kB]
#6 4.723 Get:30 http://archive.ubuntu.com/ubuntu noble/main amd64 gir1.2-girepository-2.0 amd64 1.80.1-1 [24.5 kB]
#6 4.723 Get:31 http://archive.ubuntu.com/ubuntu noble/main amd64 python3-dbus amd64 1.3.2-5build3 [100 kB]
#6 4.724 Get:32 http://archive.ubuntu.com/ubuntu noble/main amd64 python3-gi amd64 3.48.2-1 [232 kB]
#6 4.727 Get:33 http://archive.ubuntu.com/ubuntu noble/main amd64 networkd-dispatcher all 2.2.4-1 [15.5 kB]
#6 4.727 Get:34 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 python3-pkg-resources all 68.1.2-2ubuntu1.1 [168 kB]
#6 4.809 Get:35 http://archive.ubuntu.com/ubuntu noble/main amd64 python3-yaml amd64 6.0.1-2build2 [123 kB]
#6 4.907 Get:36 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 udev amd64 255.4-1ubuntu8.6 [1873 kB]
#6 4.926 Get:37 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 systemd-hwe-hwdb all 255.1.4 [3200 B]
#6 4.926 Get:38 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 systemd-resolved amd64 255.4-1ubuntu8.6 [296 kB]
#6 4.929 Get:39 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 systemd-timesyncd amd64 255.4-1ubuntu8.6 [35.3 kB]
#6 4.929 Get:40 http://archive.ubuntu.com/ubuntu noble/main amd64 cpio amd64 2.15+dfsg-1ubuntu2 [82.7 kB]
#6 4.930 Get:41 http://archive.ubuntu.com/ubuntu noble/main amd64 libmagic-mgc amd64 1:5.45-3build1 [307 kB]
#6 4.933 Get:42 http://archive.ubuntu.com/ubuntu noble/main amd64 libmagic1t64 amd64 1:5.45-3build1 [87.2 kB]
#6 4.934 Get:43 http://archive.ubuntu.com/ubuntu noble/main amd64 file amd64 1:5.45-3build1 [22.0 kB]
#6 4.934 Get:44 http://archive.ubuntu.com/ubuntu noble/main amd64 libgpm2 amd64 1.20.7-11 [14.1 kB]
#6 5.010 Get:45 http://archive.ubuntu.com/ubuntu noble/main amd64 libncurses6 amd64 6.4+20240113-1ubuntu2 [112 kB]
#6 5.120 Get:46 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 pci.ids all 0.0~2024.03.31-1ubuntu0.1 [275 kB]
#6 5.122 Get:47 http://archive.ubuntu.com/ubuntu noble/main amd64 libpci3 amd64 1:3.10.0-2build1 [36.5 kB]
#6 5.123 Get:48 http://archive.ubuntu.com/ubuntu noble/main amd64 pciutils amd64 1:3.10.0-2build1 [69.7 kB]
#6 5.123 Get:49 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 python3-setuptools all 68.1.2-2ubuntu1.1 [396 kB]
#6 5.127 Get:50 http://archive.ubuntu.com/ubuntu noble/universe amd64 python3-wheel all 0.42.0-2 [53.1 kB]
#6 5.128 Get:51 http://archive.ubuntu.com/ubuntu noble-updates/universe amd64 python3-pip all 24.0+dfsg-1ubuntu1.1 [1317 kB]
#6 5.141 Get:52 http://archive.ubuntu.com/ubuntu noble/main amd64 m4 amd64 1.4.19-4build1 [244 kB]
#6 5.144 Get:53 http://archive.ubuntu.com/ubuntu noble/main amd64 autoconf all 2.71-3 [339 kB]
#6 5.147 Get:54 http://archive.ubuntu.com/ubuntu noble/main amd64 autotools-dev all 20220109.1 [44.9 kB]
#6 5.229 Get:55 http://archive.ubuntu.com/ubuntu noble/main amd64 automake all 1:1.16.5-1.3ubuntu1 [558 kB]
#6 5.336 Get:56 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 busybox-initramfs amd64 1:1.36.1-6ubuntu3.1 [189 kB]
#6 5.337 Get:57 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 dracut-install amd64 060+5-1ubuntu3.3 [32.3 kB]
#6 5.338 Get:58 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 initramfs-tools-bin amd64 0.142ubuntu25.5 [21.5 kB]
#6 5.338 Get:59 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libklibc amd64 2.0.13-4ubuntu0.1 [47.2 kB]
#6 5.339 Get:60 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 klibc-utils amd64 2.0.13-4ubuntu0.1 [100 kB]
#6 5.340 Get:61 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 initramfs-tools-core all 0.142ubuntu25.5 [50.5 kB]
#6 5.340 Get:62 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 linux-base all 4.5ubuntu9+24.04.1 [18.1 kB]
#6 5.341 Get:63 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 initramfs-tools all 0.142ubuntu25.5 [9060 B]
#6 5.341 Get:64 http://archive.ubuntu.com/ubuntu noble/main amd64 libncurses-dev amd64 6.4+20240113-1ubuntu2 [384 kB]
#6 5.441 Get:65 http://archive.ubuntu.com/ubuntu noble/main amd64 libfakeroot amd64 1.33-1 [32.4 kB]
#6 5.562 Get:66 http://archive.ubuntu.com/ubuntu noble/main amd64 fakeroot amd64 1.33-1 [67.2 kB]
#6 5.562 Get:67 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libc6-i386 amd64 2.39-0ubuntu8.4 [2787 kB]
#6 5.591 Get:68 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libc6-dev-i386 amd64 2.39-0ubuntu8.4 [1447 kB]
#6 5.669 Get:69 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libc6-x32 amd64 2.39-0ubuntu8.4 [2917 kB]
#6 5.709 Get:70 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libc6-dev-x32 amd64 2.39-0ubuntu8.4 [1636 kB]
#6 5.782 Get:71 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 lib32gcc-s1 amd64 14.2.0-4ubuntu2~24.04 [92.3 kB]
#6 5.783 Get:72 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libx32gcc-s1 amd64 14.2.0-4ubuntu2~24.04 [78.5 kB]
#6 5.783 Get:73 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 lib32gomp1 amd64 14.2.0-4ubuntu2~24.04 [141 kB]
#6 5.785 Get:74 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libx32gomp1 amd64 14.2.0-4ubuntu2~24.04 [145 kB]
#6 5.788 Get:75 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 lib32itm1 amd64 14.2.0-4ubuntu2~24.04 [29.6 kB]
#6 5.789 Get:76 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libx32itm1 amd64 14.2.0-4ubuntu2~24.04 [29.8 kB]
#6 5.790 Get:77 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 lib32atomic1 amd64 14.2.0-4ubuntu2~24.04 [8586 B]
#6 5.904 Get:78 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libx32atomic1 amd64 14.2.0-4ubuntu2~24.04 [10.3 kB]
#6 5.904 Get:79 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 lib32asan8 amd64 14.2.0-4ubuntu2~24.04 [2879 kB]
#6 6.020 Get:80 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libx32asan8 amd64 14.2.0-4ubuntu2~24.04 [2893 kB]
#6 6.055 Get:81 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 lib32stdc++6 amd64 14.2.0-4ubuntu2~24.04 [814 kB]
#6 6.137 Get:82 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 lib32ubsan1 amd64 14.2.0-4ubuntu2~24.04 [1150 kB]
#6 6.148 Get:83 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libx32stdc++6 amd64 14.2.0-4ubuntu2~24.04 [778 kB]
#6 6.155 Get:84 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libx32ubsan1 amd64 14.2.0-4ubuntu2~24.04 [1169 kB]
#6 6.166 Get:85 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 lib32quadmath0 amd64 14.2.0-4ubuntu2~24.04 [227 kB]
#6 6.246 Get:86 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libx32quadmath0 amd64 14.2.0-4ubuntu2~24.04 [157 kB]
#6 6.247 Get:87 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 lib32gcc-13-dev amd64 13.3.0-6ubuntu2~24.04 [2380 kB]
#6 6.269 Get:88 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libx32gcc-13-dev amd64 13.3.0-6ubuntu2~24.04 [2190 kB]
#6 6.381 Get:89 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 gcc-13-multilib amd64 13.3.0-6ubuntu2~24.04 [878 B]
#6 6.382 Get:90 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 lib32stdc++-13-dev amd64 13.3.0-6ubuntu2~24.04 [1150 kB]
#6 6.411 Get:91 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libx32stdc++-13-dev amd64 13.3.0-6ubuntu2~24.04 [1086 kB]
#6 6.439 Get:92 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 g++-13-multilib amd64 13.3.0-6ubuntu2~24.04 [890 B]
#6 6.440 Get:93 http://archive.ubuntu.com/ubuntu noble/main amd64 gcc-multilib amd64 4:13.2.0-7ubuntu1 [1474 B]
#6 6.440 Get:94 http://archive.ubuntu.com/ubuntu noble/main amd64 g++-multilib amd64 4:13.2.0-7ubuntu1 [884 B]
#6 6.453 Get:95 http://archive.ubuntu.com/ubuntu noble/universe amd64 gcc-11-base amd64 11.4.0-9ubuntu1 [44.7 kB]
#6 6.454 Get:96 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libdw1t64 amd64 0.190-1.1ubuntu0.1 [261 kB]
#6 6.459 Get:97 http://archive.ubuntu.com/ubuntu noble/main amd64 libbabeltrace1 amd64 1.5.11-3build3 [164 kB]
#6 6.548 Get:98 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libdebuginfod1t64 amd64 0.190-1.1ubuntu0.1 [17.1 kB]
#6 6.549 Get:99 http://archive.ubuntu.com/ubuntu noble/main amd64 libipt2 amd64 2.0.6-1build1 [45.7 kB]
#6 6.550 Get:100 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libpython3.12t64 amd64 3.12.3-1ubuntu0.5 [2339 kB]
#6 6.610 Get:101 http://archive.ubuntu.com/ubuntu noble/main amd64 libsource-highlight-common all 3.1.9-4.3build1 [64.2 kB]
#6 6.616 Get:102 http://archive.ubuntu.com/ubuntu noble/main amd64 libsource-highlight4t64 amd64 3.1.9-4.3build1 [258 kB]
#6 6.622 Get:103 http://archive.ubuntu.com/ubuntu noble/main amd64 gdb amd64 15.0.50.20240403-0ubuntu1 [4010 kB]
#6 6.752 Get:104 http://archive.ubuntu.com/ubuntu noble/universe amd64 libfile-copy-recursive-perl all 0.45-4 [16.5 kB]
#6 6.757 Get:105 http://archive.ubuntu.com/ubuntu noble/main amd64 libtimedate-perl all 2.3300-2 [34.0 kB]
#6 6.758 Get:106 http://archive.ubuntu.com/ubuntu noble/main amd64 libhttp-date-perl all 6.06-1 [10.2 kB]
#6 6.934 Get:107 http://archive.ubuntu.com/ubuntu noble/main amd64 libfile-listing-perl all 6.16-1 [11.3 kB]
#6 6.937 Get:108 http://archive.ubuntu.com/ubuntu noble/main amd64 libfile-which-perl all 1.27-2 [12.5 kB]
#6 7.049 Get:109 http://archive.ubuntu.com/ubuntu noble/main amd64 liburi-perl all 5.27-1 [88.0 kB]
#6 7.249 Get:110 http://archive.ubuntu.com/ubuntu noble/universe amd64 libasan6 amd64 11.4.0-9ubuntu1 [2284 kB]
#6 7.721 Get:111 http://archive.ubuntu.com/ubuntu noble/universe amd64 libtsan0 amd64 11.4.0-9ubuntu1 [2268 kB]
#6 7.798 Get:112 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 half amd64 1.12.0.60300-39~24.04 [19.6 kB]
#6 7.799 Get:113 https://repo.radeon.com/amdgpu/6.3/ubuntu noble/main amd64 libdrm2-amdgpu amd64 1:2.4.123.60300-2084815.24.04 [37.6 kB]
#6 7.799 Get:114 https://repo.radeon.com/amdgpu/6.3/ubuntu noble/main amd64 libdrm-amdgpu-common all 1.0.0.60300-2084815.24.04 [5176 B]
#6 7.800 Get:115 https://repo.radeon.com/amdgpu/6.3/ubuntu noble/main amd64 libdrm-amdgpu-amdgpu1 amd64 1:2.4.123.60300-2084815.24.04 [21.4 kB]
#6 7.800 Get:116 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocprofiler-register amd64 0.4.0.60300-39~24.04 [233 kB]
#6 7.803 Get:117 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 hsa-rocr amd64 1.14.0.60300-39~24.04 [1366 kB]
#6 7.817 Get:118 http://archive.ubuntu.com/ubuntu noble/universe amd64 libgcc-11-dev amd64 11.4.0-9ubuntu1 [2481 kB]
#6 7.823 Get:119 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocminfo amd64 1.0.0.60300-39~24.04 [29.2 kB]
#6 7.829 Get:120 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 hip-runtime-amd amd64 6.3.42131.60300-39~24.04 [12.0 MB]
#6 7.876 Get:121 http://archive.ubuntu.com/ubuntu noble/universe amd64 libstdc++-11-dev amd64 11.4.0-9ubuntu1 [2091 kB]
#6 7.926 Get:122 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocm-llvm amd64 18.0.0.24455.60300-39~24.04 [325 MB]
#6 7.932 Get:123 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libc6-dbg amd64 2.39-0ubuntu8.4 [7460 kB]
#6 8.103 Get:124 http://archive.ubuntu.com/ubuntu noble/main amd64 valgrind amd64 1:3.22.0-0ubuntu3 [14.9 MB]
#6 8.454 Get:125 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libdrm-nouveau2 amd64 2.4.122-1~ubuntu0.24.04.1 [17.7 kB]
#6 8.454 Get:126 http://archive.ubuntu.com/ubuntu noble/main amd64 libpciaccess-dev amd64 0.17-3build1 [22.0 kB]
#6 8.455 Get:127 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libdrm-dev amd64 2.4.122-1~ubuntu0.24.04.1 [310 kB]
#6 8.457 Get:128 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 icu-devtools amd64 74.2-1ubuntu3.1 [212 kB]
#6 8.460 Get:129 http://archive.ubuntu.com/ubuntu noble/main amd64 javascript-common all 11+nmu1 [5936 B]
#6 8.460 Get:130 http://archive.ubuntu.com/ubuntu noble/main amd64 libsuitesparseconfig7 amd64 1:7.6.1+dfsg-1build1 [12.9 kB]
#6 8.460 Get:131 http://archive.ubuntu.com/ubuntu noble/universe amd64 libamd3 amd64 1:7.6.1+dfsg-1build1 [27.2 kB]
#6 8.461 Get:132 http://archive.ubuntu.com/ubuntu noble/universe amd64 libavutil-dev amd64 7:6.1.1-3ubuntu5 [547 kB]
#6 8.465 Get:133 http://archive.ubuntu.com/ubuntu noble/universe amd64 libswresample-dev amd64 7:6.1.1-3ubuntu5 [79.7 kB]
#6 8.548 Get:134 http://archive.ubuntu.com/ubuntu noble/universe amd64 libavcodec-dev amd64 7:6.1.1-3ubuntu5 [6504 kB]
#6 8.710 Get:135 http://archive.ubuntu.com/ubuntu noble/universe amd64 libavformat-dev amd64 7:6.1.1-3ubuntu5 [1398 kB]
#6 8.738 Get:136 http://archive.ubuntu.com/ubuntu noble/universe amd64 libcamd3 amd64 1:7.6.1+dfsg-1build1 [23.8 kB]
#6 8.739 Get:137 http://archive.ubuntu.com/ubuntu noble/universe amd64 libccolamd3 amd64 1:7.6.1+dfsg-1build1 [25.9 kB]
#6 8.739 Get:138 http://archive.ubuntu.com/ubuntu noble/main amd64 libcolamd3 amd64 1:7.6.1+dfsg-1build1 [19.4 kB]
#6 8.740 Get:139 http://archive.ubuntu.com/ubuntu noble/universe amd64 libcholmod5 amd64 1:7.6.1+dfsg-1build1 [667 kB]
#6 8.758 Get:140 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 zlib1g-dev amd64 1:1.3.dfsg-3.1ubuntu2.1 [894 kB]
#6 8.773 Get:141 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libzstd-dev amd64 1.5.5+dfsg2-2build1.1 [364 kB]
#6 8.779 Get:142 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libelf-dev amd64 0.190-1.1ubuntu0.1 [68.5 kB]
#6 8.780 Get:143 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libexpat1-dev amd64 2.6.1-2ubuntu0.3 [140 kB]
#6 8.796 Get:144 http://archive.ubuntu.com/ubuntu noble/main amd64 xorg-sgml-doctools all 1:1.11-1.1 [10.9 kB]
#6 8.878 Get:145 http://archive.ubuntu.com/ubuntu noble/main amd64 x11proto-dev all 2023.2-1 [602 kB]
#6 8.888 Get:146 http://archive.ubuntu.com/ubuntu noble/main amd64 libxau-dev amd64 1:1.0.9-1build6 [9570 B]
#6 8.888 Get:147 http://archive.ubuntu.com/ubuntu noble/main amd64 libxdmcp-dev amd64 1:1.1.3-0ubuntu6 [26.5 kB]
#6 8.888 Get:148 http://archive.ubuntu.com/ubuntu noble/main amd64 xtrans-dev all 1.4.0-1 [68.9 kB]
#6 8.889 Get:149 http://archive.ubuntu.com/ubuntu noble/main amd64 libpthread-stubs0-dev amd64 0.4-1build3 [4746 B]
#6 8.889 Get:150 http://archive.ubuntu.com/ubuntu noble/main amd64 libxcb1-dev amd64 1.15-1ubuntu2 [85.8 kB]
#6 8.891 Get:151 http://archive.ubuntu.com/ubuntu noble/main amd64 libx11-dev amd64 2:1.8.7-1build1 [732 kB]
#6 8.905 Get:152 http://archive.ubuntu.com/ubuntu noble/main amd64 libglx-dev amd64 1.7.0-1build1 [14.2 kB]
#6 8.906 Get:153 http://archive.ubuntu.com/ubuntu noble/main amd64 libgl-dev amd64 1.7.0-1build1 [102 kB]
#6 8.958 Get:154 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libicu-dev amd64 74.2-1ubuntu3.1 [11.9 MB]
#6 9.260 Get:155 http://archive.ubuntu.com/ubuntu noble/main amd64 libjs-jquery all 3.6.1+dfsg+~3.5.14-1 [328 kB]
#6 9.263 Get:156 http://archive.ubuntu.com/ubuntu noble/main amd64 libjs-underscore all 1.13.4~dfsg+~1.11.4-3 [118 kB]
#6 9.264 Get:157 http://archive.ubuntu.com/ubuntu noble/main amd64 libjs-sphinxdoc all 7.2.6-6 [149 kB]
#6 9.284 Get:158 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libpython3.12-dev amd64 3.12.3-1ubuntu0.5 [5675 kB]
#6 9.438 Get:159 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libpython3-dev amd64 3.12.3-0ubuntu2 [10.3 kB]
#6 9.438 Get:160 http://archive.ubuntu.com/ubuntu noble/universe amd64 libswscale-dev amd64 7:6.1.1-3ubuntu5 [224 kB]
#6 9.440 Get:161 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libxml2-dev amd64 2.9.14+dfsg-1.3ubuntu3.3 [780 kB]
#6 9.446 Get:162 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 linux-hwe-6.11-headers-6.11.0-17 all 6.11.0-17.17~24.04.2 [13.8 MB]
#6 9.907 Get:163 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 linux-headers-6.11.0-17-generic amd64 6.11.0-17.17~24.04.2 [3900 kB]
#6 9.958 Get:164 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 mesa-common-dev amd64 24.2.8-1ubuntu1~24.04.1 [2696 kB]
#6 10.07 Get:165 http://archive.ubuntu.com/ubuntu noble-updates/universe amd64 python3-argcomplete all 3.1.4-1ubuntu0.1 [33.8 kB]
#6 10.08 Get:166 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 python3.12-dev amd64 3.12.3-1ubuntu0.5 [498 kB]
#6 10.08 Get:167 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 python3-dev amd64 3.12.3-0ubuntu2 [26.7 kB]
#6 10.09 Get:168 http://archive.ubuntu.com/ubuntu noble/main amd64 libnuma-dev amd64 2.0.18-1build1 [37.0 kB]
#6 10.09 Get:169 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 zstd amd64 1.5.5+dfsg2-2build1.1 [644 kB]
#6 10.27 Get:170 https://repo.radeon.com/amdgpu/6.3/ubuntu noble/main amd64 libdrm-amdgpu-radeon1 amd64 1:2.4.123.60300-2084815.24.04 [24.4 kB]
#6 10.27 Get:171 https://repo.radeon.com/amdgpu/6.3/ubuntu noble/main amd64 libdrm-amdgpu-dev amd64 1:2.4.123.60300-2084815.24.04 [144 kB]
#6 10.28 Get:172 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 hsa-rocr-dev amd64 1.14.0.60300-39~24.04 [135 kB]
#6 10.28 Get:173 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 hip-dev amd64 6.3.42131.60300-39~24.04 [316 kB]
#6 10.28 Get:174 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 hip-doc amd64 6.3.42131.60300-39~24.04 [96.0 kB]
#6 10.28 Get:175 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 hipcc amd64 1.1.1.60300-39~24.04 [223 kB]
#6 10.28 Get:176 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 hip-samples amd64 6.3.42131.60300-39~24.04 [51.7 kB]
#6 10.28 Get:177 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 hipblaslt amd64 0.10.0.60300-39~24.04 [329 MB]
#6 12.69 Get:178 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocblas amd64 4.3.0.60300-39~24.04 [149 MB]
#6 13.76 Get:179 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocsolver amd64 3.27.0.60300-39~24.04 [262 MB]
#6 15.88 Get:180 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 hipblas amd64 2.3.0.60300-39~24.04 [168 kB]
#6 15.89 Get:181 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 hipblas-common-dev amd64 1.0.0.60300-39~24.04 [5758 B]
#6 15.89 Get:182 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 hipblas-dev amd64 2.3.0.60300-39~24.04 [98.2 kB]
#6 15.89 Get:183 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 hipblaslt-dev amd64 0.10.0.60300-39~24.04 [27.0 kB]
#6 15.89 Get:184 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocprim-dev amd64 3.3.0.60300-39~24.04 [230 kB]
#6 15.89 Get:185 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 hipcub-dev amd64 3.3.0.60300-39~24.04 [74.5 kB]
#6 15.89 Get:186 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocfft amd64 1.0.31.60300-39~24.04 [120 MB]
#6 16.76 Get:187 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 hipfft amd64 1.0.17.60300-39~24.04 [25.8 kB]
#6 16.76 Get:188 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 hipfft-dev amd64 1.0.17.60300-39~24.04 [11.2 kB]
#6 16.76 Get:189 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 hipfort-dev amd64 0.5.0.60300-39~24.04 [6659 kB]
#6 16.83 Get:190 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 hipify-clang amd64 18.0.0.60300-39~24.04 [20.7 MB]
#6 16.97 Get:191 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 hiprand amd64 2.11.0.60300-39~24.04 [5002 B]
#6 16.97 Get:192 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 hiprand-dev amd64 2.11.0.60300-39~24.04 [21.2 kB]
#6 16.97 Get:193 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 hipsolver amd64 2.3.0.60300-39~24.04 [54.6 kB]
#6 16.98 Get:194 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 hipsolver-dev amd64 2.3.0.60300-39~24.04 [18.9 kB]
#6 16.98 Get:195 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocsparse amd64 3.3.0.60300-39~24.04 [187 MB]
#6 18.30 Get:196 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 hipsparse amd64 3.1.2.60300-39~24.04 [46.7 kB]
#6 18.30 Get:197 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 hipsparse-dev amd64 3.1.2.60300-39~24.04 [49.1 kB]
#6 18.30 Get:198 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 hipsparselt amd64 0.2.2.60300-39~24.04 [10.3 MB]
#6 18.40 Get:199 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 hipsparselt-dev amd64 0.2.2.60300-39~24.04 [11.7 kB]
#6 18.40 Get:200 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 hiptensor amd64 1.4.0.60300-39~24.04 [34.3 MB]
#6 18.64 Get:201 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 hiptensor-dev amd64 1.4.0.60300-39~24.04 [13.2 kB]
#6 18.64 Get:202 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 hsa-amd-aqlprofile amd64 1.0.0.60300-39~24.04 [513 kB]
#6 18.64 Get:203 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 roctracer amd64 4.1.60300.60300-39~24.04 [521 kB]
#6 18.64 Get:204 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocrand amd64 3.2.0.60300-39~24.04 [23.2 MB]
#6 18.81 Get:205 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 miopen-hip amd64 3.3.0.60300-39~24.04 [163 MB]
#6 19.99 Get:206 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 migraphx amd64 2.11.0.60300-39~24.04 [49.6 MB]
#6 20.35 Get:207 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 migraphx-dev amd64 2.11.0.60300-39~24.04 [171 kB]
#6 20.35 Get:208 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 miopen-hip-dev amd64 3.3.0.60300-39~24.04 [47.7 kB]
#6 20.35 Get:209 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 openmp-extras-runtime amd64 18.63.0.60300-39~24.04 [154 MB]
#6 21.47 Get:210 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocm-language-runtime amd64 6.3.0.60300-39~24.04 [834 B]
#6 21.47 Get:211 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocm-hip-runtime amd64 6.3.0.60300-39~24.04 [2030 B]
#6 21.47 Get:212 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rpp amd64 1.9.1.60300-39~24.04 [70.2 MB]
#6 21.98 Get:213 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 mivisionx amd64 3.1.0.60300-39~24.04 [36.1 MB]
#6 22.26 Get:214 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocm-device-libs amd64 1.0.0.60300-39~24.04 [720 kB]
#6 22.27 Get:215 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocm-cmake amd64 0.14.0.60300-39~24.04 [24.7 kB]
#6 22.27 Get:216 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocm-hip-runtime-dev amd64 6.3.0.60300-39~24.04 [2206 B]
#6 22.27 Get:217 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rpp-dev amd64 1.9.1.60300-39~24.04 [48.0 kB]
#6 22.28 Get:218 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocblas-dev amd64 4.3.0.60300-39~24.04 [99.0 kB]
#6 22.28 Get:219 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 mivisionx-dev amd64 3.1.0.60300-39~24.04 [23.6 MB]
#6 22.46 Get:220 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 openmp-extras-dev amd64 18.63.0.60300-39~24.04 [51.2 MB]
#6 22.82 Get:221 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocm-smi-lib amd64 7.4.0.60300-39~24.04 [1074 kB]
#6 22.83 Get:222 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rccl amd64 2.21.5.60300-39~24.04 [53.9 MB]
#6 23.22 Get:223 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rccl-dev amd64 2.21.5.60300-39~24.04 [108 kB]
#6 23.22 Get:224 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocalution amd64 3.2.1.60300-39~24.04 [4970 kB]
#6 23.28 Get:225 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocalution-dev amd64 3.2.1.60300-39~24.04 [43.0 kB]
#6 23.28 Get:226 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocfft-dev amd64 1.0.31.60300-39~24.04 [10.6 kB]
#6 23.28 Get:227 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocm-utils amd64 6.3.0.60300-39~24.04 [810 B]
#6 23.28 Get:228 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocm-dbgapi amd64 0.77.0.60300-39~24.04 [1906 kB]
#6 23.29 Get:229 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocm-debug-agent amd64 2.0.3.60300-39~24.04 [60.7 kB]
#6 23.29 Get:230 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocm-gdb amd64 15.2.60300-39~24.04 [89.9 MB]
#6 23.93 Get:231 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocprofiler amd64 2.0.60300.60300-39~24.04 [983 kB]
#6 23.94 Get:232 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocprofiler-plugins amd64 2.0.60300.60300-39~24.04 [1085 kB]
#6 23.95 Get:233 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocprofiler-sdk-roctx amd64 0.5.0-39~24.04 [199 kB]
#6 23.96 Get:234 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocprofiler-sdk amd64 0.5.0-39~24.04 [3762 kB]
#6 23.99 Get:235 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocprofiler-dev amd64 2.0.60300.60300-39~24.04 [23.9 kB]
#6 23.99 Get:236 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 roctracer-dev amd64 4.1.60300.60300-39~24.04 [509 kB]
#6 23.99 Get:237 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocm-developer-tools amd64 6.3.0.60300-39~24.04 [2180 B]
#6 23.99 Get:238 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocm-openmp-sdk amd64 6.3.0.60300-39~24.04 [872 B]
#6 23.99 Get:239 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocm-opencl amd64 2.0.0.60300-39~24.04 [670 kB]
#6 24.00 Get:240 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocm-opencl-runtime amd64 6.3.0.60300-39~24.04 [2006 B]
#6 24.00 Get:241 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocm-opencl-dev amd64 2.0.0.60300-39~24.04 [121 kB]
#6 24.00 Get:242 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocm-opencl-sdk amd64 6.3.0.60300-39~24.04 [826 B]
#6 24.00 Get:243 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocm-hip-libraries amd64 6.3.0.60300-39~24.04 [942 B]
#6 24.00 Get:244 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocm-ml-libraries amd64 6.3.0.60300-39~24.04 [846 B]
#6 24.01 Get:245 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocrand-dev amd64 3.2.0.60300-39~24.04 [545 kB]
#6 24.01 Get:246 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocsolver-dev amd64 3.27.0.60300-39~24.04 [52.0 kB]
#6 24.01 Get:247 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocsparse-dev amd64 3.3.0.60300-39~24.04 [95.7 kB]
#6 24.01 Get:248 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocthrust-dev amd64 3.3.0.60300-39~24.04 [420 kB]
#6 24.01 Get:249 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocwmma-dev amd64 1.6.0.60300-39~24.04 [70.3 kB]
#6 24.01 Get:250 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocm-hip-sdk amd64 6.3.0.60300-39~24.04 [2194 B]
#6 24.02 Get:251 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocm-ml-sdk amd64 6.3.0.60300-39~24.04 [826 B]
#6 24.02 Get:252 https://repo.radeon.com/rocm/apt/6.3 noble/main amd64 rocm amd64 6.3.0.60300-39~24.04 [2062 B]
#6 24.17 debconf: delaying package configuration, since apt-utils is not installed
#6 24.20 Fetched 2932 MB in 21s (142 MB/s)
#6 24.22 Selecting previously unselected package libargon2-1:amd64.
(Reading database ... 52995 files and directories currently installed.)
#6 24.25 Preparing to unpack .../00-libargon2-1_0~20190702+dfsg-4build1_amd64.deb ...
#6 24.25 Unpacking libargon2-1:amd64 (0~20190702+dfsg-4build1) ...
#6 24.27 Selecting previously unselected package libdevmapper1.02.1:amd64.
#6 24.28 Preparing to unpack .../01-libdevmapper1.02.1_2%3a1.02.185-3ubuntu3.2_amd64.deb ...
#6 24.28 Unpacking libdevmapper1.02.1:amd64 (2:1.02.185-3ubuntu3.2) ...
#6 24.32 Selecting previously unselected package libjson-c5:amd64.
#6 24.32 Preparing to unpack .../02-libjson-c5_0.17-1build1_amd64.deb ...
#6 24.32 Unpacking libjson-c5:amd64 (0.17-1build1) ...
#6 24.35 Selecting previously unselected package libcryptsetup12:amd64.
#6 24.35 Preparing to unpack .../03-libcryptsetup12_2%3a2.7.0-1ubuntu4.2_amd64.deb ...
#6 24.35 Unpacking libcryptsetup12:amd64 (2:2.7.0-1ubuntu4.2) ...
#6 24.38 Selecting previously unselected package libfdisk1:amd64.
#6 24.38 Preparing to unpack .../04-libfdisk1_2.39.3-9ubuntu6.2_amd64.deb ...
#6 24.39 Unpacking libfdisk1:amd64 (2.39.3-9ubuntu6.2) ...
#6 24.41 Selecting previously unselected package libkmod2:amd64.
#6 24.41 Preparing to unpack .../05-libkmod2_31+20240202-2ubuntu7.1_amd64.deb ...
#6 24.42 Unpacking libkmod2:amd64 (31+20240202-2ubuntu7.1) ...
#6 24.44 Selecting previously unselected package libsystemd-shared:amd64.
#6 24.45 Preparing to unpack .../06-libsystemd-shared_255.4-1ubuntu8.6_amd64.deb ...
#6 24.45 Unpacking libsystemd-shared:amd64 (255.4-1ubuntu8.6) ...
#6 24.51 Selecting previously unselected package systemd-dev.
#6 24.52 Preparing to unpack .../07-systemd-dev_255.4-1ubuntu8.6_all.deb ...
#6 24.52 Unpacking systemd-dev (255.4-1ubuntu8.6) ...
#6 24.55 Selecting previously unselected package systemd.
#6 24.56 Preparing to unpack .../08-systemd_255.4-1ubuntu8.6_amd64.deb ...
#6 24.58 Unpacking systemd (255.4-1ubuntu8.6) ...
#6 24.77 Selecting previously unselected package lsb-release.
#6 24.78 Preparing to unpack .../09-lsb-release_12.0-2_all.deb ...
#6 24.78 Unpacking lsb-release (12.0-2) ...
#6 24.80 Selecting previously unselected package kmod.
#6 24.81 Preparing to unpack .../10-kmod_31+20240202-2ubuntu7.1_amd64.deb ...
#6 24.82 Unpacking kmod (31+20240202-2ubuntu7.1) ...
#6 24.86 Setting up lsb-release (12.0-2) ...
#6 24.92 Selecting previously unselected package dkms.
(Reading database ... 54057 files and directories currently installed.)
#6 24.94 Preparing to unpack .../000-dkms_3.0.11-1ubuntu13_all.deb ...
#6 25.02 Unpacking dkms (3.0.11-1ubuntu13) ...
#6 25.05 Selecting previously unselected package libdebuginfod-common.
#6 25.05 Preparing to unpack .../001-libdebuginfod-common_0.190-1.1ubuntu0.1_all.deb ...
#6 25.06 Unpacking libdebuginfod-common (0.190-1.1ubuntu0.1) ...
#6 25.09 Selecting previously unselected package dbus-bin.
#6 25.10 Preparing to unpack .../002-dbus-bin_1.14.10-4ubuntu4.1_amd64.deb ...
#6 25.10 Unpacking dbus-bin (1.14.10-4ubuntu4.1) ...
#6 25.13 Selecting previously unselected package dbus-session-bus-common.
#6 25.13 Preparing to unpack .../003-dbus-session-bus-common_1.14.10-4ubuntu4.1_all.deb ...
#6 25.13 Unpacking dbus-session-bus-common (1.14.10-4ubuntu4.1) ...
#6 25.16 Selecting previously unselected package dbus-daemon.
#6 25.16 Preparing to unpack .../004-dbus-daemon_1.14.10-4ubuntu4.1_amd64.deb ...
#6 25.16 Unpacking dbus-daemon (1.14.10-4ubuntu4.1) ...
#6 25.19 Selecting previously unselected package dbus-system-bus-common.
#6 25.19 Preparing to unpack .../005-dbus-system-bus-common_1.14.10-4ubuntu4.1_all.deb ...
#6 25.20 Unpacking dbus-system-bus-common (1.14.10-4ubuntu4.1) ...
#6 25.22 Selecting previously unselected package dbus.
#6 25.23 Preparing to unpack .../006-dbus_1.14.10-4ubuntu4.1_amd64.deb ...
#6 25.23 Unpacking dbus (1.14.10-4ubuntu4.1) ...
#6 25.26 Selecting previously unselected package dhcpcd-base.
#6 25.26 Preparing to unpack .../007-dhcpcd-base_1%3a10.0.6-1ubuntu3.1_amd64.deb ...
#6 25.26 Unpacking dhcpcd-base (1:10.0.6-1ubuntu3.1) ...
#6 25.31 Selecting previously unselected package dmsetup.
#6 25.31 Preparing to unpack .../008-dmsetup_2%3a1.02.185-3ubuntu3.2_amd64.deb ...
#6 25.31 Unpacking dmsetup (2:1.02.185-3ubuntu3.2) ...
#6 25.33 Selecting previously unselected package gir1.2-glib-2.0:amd64.
#6 25.34 Preparing to unpack .../009-gir1.2-glib-2.0_2.80.0-6ubuntu3.2_amd64.deb ...
#6 25.34 Unpacking gir1.2-glib-2.0:amd64 (2.80.0-6ubuntu3.2) ...
#6 25.36 Selecting previously unselected package libgirepository-1.0-1:amd64.
#6 25.37 Preparing to unpack .../010-libgirepository-1.0-1_1.80.1-1_amd64.deb ...
#6 25.37 Unpacking libgirepository-1.0-1:amd64 (1.80.1-1) ...
#6 25.39 Selecting previously unselected package gir1.2-girepository-2.0:amd64.
#6 25.39 Preparing to unpack .../011-gir1.2-girepository-2.0_1.80.1-1_amd64.deb ...
#6 25.39 Unpacking gir1.2-girepository-2.0:amd64 (1.80.1-1) ...
#6 25.41 Selecting previously unselected package python3-dbus.
#6 25.42 Preparing to unpack .../012-python3-dbus_1.3.2-5build3_amd64.deb ...
#6 25.42 Unpacking python3-dbus (1.3.2-5build3) ...
#6 25.45 Selecting previously unselected package python3-gi.
#6 25.45 Preparing to unpack .../013-python3-gi_3.48.2-1_amd64.deb ...
#6 25.45 Unpacking python3-gi (3.48.2-1) ...
#6 25.50 Selecting previously unselected package networkd-dispatcher.
#6 25.50 Preparing to unpack .../014-networkd-dispatcher_2.2.4-1_all.deb ...
#6 25.51 Unpacking networkd-dispatcher (2.2.4-1) ...
#6 25.53 Selecting previously unselected package python3-pkg-resources.
#6 25.54 Preparing to unpack .../015-python3-pkg-resources_68.1.2-2ubuntu1.1_all.deb ...
#6 25.54 Unpacking python3-pkg-resources (68.1.2-2ubuntu1.1) ...
#6 25.57 Selecting previously unselected package python3-yaml.
#6 25.58 Preparing to unpack .../016-python3-yaml_6.0.1-2build2_amd64.deb ...
#6 25.58 Unpacking python3-yaml (6.0.1-2build2) ...
#6 25.61 Selecting previously unselected package udev.
#6 25.62 Preparing to unpack .../017-udev_255.4-1ubuntu8.6_amd64.deb ...
#6 25.63 Unpacking udev (255.4-1ubuntu8.6) ...
#6 25.71 Selecting previously unselected package systemd-hwe-hwdb.
#6 25.72 Preparing to unpack .../018-systemd-hwe-hwdb_255.1.4_all.deb ...
#6 25.72 Unpacking systemd-hwe-hwdb (255.1.4) ...
#6 25.74 Selecting previously unselected package systemd-resolved.
#6 25.75 Preparing to unpack .../019-systemd-resolved_255.4-1ubuntu8.6_amd64.deb ...
#6 25.75 Unpacking systemd-resolved (255.4-1ubuntu8.6) ...
#6 25.78 Selecting previously unselected package systemd-timesyncd.
#6 25.79 Preparing to unpack .../020-systemd-timesyncd_255.4-1ubuntu8.6_amd64.deb ...
#6 25.79 Unpacking systemd-timesyncd (255.4-1ubuntu8.6) ...
#6 25.81 Selecting previously unselected package cpio.
#6 25.82 Preparing to unpack .../021-cpio_2.15+dfsg-1ubuntu2_amd64.deb ...
#6 25.82 Unpacking cpio (2.15+dfsg-1ubuntu2) ...
#6 25.84 Selecting previously unselected package libmagic-mgc.
#6 25.85 Preparing to unpack .../022-libmagic-mgc_1%3a5.45-3build1_amd64.deb ...
#6 25.85 Unpacking libmagic-mgc (1:5.45-3build1) ...
#6 25.91 Selecting previously unselected package libmagic1t64:amd64.
#6 25.92 Preparing to unpack .../023-libmagic1t64_1%3a5.45-3build1_amd64.deb ...
#6 25.92 Unpacking libmagic1t64:amd64 (1:5.45-3build1) ...
#6 25.94 Selecting previously unselected package file.
#6 25.95 Preparing to unpack .../024-file_1%3a5.45-3build1_amd64.deb ...
#6 25.95 Unpacking file (1:5.45-3build1) ...
#6 25.97 Selecting previously unselected package libgpm2:amd64.
#6 25.98 Preparing to unpack .../025-libgpm2_1.20.7-11_amd64.deb ...
#6 25.98 Unpacking libgpm2:amd64 (1.20.7-11) ...
#6 26.00 Selecting previously unselected package libncurses6:amd64.
#6 26.01 Preparing to unpack .../026-libncurses6_6.4+20240113-1ubuntu2_amd64.deb ...
#6 26.01 Unpacking libncurses6:amd64 (6.4+20240113-1ubuntu2) ...
#6 26.03 Selecting previously unselected package pci.ids.
#6 26.04 Preparing to unpack .../027-pci.ids_0.0~2024.03.31-1ubuntu0.1_all.deb ...
#6 26.04 Unpacking pci.ids (0.0~2024.03.31-1ubuntu0.1) ...
#6 26.07 Selecting previously unselected package libpci3:amd64.
#6 26.07 Preparing to unpack .../028-libpci3_1%3a3.10.0-2build1_amd64.deb ...
#6 26.07 Unpacking libpci3:amd64 (1:3.10.0-2build1) ...
#6 26.11 Selecting previously unselected package pciutils.
#6 26.11 Preparing to unpack .../029-pciutils_1%3a3.10.0-2build1_amd64.deb ...
#6 26.12 Unpacking pciutils (1:3.10.0-2build1) ...
#6 26.14 Selecting previously unselected package python3-setuptools.
#6 26.15 Preparing to unpack .../030-python3-setuptools_68.1.2-2ubuntu1.1_all.deb ...
#6 26.15 Unpacking python3-setuptools (68.1.2-2ubuntu1.1) ...
#6 26.20 Selecting previously unselected package python3-wheel.
#6 26.21 Preparing to unpack .../031-python3-wheel_0.42.0-2_all.deb ...
#6 26.21 Unpacking python3-wheel (0.42.0-2) ...
#6 26.24 Selecting previously unselected package python3-pip.
#6 26.25 Preparing to unpack .../032-python3-pip_24.0+dfsg-1ubuntu1.1_all.deb ...
#6 26.25 Unpacking python3-pip (24.0+dfsg-1ubuntu1.1) ...
#6 26.37 Selecting previously unselected package rocm-core.
#6 26.38 Preparing to unpack .../033-rocm-core_6.3.0.60300-39~24.04_amd64.deb ...
#6 26.38 Unpacking rocm-core (6.3.0.60300-39~24.04) ...
#6 26.40 Selecting previously unselected package amd-smi-lib.
#6 26.41 Preparing to unpack .../034-amd-smi-lib_24.7.1.60300-39~24.04_amd64.deb ...
#6 26.41 Unpacking amd-smi-lib (24.7.1.60300-39~24.04) ...
#6 26.45 Selecting previously unselected package amdgpu-core.
#6 26.46 Preparing to unpack .../035-amdgpu-core_1%3a6.3.60300-2084815.24.04_all.deb ...
#6 26.46 Unpacking amdgpu-core (1:6.3.60300-2084815.24.04) ...
#6 26.50 Selecting previously unselected package m4.
#6 26.50 Preparing to unpack .../036-m4_1.4.19-4build1_amd64.deb ...
#6 26.50 Unpacking m4 (1.4.19-4build1) ...
#6 26.53 Selecting previously unselected package autoconf.
#6 26.54 Preparing to unpack .../037-autoconf_2.71-3_all.deb ...
#6 26.54 Unpacking autoconf (2.71-3) ...
#6 26.58 Selecting previously unselected package autotools-dev.
#6 26.58 Preparing to unpack .../038-autotools-dev_20220109.1_all.deb ...
#6 26.58 Unpacking autotools-dev (20220109.1) ...
#6 26.61 Selecting previously unselected package automake.
#6 26.62 Preparing to unpack .../039-automake_1%3a1.16.5-1.3ubuntu1_all.deb ...
#6 26.62 Unpacking automake (1:1.16.5-1.3ubuntu1) ...
#6 26.66 Selecting previously unselected package busybox-initramfs.
#6 26.67 Preparing to unpack .../040-busybox-initramfs_1%3a1.36.1-6ubuntu3.1_amd64.deb ...
#6 26.69 Unpacking busybox-initramfs (1:1.36.1-6ubuntu3.1) ...
#6 26.71 Selecting previously unselected package dracut-install.
#6 26.71 Preparing to unpack .../041-dracut-install_060+5-1ubuntu3.3_amd64.deb ...
#6 26.72 Unpacking dracut-install (060+5-1ubuntu3.3) ...
#6 26.74 Selecting previously unselected package initramfs-tools-bin.
#6 26.74 Preparing to unpack .../042-initramfs-tools-bin_0.142ubuntu25.5_amd64.deb ...
#6 26.74 Unpacking initramfs-tools-bin (0.142ubuntu25.5) ...
#6 26.76 Selecting previously unselected package libklibc:amd64.
#6 26.77 Preparing to unpack .../043-libklibc_2.0.13-4ubuntu0.1_amd64.deb ...
#6 26.77 Unpacking libklibc:amd64 (2.0.13-4ubuntu0.1) ...
#6 26.79 Selecting previously unselected package klibc-utils.
#6 26.80 Preparing to unpack .../044-klibc-utils_2.0.13-4ubuntu0.1_amd64.deb ...
#6 26.80 Unpacking klibc-utils (2.0.13-4ubuntu0.1) ...
#6 26.83 Selecting previously unselected package initramfs-tools-core.
#6 26.84 Preparing to unpack .../045-initramfs-tools-core_0.142ubuntu25.5_all.deb ...
#6 26.84 Unpacking initramfs-tools-core (0.142ubuntu25.5) ...
#6 26.87 Selecting previously unselected package linux-base.
#6 26.87 Preparing to unpack .../046-linux-base_4.5ubuntu9+24.04.1_all.deb ...
#6 26.89 Unpacking linux-base (4.5ubuntu9+24.04.1) ...
#6 26.92 Selecting previously unselected package initramfs-tools.
#6 26.93 Preparing to unpack .../047-initramfs-tools_0.142ubuntu25.5_all.deb ...
#6 26.94 Unpacking initramfs-tools (0.142ubuntu25.5) ...
#6 26.96 Selecting previously unselected package amdgpu-dkms-firmware.
#6 26.97 Preparing to unpack .../048-amdgpu-dkms-firmware_1%3a6.10.5.60300-2084815.24.04_all.deb ...
#6 26.97 Unpacking amdgpu-dkms-firmware (1:6.10.5.60300-2084815.24.04) ...
#6 27.51 Selecting previously unselected package amdgpu-dkms.
#6 27.52 Preparing to unpack .../049-amdgpu-dkms_1%3a6.10.5.60300-2084815.24.04_all.deb ...
#6 27.52 Unpacking amdgpu-dkms (1:6.10.5.60300-2084815.24.04) ...
#6 29.31 Selecting previously unselected package libncurses-dev:amd64.
#6 29.33 Preparing to unpack .../050-libncurses-dev_6.4+20240113-1ubuntu2_amd64.deb ...
#6 29.33 Unpacking libncurses-dev:amd64 (6.4+20240113-1ubuntu2) ...
#6 29.37 Selecting previously unselected package comgr.
#6 29.38 Preparing to unpack .../051-comgr_2.8.0.60300-39~24.04_amd64.deb ...
#6 29.38 Unpacking comgr (2.8.0.60300-39~24.04) ...
#6 29.97 Selecting previously unselected package composablekernel-dev.
#6 29.97 Preparing to unpack .../052-composablekernel-dev_1.1.0.60300-39~24.04_amd64.deb ...
#6 29.97 Unpacking composablekernel-dev (1.1.0.60300-39~24.04) ...
#6 35.88 Selecting previously unselected package libfakeroot:amd64.
#6 35.88 Preparing to unpack .../053-libfakeroot_1.33-1_amd64.deb ...
#6 35.88 Unpacking libfakeroot:amd64 (1.33-1) ...
#6 35.91 Selecting previously unselected package fakeroot.
#6 35.91 Preparing to unpack .../054-fakeroot_1.33-1_amd64.deb ...
#6 35.91 Unpacking fakeroot (1.33-1) ...
#6 35.94 Selecting previously unselected package libc6-i386.
#6 35.95 Preparing to unpack .../055-libc6-i386_2.39-0ubuntu8.4_amd64.deb ...
#6 35.95 Unpacking libc6-i386 (2.39-0ubuntu8.4) ...
#6 36.06 Selecting previously unselected package libc6-dev-i386.
#6 36.07 Preparing to unpack .../056-libc6-dev-i386_2.39-0ubuntu8.4_amd64.deb ...
#6 36.07 Unpacking libc6-dev-i386 (2.39-0ubuntu8.4) ...
#6 36.15 Selecting previously unselected package libc6-x32.
#6 36.16 Preparing to unpack .../057-libc6-x32_2.39-0ubuntu8.4_amd64.deb ...
#6 36.16 Unpacking libc6-x32 (2.39-0ubuntu8.4) ...
#6 36.27 Selecting previously unselected package libc6-dev-x32.
#6 36.28 Preparing to unpack .../058-libc6-dev-x32_2.39-0ubuntu8.4_amd64.deb ...
#6 36.28 Unpacking libc6-dev-x32 (2.39-0ubuntu8.4) ...
#6 36.34 Selecting previously unselected package lib32gcc-s1.
#6 36.35 Preparing to unpack .../059-lib32gcc-s1_14.2.0-4ubuntu2~24.04_amd64.deb ...
#6 36.35 Unpacking lib32gcc-s1 (14.2.0-4ubuntu2~24.04) ...
#6 36.38 Selecting previously unselected package libx32gcc-s1.
#6 36.38 Preparing to unpack .../060-libx32gcc-s1_14.2.0-4ubuntu2~24.04_amd64.deb ...
#6 36.39 Unpacking libx32gcc-s1 (14.2.0-4ubuntu2~24.04) ...
#6 36.41 Selecting previously unselected package lib32gomp1.
#6 36.41 Preparing to unpack .../061-lib32gomp1_14.2.0-4ubuntu2~24.04_amd64.deb ...
#6 36.41 Unpacking lib32gomp1 (14.2.0-4ubuntu2~24.04) ...
#6 36.45 Selecting previously unselected package libx32gomp1.
#6 36.46 Preparing to unpack .../062-libx32gomp1_14.2.0-4ubuntu2~24.04_amd64.deb ...
#6 36.46 Unpacking libx32gomp1 (14.2.0-4ubuntu2~24.04) ...
#6 36.48 Selecting previously unselected package lib32itm1.
#6 36.49 Preparing to unpack .../063-lib32itm1_14.2.0-4ubuntu2~24.04_amd64.deb ...
#6 36.49 Unpacking lib32itm1 (14.2.0-4ubuntu2~24.04) ...
#6 36.51 Selecting previously unselected package libx32itm1.
#6 36.51 Preparing to unpack .../064-libx32itm1_14.2.0-4ubuntu2~24.04_amd64.deb ...
#6 36.51 Unpacking libx32itm1 (14.2.0-4ubuntu2~24.04) ...
#6 36.54 Selecting previously unselected package lib32atomic1.
#6 36.54 Preparing to unpack .../065-lib32atomic1_14.2.0-4ubuntu2~24.04_amd64.deb ...
#6 36.54 Unpacking lib32atomic1 (14.2.0-4ubuntu2~24.04) ...
#6 36.57 Selecting previously unselected package libx32atomic1.
#6 36.57 Preparing to unpack .../066-libx32atomic1_14.2.0-4ubuntu2~24.04_amd64.deb ...
#6 36.57 Unpacking libx32atomic1 (14.2.0-4ubuntu2~24.04) ...
#6 36.59 Selecting previously unselected package lib32asan8.
#6 36.60 Preparing to unpack .../067-lib32asan8_14.2.0-4ubuntu2~24.04_amd64.deb ...
#6 36.60 Unpacking lib32asan8 (14.2.0-4ubuntu2~24.04) ...
#6 36.66 Selecting previously unselected package libx32asan8.
#6 36.66 Preparing to unpack .../068-libx32asan8_14.2.0-4ubuntu2~24.04_amd64.deb ...
#6 36.66 Unpacking libx32asan8 (14.2.0-4ubuntu2~24.04) ...
#6 36.73 Selecting previously unselected package lib32stdc++6.
#6 36.73 Preparing to unpack .../069-lib32stdc++6_14.2.0-4ubuntu2~24.04_amd64.deb ...
#6 36.73 Unpacking lib32stdc++6 (14.2.0-4ubuntu2~24.04) ...
#6 36.77 Selecting previously unselected package lib32ubsan1.
#6 36.77 Preparing to unpack .../070-lib32ubsan1_14.2.0-4ubuntu2~24.04_amd64.deb ...
#6 36.77 Unpacking lib32ubsan1 (14.2.0-4ubuntu2~24.04) ...
#6 36.81 Selecting previously unselected package libx32stdc++6.
#6 36.82 Preparing to unpack .../071-libx32stdc++6_14.2.0-4ubuntu2~24.04_amd64.deb ...
#6 36.82 Unpacking libx32stdc++6 (14.2.0-4ubuntu2~24.04) ...
#6 36.86 Selecting previously unselected package libx32ubsan1.
#6 36.87 Preparing to unpack .../072-libx32ubsan1_14.2.0-4ubuntu2~24.04_amd64.deb ...
#6 36.87 Unpacking libx32ubsan1 (14.2.0-4ubuntu2~24.04) ...
#6 36.91 Selecting previously unselected package lib32quadmath0.
#6 36.92 Preparing to unpack .../073-lib32quadmath0_14.2.0-4ubuntu2~24.04_amd64.deb ...
#6 36.92 Unpacking lib32quadmath0 (14.2.0-4ubuntu2~24.04) ...
#6 36.95 Selecting previously unselected package libx32quadmath0.
#6 36.96 Preparing to unpack .../074-libx32quadmath0_14.2.0-4ubuntu2~24.04_amd64.deb ...
#6 36.96 Unpacking libx32quadmath0 (14.2.0-4ubuntu2~24.04) ...
#6 36.99 Selecting previously unselected package lib32gcc-13-dev.
#6 36.99 Preparing to unpack .../075-lib32gcc-13-dev_13.3.0-6ubuntu2~24.04_amd64.deb ...
#6 37.00 Unpacking lib32gcc-13-dev (13.3.0-6ubuntu2~24.04) ...
#6 37.06 Selecting previously unselected package libx32gcc-13-dev.
#6 37.07 Preparing to unpack .../076-libx32gcc-13-dev_13.3.0-6ubuntu2~24.04_amd64.deb ...
#6 37.07 Unpacking libx32gcc-13-dev (13.3.0-6ubuntu2~24.04) ...
#6 37.12 Selecting previously unselected package gcc-13-multilib.
#6 37.13 Preparing to unpack .../077-gcc-13-multilib_13.3.0-6ubuntu2~24.04_amd64.deb ...
#6 37.14 Unpacking gcc-13-multilib (13.3.0-6ubuntu2~24.04) ...
#6 37.16 Selecting previously unselected package lib32stdc++-13-dev.
#6 37.17 Preparing to unpack .../078-lib32stdc++-13-dev_13.3.0-6ubuntu2~24.04_amd64.deb ...
#6 37.17 Unpacking lib32stdc++-13-dev (13.3.0-6ubuntu2~24.04) ...
#6 37.24 Selecting previously unselected package libx32stdc++-13-dev.
#6 37.25 Preparing to unpack .../079-libx32stdc++-13-dev_13.3.0-6ubuntu2~24.04_amd64.deb ...
#6 37.25 Unpacking libx32stdc++-13-dev (13.3.0-6ubuntu2~24.04) ...
#6 37.30 Selecting previously unselected package g++-13-multilib.
#6 37.31 Preparing to unpack .../080-g++-13-multilib_13.3.0-6ubuntu2~24.04_amd64.deb ...
#6 37.31 Unpacking g++-13-multilib (13.3.0-6ubuntu2~24.04) ...
#6 37.34 Selecting previously unselected package gcc-multilib.
#6 37.35 Preparing to unpack .../081-gcc-multilib_4%3a13.2.0-7ubuntu1_amd64.deb ...
#6 37.35 Unpacking gcc-multilib (4:13.2.0-7ubuntu1) ...
#6 37.37 Selecting previously unselected package g++-multilib.
#6 37.38 Preparing to unpack .../082-g++-multilib_4%3a13.2.0-7ubuntu1_amd64.deb ...
#6 37.38 Unpacking g++-multilib (4:13.2.0-7ubuntu1) ...
#6 37.40 Selecting previously unselected package gcc-11-base:amd64.
#6 37.41 Preparing to unpack .../083-gcc-11-base_11.4.0-9ubuntu1_amd64.deb ...
#6 37.41 Unpacking gcc-11-base:amd64 (11.4.0-9ubuntu1) ...
#6 37.47 Selecting previously unselected package libdw1t64:amd64.
#6 37.48 Preparing to unpack .../084-libdw1t64_0.190-1.1ubuntu0.1_amd64.deb ...
#6 37.48 Unpacking libdw1t64:amd64 (0.190-1.1ubuntu0.1) ...
#6 37.50 Selecting previously unselected package libbabeltrace1:amd64.
#6 37.51 Preparing to unpack .../085-libbabeltrace1_1.5.11-3build3_amd64.deb ...
#6 37.51 Unpacking libbabeltrace1:amd64 (1.5.11-3build3) ...
#6 37.54 Selecting previously unselected package libdebuginfod1t64:amd64.
#6 37.54 Preparing to unpack .../086-libdebuginfod1t64_0.190-1.1ubuntu0.1_amd64.deb ...
#6 37.54 Unpacking libdebuginfod1t64:amd64 (0.190-1.1ubuntu0.1) ...
#6 37.57 Selecting previously unselected package libipt2.
#6 37.58 Preparing to unpack .../087-libipt2_2.0.6-1build1_amd64.deb ...
#6 37.58 Unpacking libipt2 (2.0.6-1build1) ...
#6 37.60 Selecting previously unselected package libpython3.12t64:amd64.
#6 37.61 Preparing to unpack .../088-libpython3.12t64_3.12.3-1ubuntu0.5_amd64.deb ...
#6 37.63 Unpacking libpython3.12t64:amd64 (3.12.3-1ubuntu0.5) ...
#6 37.69 Selecting previously unselected package libsource-highlight-common.
#6 37.70 Preparing to unpack .../089-libsource-highlight-common_3.1.9-4.3build1_all.deb ...
#6 37.70 Unpacking libsource-highlight-common (3.1.9-4.3build1) ...
#6 37.75 Selecting previously unselected package libsource-highlight4t64:amd64.
#6 37.76 Preparing to unpack .../090-libsource-highlight4t64_3.1.9-4.3build1_amd64.deb ...
#6 37.76 Unpacking libsource-highlight4t64:amd64 (3.1.9-4.3build1) ...
#6 37.79 Selecting previously unselected package gdb.
#6 37.80 Preparing to unpack .../091-gdb_15.0.50.20240403-0ubuntu1_amd64.deb ...
#6 37.80 Unpacking gdb (15.0.50.20240403-0ubuntu1) ...
#6 37.88 Selecting previously unselected package half.
#6 37.89 Preparing to unpack .../092-half_1.12.0.60300-39~24.04_amd64.deb ...
#6 37.89 Unpacking half (1.12.0.60300-39~24.04) ...
#6 37.92 Selecting previously unselected package libfile-copy-recursive-perl.
#6 37.93 Preparing to unpack .../093-libfile-copy-recursive-perl_0.45-4_all.deb ...
#6 37.93 Unpacking libfile-copy-recursive-perl (0.45-4) ...
#6 37.95 Selecting previously unselected package libtimedate-perl.
#6 37.96 Preparing to unpack .../094-libtimedate-perl_2.3300-2_all.deb ...
#6 37.96 Unpacking libtimedate-perl (2.3300-2) ...
#6 37.99 Selecting previously unselected package libhttp-date-perl.
#6 38.00 Preparing to unpack .../095-libhttp-date-perl_6.06-1_all.deb ...
#6 38.00 Unpacking libhttp-date-perl (6.06-1) ...
#6 38.04 Selecting previously unselected package libfile-listing-perl.
#6 38.05 Preparing to unpack .../096-libfile-listing-perl_6.16-1_all.deb ...
#6 38.05 Unpacking libfile-listing-perl (6.16-1) ...
#6 38.08 Selecting previously unselected package libfile-which-perl.
#6 38.09 Preparing to unpack .../097-libfile-which-perl_1.27-2_all.deb ...
#6 38.09 Unpacking libfile-which-perl (1.27-2) ...
#6 38.11 Selecting previously unselected package liburi-perl.
#6 38.12 Preparing to unpack .../098-liburi-perl_5.27-1_all.deb ...
#6 38.12 Unpacking liburi-perl (5.27-1) ...
#6 38.16 Selecting previously unselected package libdrm2-amdgpu:amd64.
#6 38.16 Preparing to unpack .../099-libdrm2-amdgpu_1%3a2.4.123.60300-2084815.24.04_amd64.deb ...
#6 38.17 Unpacking libdrm2-amdgpu:amd64 (1:2.4.123.60300-2084815.24.04) ...
#6 38.19 Selecting previously unselected package libdrm-amdgpu-common.
#6 38.20 Preparing to unpack .../100-libdrm-amdgpu-common_1.0.0.60300-2084815.24.04_all.deb ...
#6 38.20 Unpacking libdrm-amdgpu-common (1.0.0.60300-2084815.24.04) ...
#6 38.24 Selecting previously unselected package libdrm-amdgpu-amdgpu1:amd64.
#6 38.25 Preparing to unpack .../101-libdrm-amdgpu-amdgpu1_1%3a2.4.123.60300-2084815.24.04_amd64.deb ...
#6 38.25 Unpacking libdrm-amdgpu-amdgpu1:amd64 (1:2.4.123.60300-2084815.24.04) ...
#6 38.28 Selecting previously unselected package rocprofiler-register.
#6 38.29 Preparing to unpack .../102-rocprofiler-register_0.4.0.60300-39~24.04_amd64.deb ...
#6 38.29 Unpacking rocprofiler-register (0.4.0.60300-39~24.04) ...
#6 38.32 Selecting previously unselected package hsa-rocr.
#6 38.33 Preparing to unpack .../103-hsa-rocr_1.14.0.60300-39~24.04_amd64.deb ...
#6 38.33 Pre-install check for ROCr.
#6 38.34 Unpacking hsa-rocr (1.14.0.60300-39~24.04) ...
#6 38.38 Selecting previously unselected package rocminfo.
#6 38.39 Preparing to unpack .../104-rocminfo_1.0.0.60300-39~24.04_amd64.deb ...
#6 38.39 Unpacking rocminfo (1.0.0.60300-39~24.04) ...
#6 38.43 Selecting previously unselected package hip-runtime-amd.
#6 38.44 Preparing to unpack .../105-hip-runtime-amd_6.3.42131.60300-39~24.04_amd64.deb ...
#6 38.44 Unpacking hip-runtime-amd (6.3.42131.60300-39~24.04) ...
#6 38.56 Selecting previously unselected package libasan6:amd64.
#6 38.57 Preparing to unpack .../106-libasan6_11.4.0-9ubuntu1_amd64.deb ...
#6 38.57 Unpacking libasan6:amd64 (11.4.0-9ubuntu1) ...
#6 38.65 Selecting previously unselected package libtsan0:amd64.
#6 38.65 Preparing to unpack .../107-libtsan0_11.4.0-9ubuntu1_amd64.deb ...
#6 38.66 Unpacking libtsan0:amd64 (11.4.0-9ubuntu1) ...
#6 38.71 Selecting previously unselected package libgcc-11-dev:amd64.
#6 38.71 Preparing to unpack .../108-libgcc-11-dev_11.4.0-9ubuntu1_amd64.deb ...
#6 38.71 Unpacking libgcc-11-dev:amd64 (11.4.0-9ubuntu1) ...
#6 38.80 Selecting previously unselected package libstdc++-11-dev:amd64.
#6 38.81 Preparing to unpack .../109-libstdc++-11-dev_11.4.0-9ubuntu1_amd64.deb ...
#6 38.83 Unpacking libstdc++-11-dev:amd64 (11.4.0-9ubuntu1) ...
#6 39.03 Selecting previously unselected package rocm-llvm.
#6 39.04 Preparing to unpack .../110-rocm-llvm_18.0.0.24455.60300-39~24.04_amd64.deb ...
#6 39.04 Unpacking rocm-llvm (18.0.0.24455.60300-39~24.04) ...
#6 42.95 Selecting previously unselected package libdrm-amdgpu-radeon1:amd64.
#6 42.96 Preparing to unpack .../111-libdrm-amdgpu-radeon1_1%3a2.4.123.60300-2084815.24.04_amd64.deb ...
#6 42.96 Unpacking libdrm-amdgpu-radeon1:amd64 (1:2.4.123.60300-2084815.24.04) ...
#6 42.99 Selecting previously unselected package libc6-dbg:amd64.
#6 42.99 Preparing to unpack .../112-libc6-dbg_2.39-0ubuntu8.4_amd64.deb ...
#6 42.99 Unpacking libc6-dbg:amd64 (2.39-0ubuntu8.4) ...
#6 43.11 Selecting previously unselected package valgrind.
#6 43.12 Preparing to unpack .../113-valgrind_1%3a3.22.0-0ubuntu3_amd64.deb ...
#6 43.12 Unpacking valgrind (1:3.22.0-0ubuntu3) ...
#6 43.39 Selecting previously unselected package libdrm-amdgpu-dev:amd64.
#6 43.39 Preparing to unpack .../114-libdrm-amdgpu-dev_1%3a2.4.123.60300-2084815.24.04_amd64.deb ...
#6 43.39 Unpacking libdrm-amdgpu-dev:amd64 (1:2.4.123.60300-2084815.24.04) ...
#6 43.43 Selecting previously unselected package libdrm-nouveau2:amd64.
#6 43.44 Preparing to unpack .../115-libdrm-nouveau2_2.4.122-1~ubuntu0.24.04.1_amd64.deb ...
#6 43.44 Unpacking libdrm-nouveau2:amd64 (2.4.122-1~ubuntu0.24.04.1) ...
#6 43.46 Selecting previously unselected package libpciaccess-dev:amd64.
#6 43.47 Preparing to unpack .../116-libpciaccess-dev_0.17-3build1_amd64.deb ...
#6 43.47 Unpacking libpciaccess-dev:amd64 (0.17-3build1) ...
#6 43.49 Selecting previously unselected package libdrm-dev:amd64.
#6 43.50 Preparing to unpack .../117-libdrm-dev_2.4.122-1~ubuntu0.24.04.1_amd64.deb ...
#6 43.50 Unpacking libdrm-dev:amd64 (2.4.122-1~ubuntu0.24.04.1) ...
#6 43.53 Selecting previously unselected package hsa-rocr-dev.
#6 43.54 Preparing to unpack .../118-hsa-rocr-dev_1.14.0.60300-39~24.04_amd64.deb ...
#6 43.54 Unpacking hsa-rocr-dev (1.14.0.60300-39~24.04) ...
#6 43.57 Selecting previously unselected package hip-dev.
#6 43.57 Preparing to unpack .../119-hip-dev_6.3.42131.60300-39~24.04_amd64.deb ...
#6 43.58 Unpacking hip-dev (6.3.42131.60300-39~24.04) ...
#6 43.63 Selecting previously unselected package hip-doc.
#6 43.64 Preparing to unpack .../120-hip-doc_6.3.42131.60300-39~24.04_amd64.deb ...
#6 43.64 Unpacking hip-doc (6.3.42131.60300-39~24.04) ...
#6 43.66 Selecting previously unselected package hipcc.
#6 43.67 Preparing to unpack .../121-hipcc_1.1.1.60300-39~24.04_amd64.deb ...
#6 43.67 Unpacking hipcc (1.1.1.60300-39~24.04) ...
#6 43.69 Selecting previously unselected package hip-samples.
#6 43.70 Preparing to unpack .../122-hip-samples_6.3.42131.60300-39~24.04_amd64.deb ...
#6 43.70 Unpacking hip-samples (6.3.42131.60300-39~24.04) ...
#6 43.74 Selecting previously unselected package hipblaslt.
#6 43.75 Preparing to unpack .../123-hipblaslt_0.10.0.60300-39~24.04_amd64.deb ...
#6 43.75 Unpacking hipblaslt (0.10.0.60300-39~24.04) ...
#6 71.38 Selecting previously unselected package rocblas.
#6 71.39 Preparing to unpack .../124-rocblas_4.3.0.60300-39~24.04_amd64.deb ...
#6 71.39 Unpacking rocblas (4.3.0.60300-39~24.04) ...
#6 81.68 Selecting previously unselected package rocsolver.
#6 81.69 Preparing to unpack .../125-rocsolver_3.27.0.60300-39~24.04_amd64.deb ...
#6 81.72 Unpacking rocsolver (3.27.0.60300-39~24.04) ...
#6 86.30 Selecting previously unselected package hipblas.
#6 86.31 Preparing to unpack .../126-hipblas_2.3.0.60300-39~24.04_amd64.deb ...
#6 86.34 Unpacking hipblas (2.3.0.60300-39~24.04) ...
#6 86.55 Selecting previously unselected package hipblas-common-dev.
#6 86.56 Preparing to unpack .../127-hipblas-common-dev_1.0.0.60300-39~24.04_amd64.deb ...
#6 86.62 Unpacking hipblas-common-dev (1.0.0.60300-39~24.04) ...
#6 86.83 Selecting previously unselected package hipblas-dev.
#6 86.84 Preparing to unpack .../128-hipblas-dev_2.3.0.60300-39~24.04_amd64.deb ...
#6 86.87 Unpacking hipblas-dev (2.3.0.60300-39~24.04) ...
#6 87.11 Selecting previously unselected package hipblaslt-dev.
#6 87.12 Preparing to unpack .../129-hipblaslt-dev_0.10.0.60300-39~24.04_amd64.deb ...
#6 87.15 Unpacking hipblaslt-dev (0.10.0.60300-39~24.04) ...
#6 87.26 Selecting previously unselected package rocprim-dev.
#6 87.26 Preparing to unpack .../130-rocprim-dev_3.3.0.60300-39~24.04_amd64.deb ...
#6 87.29 Unpacking rocprim-dev (3.3.0.60300-39~24.04) ...
#6 87.57 Selecting previously unselected package hipcub-dev.
#6 87.58 Preparing to unpack .../131-hipcub-dev_3.3.0.60300-39~24.04_amd64.deb ...
#6 87.61 Unpacking hipcub-dev (3.3.0.60300-39~24.04) ...
#6 87.78 Selecting previously unselected package rocfft.
#6 87.79 Preparing to unpack .../132-rocfft_1.0.31.60300-39~24.04_amd64.deb ...
#6 87.82 Unpacking rocfft (1.0.31.60300-39~24.04) ...
#6 94.83 Selecting previously unselected package hipfft.
#6 94.84 Preparing to unpack .../133-hipfft_1.0.17.60300-39~24.04_amd64.deb ...
#6 94.88 Unpacking hipfft (1.0.17.60300-39~24.04) ...
#6 95.08 Selecting previously unselected package hipfft-dev.
#6 95.09 Preparing to unpack .../134-hipfft-dev_1.0.17.60300-39~24.04_amd64.deb ...
#6 95.11 Unpacking hipfft-dev (1.0.17.60300-39~24.04) ...
#6 95.29 Selecting previously unselected package hipfort-dev.
#6 95.30 Preparing to unpack .../135-hipfort-dev_0.5.0.60300-39~24.04_amd64.deb ...
#6 95.34 Unpacking hipfort-dev (0.5.0.60300-39~24.04) ...
#6 95.86 Selecting previously unselected package hipify-clang.
#6 95.88 Preparing to unpack .../136-hipify-clang_18.0.0.60300-39~24.04_amd64.deb ...
#6 95.92 Unpacking hipify-clang (18.0.0.60300-39~24.04) ...
#6 96.36 Selecting previously unselected package hiprand.
#6 96.37 Preparing to unpack .../137-hiprand_2.11.0.60300-39~24.04_amd64.deb ...
#6 96.41 Unpacking hiprand (2.11.0.60300-39~24.04) ...
#6 96.57 Selecting previously unselected package hiprand-dev.
#6 96.58 Preparing to unpack .../138-hiprand-dev_2.11.0.60300-39~24.04_amd64.deb ...
#6 96.62 Unpacking hiprand-dev (2.11.0.60300-39~24.04) ...
#6 96.77 Selecting previously unselected package hipsolver.
#6 96.77 Preparing to unpack .../139-hipsolver_2.3.0.60300-39~24.04_amd64.deb ...
#6 96.82 Unpacking hipsolver (2.3.0.60300-39~24.04) ...
#6 97.08 Selecting previously unselected package hipsolver-dev.
#6 97.09 Preparing to unpack .../140-hipsolver-dev_2.3.0.60300-39~24.04_amd64.deb ...
#6 97.14 Unpacking hipsolver-dev (2.3.0.60300-39~24.04) ...
#6 97.33 Selecting previously unselected package rocsparse.
#6 97.34 Preparing to unpack .../141-rocsparse_3.3.0.60300-39~24.04_amd64.deb ...
#6 97.37 Unpacking rocsparse (3.3.0.60300-39~24.04) ...
#6 101.2 Selecting previously unselected package hipsparse.
#6 101.2 Preparing to unpack .../142-hipsparse_3.1.2.60300-39~24.04_amd64.deb ...
#6 101.3 Unpacking hipsparse (3.1.2.60300-39~24.04) ...
#6 101.5 Selecting previously unselected package hipsparse-dev.
#6 101.5 Preparing to unpack .../143-hipsparse-dev_3.1.2.60300-39~24.04_amd64.deb ...
#6 101.5 Unpacking hipsparse-dev (3.1.2.60300-39~24.04) ...
#6 101.7 Selecting previously unselected package hipsparselt.
#6 101.8 Preparing to unpack .../144-hipsparselt_0.2.2.60300-39~24.04_amd64.deb ...
#6 101.8 Unpacking hipsparselt (0.2.2.60300-39~24.04) ...
#6 103.0 Selecting previously unselected package hipsparselt-dev.
#6 103.0 Preparing to unpack .../145-hipsparselt-dev_0.2.2.60300-39~24.04_amd64.deb ...
#6 103.1 Unpacking hipsparselt-dev (0.2.2.60300-39~24.04) ...
#6 103.2 Selecting previously unselected package hiptensor.
#6 103.2 Preparing to unpack .../146-hiptensor_1.4.0.60300-39~24.04_amd64.deb ...
#6 103.3 Unpacking hiptensor (1.4.0.60300-39~24.04) ...
#6 104.5 Selecting previously unselected package hiptensor-dev.
#6 104.6 Preparing to unpack .../147-hiptensor-dev_1.4.0.60300-39~24.04_amd64.deb ...
#6 104.6 Unpacking hiptensor-dev (1.4.0.60300-39~24.04) ...
#6 104.7 Selecting previously unselected package hsa-amd-aqlprofile.
#6 104.7 Preparing to unpack .../148-hsa-amd-aqlprofile_1.0.0.60300-39~24.04_amd64.deb ...
#6 104.7 Unpacking hsa-amd-aqlprofile (1.0.0.60300-39~24.04) ...
#6 104.9 Selecting previously unselected package icu-devtools.
#6 104.9 Preparing to unpack .../149-icu-devtools_74.2-1ubuntu3.1_amd64.deb ...
#6 105.0 Unpacking icu-devtools (74.2-1ubuntu3.1) ...
#6 105.2 Selecting previously unselected package javascript-common.
#6 105.2 Preparing to unpack .../150-javascript-common_11+nmu1_all.deb ...
#6 105.3 Unpacking javascript-common (11+nmu1) ...
#6 105.5 Selecting previously unselected package libsuitesparseconfig7:amd64.
#6 105.5 Preparing to unpack .../151-libsuitesparseconfig7_1%3a7.6.1+dfsg-1build1_amd64.deb ...
#6 105.5 Unpacking libsuitesparseconfig7:amd64 (1:7.6.1+dfsg-1build1) ...
#6 105.7 Selecting previously unselected package libamd3:amd64.
#6 105.7 Preparing to unpack .../152-libamd3_1%3a7.6.1+dfsg-1build1_amd64.deb ...
#6 105.7 Unpacking libamd3:amd64 (1:7.6.1+dfsg-1build1) ...
#6 105.8 Selecting previously unselected package libavutil-dev:amd64.
#6 105.9 Preparing to unpack .../153-libavutil-dev_7%3a6.1.1-3ubuntu5_amd64.deb ...
#6 105.9 Unpacking libavutil-dev:amd64 (7:6.1.1-3ubuntu5) ...
#6 106.1 Selecting previously unselected package libswresample-dev:amd64.
#6 106.1 Preparing to unpack .../154-libswresample-dev_7%3a6.1.1-3ubuntu5_amd64.deb ...
#6 106.1 Unpacking libswresample-dev:amd64 (7:6.1.1-3ubuntu5) ...
#6 106.3 Selecting previously unselected package libavcodec-dev:amd64.
#6 106.3 Preparing to unpack .../155-libavcodec-dev_7%3a6.1.1-3ubuntu5_amd64.deb ...
#6 106.3 Unpacking libavcodec-dev:amd64 (7:6.1.1-3ubuntu5) ...
#6 106.6 Selecting previously unselected package libavformat-dev:amd64.
#6 106.6 Preparing to unpack .../156-libavformat-dev_7%3a6.1.1-3ubuntu5_amd64.deb ...
#6 106.6 Unpacking libavformat-dev:amd64 (7:6.1.1-3ubuntu5) ...
#6 106.8 Selecting previously unselected package libcamd3:amd64.
#6 106.8 Preparing to unpack .../157-libcamd3_1%3a7.6.1+dfsg-1build1_amd64.deb ...
#6 106.9 Unpacking libcamd3:amd64 (1:7.6.1+dfsg-1build1) ...
#6 107.1 Selecting previously unselected package libccolamd3:amd64.
#6 107.1 Preparing to unpack .../158-libccolamd3_1%3a7.6.1+dfsg-1build1_amd64.deb ...
#6 107.1 Unpacking libccolamd3:amd64 (1:7.6.1+dfsg-1build1) ...
#6 107.3 Selecting previously unselected package libcolamd3:amd64.
#6 107.3 Preparing to unpack .../159-libcolamd3_1%3a7.6.1+dfsg-1build1_amd64.deb ...
#6 107.3 Unpacking libcolamd3:amd64 (1:7.6.1+dfsg-1build1) ...
#6 107.5 Selecting previously unselected package libcholmod5:amd64.
#6 107.5 Preparing to unpack .../160-libcholmod5_1%3a7.6.1+dfsg-1build1_amd64.deb ...
#6 107.5 Unpacking libcholmod5:amd64 (1:7.6.1+dfsg-1build1) ...
#6 107.7 Selecting previously unselected package zlib1g-dev:amd64.
#6 107.7 Preparing to unpack .../161-zlib1g-dev_1%3a1.3.dfsg-3.1ubuntu2.1_amd64.deb ...
#6 107.7 Unpacking zlib1g-dev:amd64 (1:1.3.dfsg-3.1ubuntu2.1) ...
#6 107.9 Selecting previously unselected package libzstd-dev:amd64.
#6 107.9 Preparing to unpack .../162-libzstd-dev_1.5.5+dfsg2-2build1.1_amd64.deb ...
#6 107.9 Unpacking libzstd-dev:amd64 (1.5.5+dfsg2-2build1.1) ...
#6 108.1 Selecting previously unselected package libelf-dev:amd64.
#6 108.1 Preparing to unpack .../163-libelf-dev_0.190-1.1ubuntu0.1_amd64.deb ...
#6 108.2 Unpacking libelf-dev:amd64 (0.190-1.1ubuntu0.1) ...
#6 108.4 Selecting previously unselected package libexpat1-dev:amd64.
#6 108.4 Preparing to unpack .../164-libexpat1-dev_2.6.1-2ubuntu0.3_amd64.deb ...
#6 108.4 Unpacking libexpat1-dev:amd64 (2.6.1-2ubuntu0.3) ...
#6 108.6 Selecting previously unselected package xorg-sgml-doctools.
#6 108.6 Preparing to unpack .../165-xorg-sgml-doctools_1%3a1.11-1.1_all.deb ...
#6 108.6 Unpacking xorg-sgml-doctools (1:1.11-1.1) ...
#6 108.9 Selecting previously unselected package x11proto-dev.
#6 108.9 Preparing to unpack .../166-x11proto-dev_2023.2-1_all.deb ...
#6 108.9 Unpacking x11proto-dev (2023.2-1) ...
#6 109.2 Selecting previously unselected package libxau-dev:amd64.
#6 109.2 Preparing to unpack .../167-libxau-dev_1%3a1.0.9-1build6_amd64.deb ...
#6 109.3 Unpacking libxau-dev:amd64 (1:1.0.9-1build6) ...
#6 109.5 Selecting previously unselected package libxdmcp-dev:amd64.
#6 109.5 Preparing to unpack .../168-libxdmcp-dev_1%3a1.1.3-0ubuntu6_amd64.deb ...
#6 109.5 Unpacking libxdmcp-dev:amd64 (1:1.1.3-0ubuntu6) ...
#6 109.7 Selecting previously unselected package xtrans-dev.
#6 109.7 Preparing to unpack .../169-xtrans-dev_1.4.0-1_all.deb ...
#6 109.7 Unpacking xtrans-dev (1.4.0-1) ...
#6 109.9 Selecting previously unselected package libpthread-stubs0-dev:amd64.
#6 109.9 Preparing to unpack .../170-libpthread-stubs0-dev_0.4-1build3_amd64.deb ...
#6 110.0 Unpacking libpthread-stubs0-dev:amd64 (0.4-1build3) ...
#6 110.1 Selecting previously unselected package libxcb1-dev:amd64.
#6 110.1 Preparing to unpack .../171-libxcb1-dev_1.15-1ubuntu2_amd64.deb ...
#6 110.2 Unpacking libxcb1-dev:amd64 (1.15-1ubuntu2) ...
#6 110.3 Selecting previously unselected package libx11-dev:amd64.
#6 110.4 Preparing to unpack .../172-libx11-dev_2%3a1.8.7-1build1_amd64.deb ...
#6 110.4 Unpacking libx11-dev:amd64 (2:1.8.7-1build1) ...
#6 110.6 Selecting previously unselected package libglx-dev:amd64.
#6 110.6 Preparing to unpack .../173-libglx-dev_1.7.0-1build1_amd64.deb ...
#6 110.6 Unpacking libglx-dev:amd64 (1.7.0-1build1) ...
#6 110.8 Selecting previously unselected package libgl-dev:amd64.
#6 110.8 Preparing to unpack .../174-libgl-dev_1.7.0-1build1_amd64.deb ...
#6 110.8 Unpacking libgl-dev:amd64 (1.7.0-1build1) ...
#6 110.9 Selecting previously unselected package libicu-dev:amd64.
#6 110.9 Preparing to unpack .../175-libicu-dev_74.2-1ubuntu3.1_amd64.deb ...
#6 110.9 Unpacking libicu-dev:amd64 (74.2-1ubuntu3.1) ...
#6 111.3 Selecting previously unselected package libjs-jquery.
#6 111.3 Preparing to unpack .../176-libjs-jquery_3.6.1+dfsg+~3.5.14-1_all.deb ...
#6 111.4 Unpacking libjs-jquery (3.6.1+dfsg+~3.5.14-1) ...
#6 111.6 Selecting previously unselected package libjs-underscore.
#6 111.6 Preparing to unpack .../177-libjs-underscore_1.13.4~dfsg+~1.11.4-3_all.deb ...
#6 111.6 Unpacking libjs-underscore (1.13.4~dfsg+~1.11.4-3) ...
#6 111.8 Selecting previously unselected package libjs-sphinxdoc.
#6 111.8 Preparing to unpack .../178-libjs-sphinxdoc_7.2.6-6_all.deb ...
#6 111.8 Unpacking libjs-sphinxdoc (7.2.6-6) ...
#6 112.0 Selecting previously unselected package libpython3.12-dev:amd64.
#6 112.0 Preparing to unpack .../179-libpython3.12-dev_3.12.3-1ubuntu0.5_amd64.deb ...
#6 112.1 Unpacking libpython3.12-dev:amd64 (3.12.3-1ubuntu0.5) ...
#6 112.3 Selecting previously unselected package libpython3-dev:amd64.
#6 112.3 Preparing to unpack .../180-libpython3-dev_3.12.3-0ubuntu2_amd64.deb ...
#6 112.4 Unpacking libpython3-dev:amd64 (3.12.3-0ubuntu2) ...
#6 112.6 Selecting previously unselected package libswscale-dev:amd64.
#6 112.6 Preparing to unpack .../181-libswscale-dev_7%3a6.1.1-3ubuntu5_amd64.deb ...
#6 112.6 Unpacking libswscale-dev:amd64 (7:6.1.1-3ubuntu5) ...
#6 112.8 Selecting previously unselected package libxml2-dev:amd64.
#6 112.8 Preparing to unpack .../182-libxml2-dev_2.9.14+dfsg-1.3ubuntu3.3_amd64.deb ...
#6 112.8 Unpacking libxml2-dev:amd64 (2.9.14+dfsg-1.3ubuntu3.3) ...
#6 113.0 Selecting previously unselected package linux-hwe-6.11-headers-6.11.0-17.
#6 113.0 Preparing to unpack .../183-linux-hwe-6.11-headers-6.11.0-17_6.11.0-17.17~24.04.2_all.deb ...
#6 113.0 Unpacking linux-hwe-6.11-headers-6.11.0-17 (6.11.0-17.17~24.04.2) ...
#6 116.3 Selecting previously unselected package linux-headers-6.11.0-17-generic.
#6 116.3 Preparing to unpack .../184-linux-headers-6.11.0-17-generic_6.11.0-17.17~24.04.2_amd64.deb ...
#6 116.3 Unpacking linux-headers-6.11.0-17-generic (6.11.0-17.17~24.04.2) ...
#6 117.9 Selecting previously unselected package mesa-common-dev:amd64.
#6 117.9 Preparing to unpack .../185-mesa-common-dev_24.2.8-1ubuntu1~24.04.1_amd64.deb ...
#6 117.9 Unpacking mesa-common-dev:amd64 (24.2.8-1ubuntu1~24.04.1) ...
#6 118.0 Selecting previously unselected package roctracer.
#6 118.0 Preparing to unpack .../186-roctracer_4.1.60300.60300-39~24.04_amd64.deb ...
#6 118.0 Unpacking roctracer (4.1.60300.60300-39~24.04) ...
#6 118.0 Selecting previously unselected package rocrand.
#6 118.0 Preparing to unpack .../187-rocrand_3.2.0.60300-39~24.04_amd64.deb ...
#6 118.0 Unpacking rocrand (3.2.0.60300-39~24.04) ...
#6 119.2 Selecting previously unselected package miopen-hip.
#6 119.2 Preparing to unpack .../188-miopen-hip_3.3.0.60300-39~24.04_amd64.deb ...
#6 119.2 Unpacking miopen-hip (3.3.0.60300-39~24.04) ...
#6 122.5 Selecting previously unselected package migraphx.
#6 122.5 Preparing to unpack .../189-migraphx_2.11.0.60300-39~24.04_amd64.deb ...
#6 122.5 Unpacking migraphx (2.11.0.60300-39~24.04) ...
#6 124.1 Selecting previously unselected package migraphx-dev.
#6 124.1 Preparing to unpack .../190-migraphx-dev_2.11.0.60300-39~24.04_amd64.deb ...
#6 124.1 Unpacking migraphx-dev (2.11.0.60300-39~24.04) ...
#6 124.4 Selecting previously unselected package miopen-hip-dev.
#6 124.4 Preparing to unpack .../191-miopen-hip-dev_3.3.0.60300-39~24.04_amd64.deb ...
#6 124.5 Unpacking miopen-hip-dev (3.3.0.60300-39~24.04) ...
#6 124.7 Selecting previously unselected package openmp-extras-runtime.
#6 124.7 Preparing to unpack .../192-openmp-extras-runtime_18.63.0.60300-39~24.04_amd64.deb ...
#6 124.7 Unpacking openmp-extras-runtime (18.63.0.60300-39~24.04) ...
#6 126.6 Selecting previously unselected package rocm-language-runtime.
#6 126.6 Preparing to unpack .../193-rocm-language-runtime_6.3.0.60300-39~24.04_amd64.deb ...
#6 126.6 Unpacking rocm-language-runtime (6.3.0.60300-39~24.04) ...
#6 126.9 Selecting previously unselected package rocm-hip-runtime.
#6 126.9 Preparing to unpack .../194-rocm-hip-runtime_6.3.0.60300-39~24.04_amd64.deb ...
#6 126.9 Unpacking rocm-hip-runtime (6.3.0.60300-39~24.04) ...
#6 127.1 Selecting previously unselected package rpp.
#6 127.2 Preparing to unpack .../195-rpp_1.9.1.60300-39~24.04_amd64.deb ...
#6 127.2 Unpacking rpp (1.9.1.60300-39~24.04) ...
#6 128.1 Selecting previously unselected package mivisionx.
#6 128.1 Preparing to unpack .../196-mivisionx_3.1.0.60300-39~24.04_amd64.deb ...
#6 128.2 Unpacking mivisionx (3.1.0.60300-39~24.04) ...
#6 128.8 Selecting previously unselected package rocm-device-libs.
#6 128.8 Preparing to unpack .../197-rocm-device-libs_1.0.0.60300-39~24.04_amd64.deb ...
#6 128.8 Unpacking rocm-device-libs (1.0.0.60300-39~24.04) ...
#6 129.1 Selecting previously unselected package rocm-cmake.
#6 129.1 Preparing to unpack .../198-rocm-cmake_0.14.0.60300-39~24.04_amd64.deb ...
#6 129.1 Unpacking rocm-cmake (0.14.0.60300-39~24.04) ...
#6 129.4 Selecting previously unselected package rocm-hip-runtime-dev.
#6 129.4 Preparing to unpack .../199-rocm-hip-runtime-dev_6.3.0.60300-39~24.04_amd64.deb ...
#6 129.4 Unpacking rocm-hip-runtime-dev (6.3.0.60300-39~24.04) ...
#6 129.6 Selecting previously unselected package rpp-dev.
#6 129.6 Preparing to unpack .../200-rpp-dev_1.9.1.60300-39~24.04_amd64.deb ...
#6 129.6 Unpacking rpp-dev (1.9.1.60300-39~24.04) ...
#6 129.9 Selecting previously unselected package rocblas-dev.
#6 129.9 Preparing to unpack .../201-rocblas-dev_4.3.0.60300-39~24.04_amd64.deb ...
#6 129.9 Unpacking rocblas-dev (4.3.0.60300-39~24.04) ...
#6 130.2 Selecting previously unselected package mivisionx-dev.
#6 130.2 Preparing to unpack .../202-mivisionx-dev_3.1.0.60300-39~24.04_amd64.deb ...
#6 130.2 Unpacking mivisionx-dev (3.1.0.60300-39~24.04) ...
#6 130.6 Selecting previously unselected package openmp-extras-dev.
#6 130.7 Preparing to unpack .../203-openmp-extras-dev_18.63.0.60300-39~24.04_amd64.deb ...
#6 130.7 Unpacking openmp-extras-dev (18.63.0.60300-39~24.04) ...
#6 131.6 Selecting previously unselected package python3-argcomplete.
#6 131.6 Preparing to unpack .../204-python3-argcomplete_3.1.4-1ubuntu0.1_all.deb ...
#6 131.6 Unpacking python3-argcomplete (3.1.4-1ubuntu0.1) ...
#6 131.9 Selecting previously unselected package python3.12-dev.
#6 131.9 Preparing to unpack .../205-python3.12-dev_3.12.3-1ubuntu0.5_amd64.deb ...
#6 131.9 Unpacking python3.12-dev (3.12.3-1ubuntu0.5) ...
#6 132.1 Selecting previously unselected package python3-dev.
#6 132.1 Preparing to unpack .../206-python3-dev_3.12.3-0ubuntu2_amd64.deb ...
#6 132.2 Unpacking python3-dev (3.12.3-0ubuntu2) ...
#6 132.5 Selecting previously unselected package rocm-smi-lib.
#6 132.5 Preparing to unpack .../207-rocm-smi-lib_7.4.0.60300-39~24.04_amd64.deb ...
#6 132.5 Unpacking rocm-smi-lib (7.4.0.60300-39~24.04) ...
#6 132.7 Selecting previously unselected package rccl.
#6 132.8 Preparing to unpack .../208-rccl_2.21.5.60300-39~24.04_amd64.deb ...
#6 132.8 Unpacking rccl (2.21.5.60300-39~24.04) ...
#6 134.8 Selecting previously unselected package rccl-dev.
#6 134.8 Preparing to unpack .../209-rccl-dev_2.21.5.60300-39~24.04_amd64.deb ...
#6 134.8 Unpacking rccl-dev (2.21.5.60300-39~24.04) ...
#6 134.9 Selecting previously unselected package rocalution.
#6 134.9 Preparing to unpack .../210-rocalution_3.2.1.60300-39~24.04_amd64.deb ...
#6 134.9 Unpacking rocalution (3.2.1.60300-39~24.04) ...
#6 135.3 Selecting previously unselected package rocalution-dev.
#6 135.3 Preparing to unpack .../211-rocalution-dev_3.2.1.60300-39~24.04_amd64.deb ...
#6 135.3 Unpacking rocalution-dev (3.2.1.60300-39~24.04) ...
#6 135.3 Selecting previously unselected package rocfft-dev.
#6 135.3 Preparing to unpack .../212-rocfft-dev_1.0.31.60300-39~24.04_amd64.deb ...
#6 135.3 Unpacking rocfft-dev (1.0.31.60300-39~24.04) ...
#6 135.4 Selecting previously unselected package rocm-utils.
#6 135.5 Preparing to unpack .../213-rocm-utils_6.3.0.60300-39~24.04_amd64.deb ...
#6 135.5 Unpacking rocm-utils (6.3.0.60300-39~24.04) ...
#6 135.5 Selecting previously unselected package rocm-dbgapi.
#6 135.5 Preparing to unpack .../214-rocm-dbgapi_0.77.0.60300-39~24.04_amd64.deb ...
#6 135.5 Unpacking rocm-dbgapi (0.77.0.60300-39~24.04) ...
#6 135.6 Selecting previously unselected package rocm-debug-agent.
#6 135.6 Preparing to unpack .../215-rocm-debug-agent_2.0.3.60300-39~24.04_amd64.deb ...
#6 135.6 Unpacking rocm-debug-agent (2.0.3.60300-39~24.04) ...
#6 135.6 Selecting previously unselected package rocm-gdb.
#6 135.6 Preparing to unpack .../216-rocm-gdb_15.2.60300-39~24.04_amd64.deb ...
#6 135.6 Unpacking rocm-gdb (15.2.60300-39~24.04) ...
#6 136.6 Selecting previously unselected package libnuma-dev:amd64.
#6 136.7 Preparing to unpack .../217-libnuma-dev_2.0.18-1build1_amd64.deb ...
#6 136.7 Unpacking libnuma-dev:amd64 (2.0.18-1build1) ...
#6 136.7 Selecting previously unselected package rocprofiler.
#6 136.7 Preparing to unpack .../218-rocprofiler_2.0.60300.60300-39~24.04_amd64.deb ...
#6 136.7 Unpacking rocprofiler (2.0.60300.60300-39~24.04) ...
#6 136.7 Selecting previously unselected package rocprofiler-plugins.
#6 136.7 Preparing to unpack .../219-rocprofiler-plugins_2.0.60300.60300-39~24.04_amd64.deb ...
#6 136.7 Unpacking rocprofiler-plugins (2.0.60300.60300-39~24.04) ...
#6 136.8 Selecting previously unselected package rocprofiler-sdk-roctx.
#6 136.8 Preparing to unpack .../220-rocprofiler-sdk-roctx_0.5.0-39~24.04_amd64.deb ...
#6 136.8 Unpacking rocprofiler-sdk-roctx (0.5.0-39~24.04) ...
#6 136.8 Selecting previously unselected package rocprofiler-sdk.
#6 136.8 Preparing to unpack .../221-rocprofiler-sdk_0.5.0-39~24.04_amd64.deb ...
#6 136.8 Unpacking rocprofiler-sdk (0.5.0-39~24.04) ...
#6 136.9 Selecting previously unselected package rocprofiler-dev.
#6 136.9 Preparing to unpack .../222-rocprofiler-dev_2.0.60300.60300-39~24.04_amd64.deb ...
#6 136.9 Unpacking rocprofiler-dev (2.0.60300.60300-39~24.04) ...
#6 136.9 Selecting previously unselected package roctracer-dev.
#6 137.0 Preparing to unpack .../223-roctracer-dev_4.1.60300.60300-39~24.04_amd64.deb ...
#6 137.0 Unpacking roctracer-dev (4.1.60300.60300-39~24.04) ...
#6 137.0 Selecting previously unselected package rocm-developer-tools.
#6 137.0 Preparing to unpack .../224-rocm-developer-tools_6.3.0.60300-39~24.04_amd64.deb ...
#6 137.0 Unpacking rocm-developer-tools (6.3.0.60300-39~24.04) ...
#6 137.1 Selecting previously unselected package rocm-openmp-sdk.
#6 137.1 Preparing to unpack .../225-rocm-openmp-sdk_6.3.0.60300-39~24.04_amd64.deb ...
#6 137.1 Unpacking rocm-openmp-sdk (6.3.0.60300-39~24.04) ...
#6 137.1 Selecting previously unselected package rocm-opencl.
#6 137.1 Preparing to unpack .../226-rocm-opencl_2.0.0.60300-39~24.04_amd64.deb ...
#6 137.1 Unpacking rocm-opencl (2.0.0.60300-39~24.04) ...
#6 137.1 Selecting previously unselected package rocm-opencl-runtime.
#6 137.1 Preparing to unpack .../227-rocm-opencl-runtime_6.3.0.60300-39~24.04_amd64.deb ...
#6 137.1 Unpacking rocm-opencl-runtime (6.3.0.60300-39~24.04) ...
#6 137.2 Selecting previously unselected package rocm-opencl-dev.
#6 137.2 Preparing to unpack .../228-rocm-opencl-dev_2.0.0.60300-39~24.04_amd64.deb ...
#6 137.2 Unpacking rocm-opencl-dev (2.0.0.60300-39~24.04) ...
#6 137.2 Selecting previously unselected package rocm-opencl-sdk.
#6 137.2 Preparing to unpack .../229-rocm-opencl-sdk_6.3.0.60300-39~24.04_amd64.deb ...
#6 137.2 Unpacking rocm-opencl-sdk (6.3.0.60300-39~24.04) ...
#6 137.2 Selecting previously unselected package rocm-hip-libraries.
#6 137.3 Preparing to unpack .../230-rocm-hip-libraries_6.3.0.60300-39~24.04_amd64.deb ...
#6 137.3 Unpacking rocm-hip-libraries (6.3.0.60300-39~24.04) ...
#6 137.3 Selecting previously unselected package rocm-ml-libraries.
#6 137.3 Preparing to unpack .../231-rocm-ml-libraries_6.3.0.60300-39~24.04_amd64.deb ...
#6 137.3 Unpacking rocm-ml-libraries (6.3.0.60300-39~24.04) ...
#6 137.3 Selecting previously unselected package rocrand-dev.
#6 137.3 Preparing to unpack .../232-rocrand-dev_3.2.0.60300-39~24.04_amd64.deb ...
#6 137.3 Unpacking rocrand-dev (3.2.0.60300-39~24.04) ...
#6 137.4 Selecting previously unselected package rocsolver-dev.
#6 137.4 Preparing to unpack .../233-rocsolver-dev_3.27.0.60300-39~24.04_amd64.deb ...
#6 137.4 Unpacking rocsolver-dev (3.27.0.60300-39~24.04) ...
#6 137.4 Selecting previously unselected package rocsparse-dev.
#6 137.4 Preparing to unpack .../234-rocsparse-dev_3.3.0.60300-39~24.04_amd64.deb ...
#6 137.4 Unpacking rocsparse-dev (3.3.0.60300-39~24.04) ...
#6 137.5 Selecting previously unselected package rocthrust-dev.
#6 137.5 Preparing to unpack .../235-rocthrust-dev_3.3.0.60300-39~24.04_amd64.deb ...
#6 137.5 Unpacking rocthrust-dev (3.3.0.60300-39~24.04) ...
#6 137.7 Selecting previously unselected package rocwmma-dev.
#6 137.7 Preparing to unpack .../236-rocwmma-dev_1.6.0.60300-39~24.04_amd64.deb ...
#6 137.7 Unpacking rocwmma-dev (1.6.0.60300-39~24.04) ...
#6 137.7 Selecting previously unselected package rocm-hip-sdk.
#6 137.7 Preparing to unpack .../237-rocm-hip-sdk_6.3.0.60300-39~24.04_amd64.deb ...
#6 137.7 Unpacking rocm-hip-sdk (6.3.0.60300-39~24.04) ...
#6 137.8 Selecting previously unselected package rocm-ml-sdk.
#6 137.8 Preparing to unpack .../238-rocm-ml-sdk_6.3.0.60300-39~24.04_amd64.deb ...
#6 137.8 Unpacking rocm-ml-sdk (6.3.0.60300-39~24.04) ...
#6 137.8 Selecting previously unselected package rocm.
#6 137.8 Preparing to unpack .../239-rocm_6.3.0.60300-39~24.04_amd64.deb ...
#6 137.8 Unpacking rocm (6.3.0.60300-39~24.04) ...
#6 137.8 Selecting previously unselected package zstd.
#6 137.9 Preparing to unpack .../240-zstd_1.5.5+dfsg2-2build1.1_amd64.deb ...
#6 137.9 Unpacking zstd (1.5.5+dfsg2-2build1.1) ...
#6 137.9 Setting up python3-pkg-resources (68.1.2-2ubuntu1.1) ...
#6 138.1 Setting up cpio (2.15+dfsg-1ubuntu2) ...
#6 138.1 update-alternatives: using /usr/bin/mt-gnu to provide /usr/bin/mt (mt) in auto mode
#6 138.1 update-alternatives: warning: skip creation of /usr/share/man/man1/mt.1.gz because associated file /usr/share/man/man1/mt-gnu.1.gz (of link group mt) doesn't exist
#6 138.1 Setting up libavutil-dev:amd64 (7:6.1.1-3ubuntu5) ...
#6 138.1 Setting up javascript-common (11+nmu1) ...
#6 138.1 Setting up gcc-11-base:amd64 (11.4.0-9ubuntu1) ...
#6 138.1 Setting up libfile-which-perl (1.27-2) ...
#6 138.1 Setting up python3-dbus (1.3.2-5build3) ...
#6 138.2 Setting up pci.ids (0.0~2024.03.31-1ubuntu0.1) ...
#6 138.2 Setting up libdrm-nouveau2:amd64 (2.4.122-1~ubuntu0.24.04.1) ...
#6 138.2 Setting up libgpm2:amd64 (1.20.7-11) ...
#6 138.2 Setting up linux-base (4.5ubuntu9+24.04.1) ...
#6 138.3 Setting up libpciaccess-dev:amd64 (0.17-3build1) ...
#6 138.3 Setting up libzstd-dev:amd64 (1.5.5+dfsg2-2build1.1) ...
#6 138.3 Setting up python3-setuptools (68.1.2-2ubuntu1.1) ...
#6 138.7 Setting up libdebuginfod-common (0.190-1.1ubuntu0.1) ...
#6 138.8 Setting up libmagic-mgc (1:5.45-3build1) ...
#6 138.8 Setting up libswresample-dev:amd64 (7:6.1.1-3ubuntu5) ...
#6 138.8 Setting up libavcodec-dev:amd64 (7:6.1.1-3ubuntu5) ...
#6 138.8 Setting up libargon2-1:amd64 (0~20190702+dfsg-4build1) ...
#6 138.8 Setting up libmagic1t64:amd64 (1:5.45-3build1) ...
#6 138.8 Setting up m4 (1.4.19-4build1) ...
#6 138.8 Setting up python3-yaml (6.0.1-2build2) ...
#6 138.9 Setting up systemd-dev (255.4-1ubuntu8.6) ...
#6 138.9 Setting up libavformat-dev:amd64 (7:6.1.1-3ubuntu5) ...
#6 138.9 Setting up file (1:5.45-3build1) ...
#6 138.9 Setting up libpthread-stubs0-dev:amd64 (0.4-1build3) ...
#6 138.9 Setting up python3-wheel (0.42.0-2) ...
#6 139.0 Setting up libsource-highlight-common (3.1.9-4.3build1) ...
#6 139.0 Setting up libfakeroot:amd64 (1.33-1) ...
#6 139.0 Setting up libasan6:amd64 (11.4.0-9ubuntu1) ...
#6 139.0 Setting up libc6-dbg:amd64 (2.39-0ubuntu8.4) ...
#6 139.0 Setting up libnuma-dev:amd64 (2.0.18-1build1) ...
#6 139.1 Setting up libdw1t64:amd64 (0.190-1.1ubuntu0.1) ...
#6 139.1 Setting up rocm-core (6.3.0.60300-39~24.04) ...
#6 139.1 update-alternatives: using /opt/rocm-6.3.0 to provide /opt/rocm (rocm) in auto mode
#6 139.1 Setting up libc6-x32 (2.39-0ubuntu8.4) ...
#6 139.1 Setting up libfile-copy-recursive-perl (0.45-4) ...
#6 139.1 Setting up fakeroot (1.33-1) ...
#6 139.1 update-alternatives: using /usr/bin/fakeroot-sysv to provide /usr/bin/fakeroot (fakeroot) in auto mode
#6 139.1 update-alternatives: warning: skip creation of /usr/share/man/man1/fakeroot.1.gz because associated file /usr/share/man/man1/fakeroot-sysv.1.gz (of link group fakeroot) doesn't exist
#6 139.1 update-alternatives: warning: skip creation of /usr/share/man/man1/faked.1.gz because associated file /usr/share/man/man1/faked-sysv.1.gz (of link group fakeroot) doesn't exist
#6 139.1 update-alternatives: warning: skip creation of /usr/share/man/es/man1/fakeroot.1.gz because associated file /usr/share/man/es/man1/fakeroot-sysv.1.gz (of link group fakeroot) doesn't exist
#6 139.1 update-alternatives: warning: skip creation of /usr/share/man/es/man1/faked.1.gz because associated file /usr/share/man/es/man1/faked-sysv.1.gz (of link group fakeroot) doesn't exist
#6 139.1 update-alternatives: warning: skip creation of /usr/share/man/fr/man1/fakeroot.1.gz because associated file /usr/share/man/fr/man1/fakeroot-sysv.1.gz (of link group fakeroot) doesn't exist
#6 139.1 update-alternatives: warning: skip creation of /usr/share/man/fr/man1/faked.1.gz because associated file /usr/share/man/fr/man1/faked-sysv.1.gz (of link group fakeroot) doesn't exist
#6 139.1 update-alternatives: warning: skip creation of /usr/share/man/sv/man1/fakeroot.1.gz because associated file /usr/share/man/sv/man1/fakeroot-sysv.1.gz (of link group fakeroot) doesn't exist
#6 139.1 update-alternatives: warning: skip creation of /usr/share/man/sv/man1/faked.1.gz because associated file /usr/share/man/sv/man1/faked-sysv.1.gz (of link group fakeroot) doesn't exist
#6 139.1 Setting up rocm-device-libs (1.0.0.60300-39~24.04) ...
#6 139.1 Setting up libpython3.12t64:amd64 (3.12.3-1ubuntu0.5) ...
#6 139.1 Setting up libklibc:amd64 (2.0.13-4ubuntu0.1) ...
#6 139.1 Setting up xtrans-dev (1.4.0-1) ...
#6 139.1 Setting up autotools-dev (20220109.1) ...
#6 139.1 Setting up libexpat1-dev:amd64 (2.6.1-2ubuntu0.3) ...
#6 139.1 Setting up libncurses6:amd64 (6.4+20240113-1ubuntu2) ...
#6 139.1 Setting up libswscale-dev:amd64 (7:6.1.1-3ubuntu5) ...
#6 139.1 Setting up rocfft (1.0.31.60300-39~24.04) ...
#6 139.1 Setting up icu-devtools (74.2-1ubuntu3.1) ...
#6 139.1 Setting up libipt2 (2.0.6-1build1) ...
#6 139.1 Setting up dhcpcd-base (1:10.0.6-1ubuntu3.1) ...
#6 139.1 info: Selecting UID from range 100 to 999 ...
#6 139.1 
#6 139.1 info: Adding system user `dhcpcd' (UID 100) ...
#6 139.2 info: Adding new user `dhcpcd' (UID 100) with group `nogroup' ...
#6 139.2 info: Not creating home directory `/usr/lib/dhcpcd'.
#6 139.2 Setting up gir1.2-glib-2.0:amd64 (2.80.0-6ubuntu3.2) ...
#6 139.2 Setting up python3-pip (24.0+dfsg-1ubuntu1.1) ...
#6 140.2 Setting up busybox-initramfs (1:1.36.1-6ubuntu3.1) ...
#6 140.2 Setting up libx32gomp1 (14.2.0-4ubuntu2~24.04) ...
#6 140.2 Setting up hipblas-common-dev (1.0.0.60300-39~24.04) ...
#6 140.2 Setting up amdgpu-core (1:6.3.60300-2084815.24.04) ...
#6 140.2 Setting up rocprofiler-register (0.4.0.60300-39~24.04) ...
#6 140.2 Setting up libbabeltrace1:amd64 (1.5.11-3build3) ...
#6 140.2 Setting up autoconf (2.71-3) ...
#6 140.2 Setting up amdgpu-dkms-firmware (1:6.10.5.60300-2084815.24.04) ...
#6 140.2 Setting up rocwmma-dev (1.6.0.60300-39~24.04) ...
#6 140.2 Setting up libfdisk1:amd64 (2.39.3-9ubuntu6.2) ...
#6 140.2 Setting up libtimedate-perl (2.3300-2) ...
#6 140.2 Setting up zlib1g-dev:amd64 (1:1.3.dfsg-3.1ubuntu2.1) ...
#6 140.2 Setting up libpci3:amd64 (1:3.10.0-2build1) ...
#6 140.2 Setting up libdevmapper1.02.1:amd64 (2:1.02.185-3ubuntu3.2) ...
#6 140.2 Setting up dmsetup (2:1.02.185-3ubuntu3.2) ...
#6 140.2 Setting up dbus-session-bus-common (1.14.10-4ubuntu4.1) ...
#6 140.2 Setting up hipify-clang (18.0.0.60300-39~24.04) ...
#6 140.2 Setting up libdrm-amdgpu-common (1.0.0.60300-2084815.24.04) ...
#6 140.2 Setting up libc6-i386 (2.39-0ubuntu8.4) ...
#6 140.3 Setting up libsuitesparseconfig7:amd64 (1:7.6.1+dfsg-1build1) ...
#6 140.3 Setting up libgirepository-1.0-1:amd64 (1.80.1-1) ...
#6 140.3 Setting up libx32quadmath0 (14.2.0-4ubuntu2~24.04) ...
#6 140.3 Setting up xorg-sgml-doctools (1:1.11-1.1) ...
#6 140.3 Setting up rocm-smi-lib (7.4.0.60300-39~24.04) ...
#6 140.3 [WARNING] Detected logrotate is not installed. rocm-smi-lib logs (when turned on) will not rotate properly.
#6 140.3 Setting up linux-hwe-6.11-headers-6.11.0-17 (6.11.0-17.17~24.04.2) ...
#6 140.3 Setting up libjs-jquery (3.6.1+dfsg+~3.5.14-1) ...
#6 140.3 Setting up dbus-system-bus-common (1.14.10-4ubuntu4.1) ...
#6 140.4 Setting up python3-argcomplete (3.1.4-1ubuntu0.1) ...
#6 140.5 Setting up valgrind (1:3.22.0-0ubuntu3) ...
#6 140.5 Setting up klibc-utils (2.0.13-4ubuntu0.1) ...
#6 140.5 No diversion 'diversion of /usr/share/initramfs-tools/hooks/klibc to /usr/share/initramfs-tools/hooks/klibc^i-t by klibc-utils', none removed.
#6 140.5 Setting up libjson-c5:amd64 (0.17-1build1) ...
#6 140.5 Setting up libicu-dev:amd64 (74.2-1ubuntu3.1) ...
#6 140.5 Setting up lib32atomic1 (14.2.0-4ubuntu2~24.04) ...
#6 140.5 Setting up zstd (1.5.5+dfsg2-2build1.1) ...
#6 140.5 Setting up liburi-perl (5.27-1) ...
#6 140.5 Setting up dbus-bin (1.14.10-4ubuntu4.1) ...
#6 140.5 Setting up libkmod2:amd64 (31+20240202-2ubuntu7.1) ...
#6 140.5 Setting up libjs-underscore (1.13.4~dfsg+~1.11.4-3) ...
#6 140.5 Setting up initramfs-tools-bin (0.142ubuntu25.5) ...
#6 140.5 Setting up rocrand (3.2.0.60300-39~24.04) ...
#6 140.5 Setting up libtsan0:amd64 (11.4.0-9ubuntu1) ...
#6 140.5 Setting up libx32atomic1 (14.2.0-4ubuntu2~24.04) ...
#6 140.5 Setting up automake (1:1.16.5-1.3ubuntu1) ...
#6 140.5 update-alternatives: using /usr/bin/automake-1.16 to provide /usr/bin/automake (automake) in auto mode
#6 140.5 update-alternatives: warning: skip creation of /usr/share/man/man1/automake.1.gz because associated file /usr/share/man/man1/automake-1.16.1.gz (of link group automake) doesn't exist
#6 140.5 update-alternatives: warning: skip creation of /usr/share/man/man1/aclocal.1.gz because associated file /usr/share/man/man1/aclocal-1.16.1.gz (of link group automake) doesn't exist
#6 140.5 Setting up x11proto-dev (2023.2-1) ...
#6 140.5 Setting up linux-headers-6.11.0-17-generic (6.11.0-17.17~24.04.2) ...
#6 140.5 Setting up hiprand (2.11.0.60300-39~24.04) ...
#6 140.5 Setting up libdebuginfod1t64:amd64 (0.190-1.1ubuntu0.1) ...
#6 140.5 Setting up libhttp-date-perl (6.06-1) ...
#6 140.6 Setting up libdrm-dev:amd64 (2.4.122-1~ubuntu0.24.04.1) ...
#6 140.6 Setting up libncurses-dev:amd64 (6.4+20240113-1ubuntu2) ...
#6 140.6 Setting up roctracer (4.1.60300.60300-39~24.04) ...
#6 140.6 Setting up libc6-dev-i386 (2.39-0ubuntu8.4) ...
#6 140.6 Setting up lib32itm1 (14.2.0-4ubuntu2~24.04) ...
#6 140.6 Setting up libamd3:amd64 (1:7.6.1+dfsg-1build1) ...
#6 140.6 Setting up libfile-listing-perl (6.16-1) ...
#6 140.6 Setting up libxau-dev:amd64 (1:1.0.9-1build6) ...
#6 140.6 Setting up rocrand-dev (3.2.0.60300-39~24.04) ...
#6 140.6 Setting up composablekernel-dev (1.1.0.60300-39~24.04) ...
#6 140.6 Setting up amd-smi-lib (24.7.1.60300-39~24.04) ...
#6 140.8 [33mWARNING: The directory '/home/jovyan/.cache/pip' or its parent directory is not owned or is not writable by the current user. The cache has been disabled. Check the permissions and owner of that directory. If executing pip with sudo, you should use sudo's -H flag.[0m[33m
#6 140.8 [0mUsing pyproject.toml for installation due to setuptools version 68.1.2
#6 141.3 [33mWARNING: The directory '/home/jovyan/.cache/pip' or its parent directory is not owned or is not writable by the current user. The cache has been disabled. Check the permissions and owner of that directory. If executing pip with sudo, you should use sudo's -H flag.[0m[33m
#6 141.3 [0mDefaulting to system-wide installation.
#6 142.0 Installing /usr/lib/python3/dist-packages/argcomplete/bash_completion.d/_python-argcomplete to /usr/local/share/zsh/site-functions/_python-argcomplete...
#6 142.0 Installed.
#6 142.0 Installing /usr/lib/python3/dist-packages/argcomplete/bash_completion.d/_python-argcomplete to /etc/bash_completion.d/python-argcomplete...
#6 142.0 Installed.
#6 142.0 Please restart your shell or source the installed file to activate it.
#6 143.5 [WARNING] Detected logrotate is not installed. amd-smi-lib logs (when turned on) will not rotate properly.
#6 143.5 Setting up libcolamd3:amd64 (1:7.6.1+dfsg-1build1) ...
#6 143.5 Setting up rocm-cmake (0.14.0.60300-39~24.04) ...
#6 143.6 Setting up rocprofiler-sdk-roctx (0.5.0-39~24.04) ...
#6 143.6 Setting up libx32gcc-s1 (14.2.0-4ubuntu2~24.04) ...
#6 143.6 Setting up hsa-amd-aqlprofile (1.0.0.60300-39~24.04) ...
#6 143.6 Setting up hipfft (1.0.17.60300-39~24.04) ...
#6 143.6 Setting up libx32itm1 (14.2.0-4ubuntu2~24.04) ...
#6 143.6 Setting up libpython3.12-dev:amd64 (3.12.3-1ubuntu0.5) ...
#6 143.6 Setting up libsource-highlight4t64:amd64 (3.1.9-4.3build1) ...
#6 143.6 Setting up dbus-daemon (1.14.10-4ubuntu4.1) ...
#6 143.6 Setting up hipfft-dev (1.0.17.60300-39~24.04) ...
#6 143.6 Setting up hiptensor (1.4.0.60300-39~24.04) ...
#6 143.6 Setting up kmod (31+20240202-2ubuntu7.1) ...
#6 143.6 sed: can't read /etc/modules: No such file or directory
#6 143.6 Setting up half (1.12.0.60300-39~24.04) ...
#6 143.7 Setting up hipblaslt (0.10.0.60300-39~24.04) ...
#6 143.7 Setting up libcamd3:amd64 (1:7.6.1+dfsg-1build1) ...
#6 143.7 Setting up dkms (3.0.11-1ubuntu13) ...
#6 143.7 Setting up hsa-rocr (1.14.0.60300-39~24.04) ...
#6 143.8 Setting up libx32asan8 (14.2.0-4ubuntu2~24.04) ...
#6 143.8 Setting up libc6-dev-x32 (2.39-0ubuntu8.4) ...
#6 143.8 Setting up libxdmcp-dev:amd64 (1:1.1.3-0ubuntu6) ...
#6 143.8 Setting up libxml2-dev:amd64 (2.9.14+dfsg-1.3ubuntu3.3) ...
#6 143.8 Setting up gdb (15.0.50.20240403-0ubuntu1) ...
#6 143.8 Setting up lib32gomp1 (14.2.0-4ubuntu2~24.04) ...
#6 143.8 Setting up hiptensor-dev (1.4.0.60300-39~24.04) ...
#6 143.8 Setting up libdrm2-amdgpu:amd64 (1:2.4.123.60300-2084815.24.04) ...
#6 143.8 Setting up lib32gcc-s1 (14.2.0-4ubuntu2~24.04) ...
#6 143.8 Setting up lib32stdc++6 (14.2.0-4ubuntu2~24.04) ...
#6 143.8 Setting up gir1.2-girepository-2.0:amd64 (1.80.1-1) ...
#6 143.8 Setting up rocfft-dev (1.0.31.60300-39~24.04) ...
#6 143.8 Setting up hiprand-dev (2.11.0.60300-39~24.04) ...
#6 143.8 Setting up dbus (1.14.10-4ubuntu4.1) ...
#6 143.8 Setting up python3-gi (3.48.2-1) ...
#6 144.0 Setting up lib32asan8 (14.2.0-4ubuntu2~24.04) ...
#6 144.0 Setting up libsystemd-shared:amd64 (255.4-1ubuntu8.6) ...
#6 144.0 Setting up python3.12-dev (3.12.3-1ubuntu0.5) ...
#6 144.0 Setting up libelf-dev:amd64 (0.190-1.1ubuntu0.1) ...
#6 144.0 Setting up rocprofiler-sdk (0.5.0-39~24.04) ...
#6 144.0 Setting up pciutils (1:3.10.0-2build1) ...
#6 144.0 Setting up libjs-sphinxdoc (7.2.6-6) ...
#6 144.0 Setting up libccolamd3:amd64 (1:7.6.1+dfsg-1build1) ...
#6 144.0 Setting up libgcc-11-dev:amd64 (11.4.0-9ubuntu1) ...
#6 144.0 Setting up dracut-install (060+5-1ubuntu3.3) ...
#6 144.0 Setting up hipblaslt-dev (0.10.0.60300-39~24.04) ...
#6 144.0 Setting up lib32quadmath0 (14.2.0-4ubuntu2~24.04) ...
#6 144.0 Setting up libcryptsetup12:amd64 (2:2.7.0-1ubuntu4.2) ...
#6 144.0 Setting up libx32stdc++6 (14.2.0-4ubuntu2~24.04) ...
#6 144.0 Setting up networkd-dispatcher (2.2.4-1) ...
#6 144.2 Created symlink /etc/systemd/system/multi-user.target.wants/networkd-dispatcher.service -> /usr/lib/systemd/system/networkd-dispatcher.service.
#6 144.2 Setting up comgr (2.8.0.60300-39~24.04) ...
#6 144.2 Setting up libcholmod5:amd64 (1:7.6.1+dfsg-1build1) ...
#6 144.2 Setting up libpython3-dev:amd64 (3.12.3-0ubuntu2) ...
#6 144.2 Setting up libxcb1-dev:amd64 (1.15-1ubuntu2) ...
#6 144.2 Setting up libdrm-amdgpu-radeon1:amd64 (1:2.4.123.60300-2084815.24.04) ...
#6 144.2 Setting up libx32ubsan1 (14.2.0-4ubuntu2~24.04) ...
#6 144.2 Setting up libdrm-amdgpu-amdgpu1:amd64 (1:2.4.123.60300-2084815.24.04) ...
#6 144.2 Setting up rocminfo (1.0.0.60300-39~24.04) ...
#6 144.2 Setting up libx11-dev:amd64 (2:1.8.7-1build1) ...
#6 144.2 Setting up systemd (255.4-1ubuntu8.6) ...
#6 144.2 Created symlink /etc/systemd/system/getty.target.wants/getty@tty1.service -> /usr/lib/systemd/system/getty@.service.
#6 144.2 Created symlink /etc/systemd/system/multi-user.target.wants/remote-fs.target -> /usr/lib/systemd/system/remote-fs.target.
#6 144.2 Created symlink /etc/systemd/system/sysinit.target.wants/systemd-pstore.service -> /usr/lib/systemd/system/systemd-pstore.service.
#6 144.2 Initializing machine ID from D-Bus machine ID.
#6 144.3 /usr/lib/tmpfiles.d/static-nodes-permissions.conf:18: Failed to resolve group 'kvm': No such process
#6 144.3 /usr/lib/tmpfiles.d/static-nodes-permissions.conf:19: Failed to resolve group 'kvm': No such process
#6 144.3 /usr/lib/tmpfiles.d/static-nodes-permissions.conf:20: Failed to resolve group 'kvm': No such process
#6 144.3 /usr/lib/tmpfiles.d/systemd-network.conf:10: Failed to resolve user 'systemd-network': No such process
#6 144.3 /usr/lib/tmpfiles.d/systemd-network.conf:11: Failed to resolve user 'systemd-network': No such process
#6 144.3 /usr/lib/tmpfiles.d/systemd-network.conf:12: Failed to resolve user 'systemd-network': No such process
#6 144.3 /usr/lib/tmpfiles.d/systemd-network.conf:13: Failed to resolve user 'systemd-network': No such process
#6 144.3 /usr/lib/tmpfiles.d/systemd.conf:22: Failed to resolve group 'systemd-journal': No such process
#6 144.3 /usr/lib/tmpfiles.d/systemd.conf:23: Failed to resolve group 'systemd-journal': No such process
#6 144.3 /usr/lib/tmpfiles.d/systemd.conf:28: Failed to resolve group 'systemd-journal': No such process
#6 144.3 /usr/lib/tmpfiles.d/systemd.conf:29: Failed to resolve group 'systemd-journal': No such process
#6 144.3 /usr/lib/tmpfiles.d/systemd.conf:30: Failed to resolve group 'systemd-journal': No such process
#6 144.3 Creating group 'systemd-journal' with GID 999.
#6 144.3 Creating group 'systemd-network' with GID 998.
#6 144.3 Creating user 'systemd-network' (systemd Network Management) with UID 998 and GID 998.
#6 144.3 Setting up hip-runtime-amd (6.3.42131.60300-39~24.04) ...
#6 144.3 Setting up lib32ubsan1 (14.2.0-4ubuntu2~24.04) ...
#6 144.3 Setting up hsa-rocr-dev (1.14.0.60300-39~24.04) ...
#6 144.3 Setting up lib32gcc-13-dev (13.3.0-6ubuntu2~24.04) ...
#6 144.3 Setting up openmp-extras-runtime (18.63.0.60300-39~24.04) ...
#6 144.3 Setting up rocm-utils (6.3.0.60300-39~24.04) ...
#6 144.3 Setting up rocprim-dev (3.3.0.60300-39~24.04) ...
#6 144.3 Setting up rocm-dbgapi (0.77.0.60300-39~24.04) ...
#6 144.3 Setting up libdrm-amdgpu-dev:amd64 (1:2.4.123.60300-2084815.24.04) ...
#6 144.3 Setting up python3-dev (3.12.3-0ubuntu2) ...
#6 144.3 Setting up libx32gcc-13-dev (13.3.0-6ubuntu2~24.04) ...
#6 144.3 Setting up hipcub-dev (3.3.0.60300-39~24.04) ...
#6 144.3 Setting up systemd-timesyncd (255.4-1ubuntu8.6) ...
#6 144.3 Creating group 'systemd-timesync' with GID 997.
#6 144.3 Creating user 'systemd-timesync' (systemd Time Synchronization) with UID 997 and GID 997.
#6 144.4 Created symlink /etc/systemd/system/dbus-org.freedesktop.timesync1.service -> /usr/lib/systemd/system/systemd-timesyncd.service.
#6 144.4 Created symlink /etc/systemd/system/sysinit.target.wants/systemd-timesyncd.service -> /usr/lib/systemd/system/systemd-timesyncd.service.
#6 144.4 Setting up udev (255.4-1ubuntu8.6) ...
#6 144.7 Creating group 'input' with GID 996.
#6 144.7 Creating group 'sgx' with GID 995.
#6 144.7 Creating group 'kvm' with GID 994.
#6 144.7 Creating group 'render' with GID 993.
#6 144.7 Setting up rocm-opencl (2.0.0.60300-39~24.04) ...
#6 144.8 Setting up systemd-hwe-hwdb (255.1.4) ...
#6 145.0 Setting up libstdc++-11-dev:amd64 (11.4.0-9ubuntu1) ...
#6 145.0 Setting up hipfort-dev (0.5.0.60300-39~24.04) ...
#6 145.0 Setting up libglx-dev:amd64 (1.7.0-1build1) ...
#6 145.0 Setting up rocblas (4.3.0.60300-39~24.04) ...
#6 145.1 Setting up gcc-13-multilib (13.3.0-6ubuntu2~24.04) ...
#6 145.1 Setting up lib32stdc++-13-dev (13.3.0-6ubuntu2~24.04) ...
#6 145.1 Setting up initramfs-tools-core (0.142ubuntu25.5) ...
#6 145.1 Setting up rccl (2.21.5.60300-39~24.04) ...
#6 145.1 Setting up gcc-multilib (4:13.2.0-7ubuntu1) ...
#6 145.1 Setting up libgl-dev:amd64 (1.7.0-1build1) ...
#6 145.1 Setting up systemd-resolved (255.4-1ubuntu8.6) ...
#6 145.1 Converting /etc/resolv.conf to a symlink to /run/systemd/resolve/stub-resolv.conf...
#6 145.1 mv: cannot move '/etc/resolv.conf' to '/etc/.resolv.conf.systemd-resolved.bak': Device or resource busy
#6 145.1 Cannot take a backup of /etc/resolv.conf.
#6 145.1 ln: failed to create symbolic link '/etc/resolv.conf': Device or resource busy
#6 145.1 Cannot install symlink from /etc/resolv.conf to ../run/systemd/resolve/stub-resolv.conf
#6 145.1 Creating group 'systemd-resolve' with GID 992.
#6 145.1 Creating user 'systemd-resolve' (systemd Resolver) with UID 992 and GID 992.
#6 145.2 Created symlink /etc/systemd/system/dbus-org.freedesktop.resolve1.service -> /usr/lib/systemd/system/systemd-resolved.service.
#6 145.2 Created symlink /etc/systemd/system/sysinit.target.wants/systemd-resolved.service -> /usr/lib/systemd/system/systemd-resolved.service.
#6 145.3 Setting up rocm-llvm (18.0.0.24455.60300-39~24.04) ...
#6 145.3 Setting up initramfs-tools (0.142ubuntu25.5) ...
#6 145.4 update-initramfs: deferring update (trigger activated)
#6 145.4 Setting up rocprofiler (2.0.60300.60300-39~24.04) ...
#6 145.4 Setting up rocsparse (3.3.0.60300-39~24.04) ...
#6 145.4 Setting up miopen-hip (3.3.0.60300-39~24.04) ...
#6 145.5 Setting up rocprofiler-dev (2.0.60300.60300-39~24.04) ...
#6 145.5 Setting up rocthrust-dev (3.3.0.60300-39~24.04) ...
#6 145.5 Setting up roctracer-dev (4.1.60300.60300-39~24.04) ...
#6 145.5 Setting up openmp-extras-dev (18.63.0.60300-39~24.04) ...
#6 145.5 Setting up libx32stdc++-13-dev (13.3.0-6ubuntu2~24.04) ...
#6 145.5 Setting up rocm-language-runtime (6.3.0.60300-39~24.04) ...
#6 145.6 Setting up hipsparse (3.1.2.60300-39~24.04) ...
#6 145.6 Setting up amdgpu-dkms (1:6.10.5.60300-2084815.24.04) ...
#6 145.7 Loading new amdgpu-6.10.5-2084815.24.04 DKMS files...
#6 145.8 Building for 6.11.0-17-generic
#6 145.9 Building for architecture x86_64
#6 145.9 Building initial module for 6.11.0-17-generic
#6 189.7 Done.
#6 190.0 Forcing installation of amdgpu
#6 190.0 
#6 190.0 amdgpu.ko:
#6 190.0 Running module version sanity check.
#6 190.0  - Original module
#6 190.1    - No original module exists within this kernel
#6 190.1  - Installation
#6 190.1    - Installing to /lib/modules/6.11.0-17-generic/updates/dkms/
#6 190.1 
#6 190.1 amdttm.ko:
#6 190.1 Running module version sanity check.
#6 190.1  - Original module
#6 190.1    - No original module exists within this kernel
#6 190.1  - Installation
#6 190.1    - Installing to /lib/modules/6.11.0-17-generic/updates/dkms/
#6 190.1 
#6 190.1 amdkcl.ko:
#6 190.1 Running module version sanity check.
#6 190.1  - Original module
#6 190.1    - No original module exists within this kernel
#6 190.1  - Installation
#6 190.1    - Installing to /lib/modules/6.11.0-17-generic/updates/dkms/
#6 190.1 
#6 190.1 amd-sched.ko:
#6 190.1 Running module version sanity check.
#6 190.2  - Original module
#6 190.2    - No original module exists within this kernel
#6 190.2  - Installation
#6 190.2    - Installing to /lib/modules/6.11.0-17-generic/updates/dkms/
#6 190.2 
#6 190.2 amddrm_ttm_helper.ko:
#6 190.2 Running module version sanity check.
#6 190.2  - Original module
#6 190.2    - No original module exists within this kernel
#6 190.2  - Installation
#6 190.2    - Installing to /lib/modules/6.11.0-17-generic/updates/dkms/
#6 190.2 
#6 190.2 amddrm_buddy.ko:
#6 190.2 Running module version sanity check.
#6 190.2  - Original module
#6 190.2    - No original module exists within this kernel
#6 190.2  - Installation
#6 190.2    - Installing to /lib/modules/6.11.0-17-generic/updates/dkms/
#6 190.2 
#6 190.2 amdxcp.ko:
#6 190.2 Running module version sanity check.
#6 190.2  - Original module
#6 190.2    - No original module exists within this kernel
#6 190.2  - Installation
#6 190.2    - Installing to /lib/modules/6.11.0-17-generic/updates/dkms/
#6 190.2 depmod...
#6 190.7 update-initramfs: Generating /boot/initrd.img-6.11.0-17-generic
#6 190.7 W: Kernel configuration /boot/config-6.11.0-17-generic is missing, cannot check for zstd compression support (CONFIG_RD_ZSTD)
#6 190.8 W: Can't find modules.builtin.modinfo (for locating built-in drivers' firmware, supported in Linux >=5.2)
#6 192.9 cat: /var/tmp/mkinitramfs_4utzXx/lib/modules/6.11.0-17-generic/modules.builtin: No such file or directory
#6 192.9 depmod: WARNING: could not open modules.order at /var/tmp/mkinitramfs_4utzXx/lib/modules/6.11.0-17-generic: No such file or directory
#6 192.9 depmod: WARNING: could not open modules.builtin at /var/tmp/mkinitramfs_4utzXx/lib/modules/6.11.0-17-generic: No such file or directory
#6 192.9 depmod: WARNING: could not open modules.builtin.modinfo at /var/tmp/mkinitramfs_4utzXx/lib/modules/6.11.0-17-generic: No such file or directory
#6 194.1 Setting up rocprofiler-plugins (2.0.60300.60300-39~24.04) ...
#6 194.1 Setting up rocm-gdb (15.2.60300-39~24.04) ...
#6 194.1 Setting up rocm-debug-agent (2.0.3.60300-39~24.04) ...
#6 194.1 Setting up rocsolver (3.27.0.60300-39~24.04) ...
#6 194.1 Setting up miopen-hip-dev (3.3.0.60300-39~24.04) ...
#6 194.1 Setting up hipblas (2.3.0.60300-39~24.04) ...
#6 194.1 Setting up rocm-hip-runtime (6.3.0.60300-39~24.04) ...
#6 194.1 update-alternatives: using /opt/rocm-6.3.0/bin/rocm_agent_enumerator to provide /usr/bin/rocm_agent_enumerator (rocm_agent_enumerator) in auto mode
#6 194.1 update-alternatives: using /opt/rocm-6.3.0/bin/rocminfo to provide /usr/bin/rocminfo (rocminfo) in auto mode
#6 194.1 Setting up rocm-developer-tools (6.3.0.60300-39~24.04) ...
#6 194.1 update-alternatives: using /opt/rocm-6.3.0/bin/amd-smi to provide /usr/bin/amd-smi (amd-smi) in auto mode
#6 194.1 update-alternatives: using /opt/rocm-6.3.0/bin/rocgdb to provide /usr/bin/rocgdb (rocgdb) in auto mode
#6 194.1 update-alternatives: using /opt/rocm-6.3.0/bin/rocm-smi to provide /usr/bin/rocm-smi (rocm-smi) in auto mode
#6 194.1 update-alternatives: using /opt/rocm-6.3.0/bin/rocprof to provide /usr/bin/rocprof (rocprof) in auto mode
#6 194.1 update-alternatives: using /opt/rocm-6.3.0/bin/rocsys to provide /usr/bin/rocsys (rocsys) in auto mode
#6 194.1 update-alternatives: using /opt/rocm-6.3.0/bin/rocprofv2 to provide /usr/bin/rocprofv2 (rocprofv2) in auto mode
#6 194.1 update-alternatives: using /opt/rocm-6.3.0/bin/roccoremerge to provide /usr/bin/roccoremerge (roccoremerge) in auto mode
#6 194.1 update-alternatives: using /opt/rocm-6.3.0/bin/rocprofv3 to provide /usr/bin/rocprofv3 (rocprofv3) in auto mode
#6 194.1 Setting up rocm-openmp-sdk (6.3.0.60300-39~24.04) ...
#6 194.1 Setting up rccl-dev (2.21.5.60300-39~24.04) ...
#6 194.2 Setting up rocblas-dev (4.3.0.60300-39~24.04) ...
#6 194.2 Setting up mesa-common-dev:amd64 (24.2.8-1ubuntu1~24.04.1) ...
#6 194.2 Setting up rocsparse-dev (3.3.0.60300-39~24.04) ...
#6 194.2 Setting up hipsparse-dev (3.1.2.60300-39~24.04) ...
#6 194.2 Setting up hipblas-dev (2.3.0.60300-39~24.04) ...
#6 194.2 Setting up rocsolver-dev (3.27.0.60300-39~24.04) ...
#6 194.2 Setting up rocalution (3.2.1.60300-39~24.04) ...
#6 194.2 Setting up hip-dev (6.3.42131.60300-39~24.04) ...
#6 194.2 Setting up hipsolver (2.3.0.60300-39~24.04) ...
#6 194.2 Setting up rpp (1.9.1.60300-39~24.04) ...
#6 194.2 Setting up rocm-opencl-runtime (6.3.0.60300-39~24.04) ...
#6 194.2 update-alternatives: using /opt/rocm-6.3.0/bin/clinfo to provide /usr/bin/clinfo (clinfo) in auto mode
#6 194.2 Setting up rocm-opencl-dev (2.0.0.60300-39~24.04) ...
#6 194.2 Setting up hipsolver-dev (2.3.0.60300-39~24.04) ...
#6 194.2 Setting up g++-13-multilib (13.3.0-6ubuntu2~24.04) ...
#6 194.2 Setting up g++-multilib (4:13.2.0-7ubuntu1) ...
#6 194.2 Setting up hipsparselt (0.2.2.60300-39~24.04) ...
#6 194.2 Setting up migraphx (2.11.0.60300-39~24.04) ...
#6 194.3 Setting up rocm-hip-libraries (6.3.0.60300-39~24.04) ...
#6 194.3 Setting up mivisionx (3.1.0.60300-39~24.04) ...
#6 194.3 Setting up rocm-opencl-sdk (6.3.0.60300-39~24.04) ...
#6 194.3 Setting up hipcc (1.1.1.60300-39~24.04) ...
#6 194.3 Setting up rocalution-dev (3.2.1.60300-39~24.04) ...
#6 194.3 Setting up hip-doc (6.3.42131.60300-39~24.04) ...
#6 194.3 Setting up migraphx-dev (2.11.0.60300-39~24.04) ...
#6 194.3 Setting up hipsparselt-dev (0.2.2.60300-39~24.04) ...
#6 194.3 Setting up hip-samples (6.3.42131.60300-39~24.04) ...
#6 194.3 Setting up rocm-ml-libraries (6.3.0.60300-39~24.04) ...
#6 194.3 Setting up rocm-hip-runtime-dev (6.3.0.60300-39~24.04) ...
#6 194.3 update-alternatives: using /opt/rocm-6.3.0/bin/roc-obj to provide /usr/bin/roc-obj (roc-obj) in auto mode
#6 194.3 update-alternatives: using /opt/rocm-6.3.0/bin/roc-obj-extract to provide /usr/bin/roc-obj-extract (roc-obj-extract) in auto mode
#6 194.3 update-alternatives: using /opt/rocm-6.3.0/bin/roc-obj-ls to provide /usr/bin/roc-obj-ls (roc-obj-ls) in auto mode
#6 194.3 update-alternatives: using /opt/rocm-6.3.0/bin/hipcc to provide /usr/bin/hipcc (hipcc) in auto mode
#6 194.3 update-alternatives: using /opt/rocm-6.3.0/bin/hipcc.pl to provide /usr/bin/hipcc.pl (hipcc.pl) in auto mode
#6 194.3 /opt/rocm-6.3.0/bin/hipcc.bin not found, but that is OK
#6 194.3 update-alternatives: using /opt/rocm-6.3.0/bin/hipcc_cmake_linker_helper to provide /usr/bin/hipcc_cmake_linker_helper (hipcc_cmake_linker_helper) in auto mode
#6 194.3 update-alternatives: using /opt/rocm-6.3.0/bin/hipconfig to provide /usr/bin/hipconfig (hipconfig) in auto mode
#6 194.3 update-alternatives: using /opt/rocm-6.3.0/bin/hipconfig.pl to provide /usr/bin/hipconfig.pl (hipconfig.pl) in auto mode
#6 194.3 /opt/rocm-6.3.0/bin/hipconfig.bin not found, but that is OK
#6 194.3 update-alternatives: using /opt/rocm-6.3.0/bin/hipconvertinplace-perl.sh to provide /usr/bin/hipconvertinplace-perl.sh (hipconvertinplace-perl.sh) in auto mode
#6 194.3 update-alternatives: using /opt/rocm-6.3.0/bin/hipconvertinplace.sh to provide /usr/bin/hipconvertinplace.sh (hipconvertinplace.sh) in auto mode
#6 194.3 update-alternatives: using /opt/rocm-6.3.0/bin/hipdemangleatp to provide /usr/bin/hipdemangleatp (hipdemangleatp) in auto mode
#6 194.4 update-alternatives: using /opt/rocm-6.3.0/bin/hipexamine-perl.sh to provide /usr/bin/hipexamine-perl.sh (hipexamine-perl.sh) in auto mode
#6 194.4 update-alternatives: using /opt/rocm-6.3.0/bin/hipexamine.sh to provide /usr/bin/hipexamine.sh (hipexamine.sh) in auto mode
#6 194.4 update-alternatives: using /opt/rocm-6.3.0/bin/hipify-perl to provide /usr/bin/hipify-perl (hipify-perl) in auto mode
#6 194.4 update-alternatives: using /opt/rocm-6.3.0/bin/hipify-clang to provide /usr/bin/hipify-clang (hipify-clang) in auto mode
#6 194.4 Setting up rocm-hip-sdk (6.3.0.60300-39~24.04) ...
#6 194.4 update-alternatives: using /opt/rocm-6.3.0/bin/hipfc to provide /usr/bin/hipfc (hipfc) in auto mode
#6 194.4 Setting up rpp-dev (1.9.1.60300-39~24.04) ...
#6 194.4 Setting up rocm-ml-sdk (6.3.0.60300-39~24.04) ...
#6 194.4 Setting up mivisionx-dev (3.1.0.60300-39~24.04) ...
#6 194.4 Setting up rocm (6.3.0.60300-39~24.04) ...
#6 194.4 update-alternatives: using /opt/rocm-6.3.0/bin/runvx to provide /usr/bin/runvx (runvx) in auto mode
#6 194.4 Processing triggers for libc-bin (2.39-0ubuntu8.4) ...
#6 194.4 Processing triggers for initramfs-tools (0.142ubuntu25.5) ...
#6 194.5 update-initramfs: Generating /boot/initrd.img-6.11.0-17-generic
#6 194.5 W: Kernel configuration /boot/config-6.11.0-17-generic is missing, cannot check for zstd compression support (CONFIG_RD_ZSTD)
#6 194.6 W: Can't find modules.builtin.modinfo (for locating built-in drivers' firmware, supported in Linux >=5.2)
#6 196.7 cat: /var/tmp/mkinitramfs_OjCM1s/lib/modules/6.11.0-17-generic/modules.builtin: No such file or directory
#6 196.7 depmod: WARNING: could not open modules.order at /var/tmp/mkinitramfs_OjCM1s/lib/modules/6.11.0-17-generic: No such file or directory
#6 196.7 depmod: WARNING: could not open modules.builtin at /var/tmp/mkinitramfs_OjCM1s/lib/modules/6.11.0-17-generic: No such file or directory
#6 196.7 depmod: WARNING: could not open modules.builtin.modinfo at /var/tmp/mkinitramfs_OjCM1s/lib/modules/6.11.0-17-generic: No such file or directory
#6 DONE 199.0s

#7 [4/5] RUN pip install --pre --no-cache-dir  --index-url https://download.pytorch.org/whl/nightly/rocm6.3/     'torch'     'torchaudio'     'torchvision' &&     pip install --pre --no-cache-dir lightning &&     fix-permissions "/opt/conda" &&     fix-permissions "/home/jovyan"
#7 0.517 Looking in indexes: https://download.pytorch.org/whl/nightly/rocm6.3/
#7 0.820 Collecting torch
#7 0.854   Downloading https://download.pytorch.org/whl/nightly/rocm6.3/torch-2.8.0.dev20250507%2Brocm6.3-cp312-cp312-manylinux_2_28_x86_64.whl (4569.0 MB)
#7 25.19      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.6/4.6 GB 223.3 MB/s eta 0:00:00
#7 28.79 Collecting torchaudio
#7 28.82   Downloading https://download.pytorch.org/whl/nightly/rocm6.3/torchaudio-2.6.0.dev20250507%2Brocm6.3-cp312-cp312-manylinux_2_28_x86_64.whl.metadata (7.2 kB)
#7 29.04 Collecting torchvision
#7 29.07   Downloading https://download.pytorch.org/whl/nightly/rocm6.3/torchvision-0.22.0.dev20250507%2Brocm6.3-cp312-cp312-manylinux_2_28_x86_64.whl.metadata (6.2 kB)
#7 29.19 Collecting filelock (from torch)
#7 29.23   Downloading https://download.pytorch.org/whl/nightly/filelock-3.16.1-py3-none-any.whl (16 kB)
#7 29.23 Requirement already satisfied: typing-extensions>=4.10.0 in /opt/conda/lib/python3.12/site-packages (from torch) (4.13.2)
#7 29.23 Requirement already satisfied: setuptools in /opt/conda/lib/python3.12/site-packages (from torch) (80.1.0)
#7 29.23 Requirement already satisfied: sympy>=1.13.3 in /opt/conda/lib/python3.12/site-packages (from torch) (1.14.0)
#7 29.23 Requirement already satisfied: networkx in /opt/conda/lib/python3.12/site-packages (from torch) (3.4.2)
#7 29.24 Requirement already satisfied: jinja2 in /opt/conda/lib/python3.12/site-packages (from torch) (3.1.6)
#7 29.24 Requirement already satisfied: fsspec in /opt/conda/lib/python3.12/site-packages (from torch) (2025.3.2)
#7 29.39 Collecting pytorch-triton-rocm==3.3.0+git96316ce5 (from torch)
#7 29.40   Downloading https://download.pytorch.org/whl/nightly/pytorch_triton_rocm-3.3.0%2Bgit96316ce5-cp312-cp312-linux_x86_64.whl.metadata (1.6 kB)
#7 29.41 Collecting torch
#7 29.44   Downloading https://download.pytorch.org/whl/nightly/rocm6.3/torch-2.8.0.dev20250502%2Brocm6.3-cp312-cp312-manylinux_2_28_x86_64.whl (4568.3 MB)
#7 39.11      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.6/4.6 GB 447.1 MB/s eta 0:00:00
#7 42.28 Requirement already satisfied: numpy in /opt/conda/lib/python3.12/site-packages (from torchvision) (2.2.5)
#7 42.28 Requirement already satisfied: pillow!=8.3.*,>=5.3.0 in /opt/conda/lib/python3.12/site-packages (from torchvision) (11.1.0)
#7 42.29 Requirement already satisfied: mpmath<1.4,>=1.1.0 in /opt/conda/lib/python3.12/site-packages (from sympy>=1.13.3->torch) (1.3.0)
#7 42.32 Requirement already satisfied: MarkupSafe>=2.0 in /opt/conda/lib/python3.12/site-packages (from jinja2->torch) (3.0.2)
#7 42.35 Downloading https://download.pytorch.org/whl/nightly/pytorch_triton_rocm-3.3.0%2Bgit96316ce5-cp312-cp312-linux_x86_64.whl (257.5 MB)
#7 42.81    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 257.5/257.5 MB 570.2 MB/s eta 0:00:00
#7 42.84 Downloading https://download.pytorch.org/whl/nightly/rocm6.3/torchaudio-2.6.0.dev20250507%2Brocm6.3-cp312-cp312-manylinux_2_28_x86_64.whl (1.8 MB)
#7 42.93    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.8/1.8 MB 22.4 MB/s eta 0:00:00
#7 42.97 Downloading https://download.pytorch.org/whl/nightly/rocm6.3/torchvision-0.22.0.dev20250507%2Brocm6.3-cp312-cp312-manylinux_2_28_x86_64.whl (3.1 MB)
#7 43.06    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.1/3.1 MB 31.0 MB/s eta 0:00:00
#7 43.57 Installing collected packages: pytorch-triton-rocm, filelock, torch, torchvision, torchaudio
#7 109.6 
#7 109.6 Successfully installed filelock-3.16.1 pytorch-triton-rocm-3.3.0+git96316ce5 torch-2.8.0.dev20250502+rocm6.3 torchaudio-2.6.0.dev20250507+rocm6.3 torchvision-0.22.0.dev20250507+rocm6.3
#7 112.0 Collecting lightning
#7 112.0   Downloading lightning-2.5.1.post0-py3-none-any.whl.metadata (39 kB)
#7 112.1 Requirement already satisfied: PyYAML<8.0,>=5.4 in /opt/conda/lib/python3.12/site-packages (from lightning) (6.0.2)
#7 112.1 Requirement already satisfied: fsspec<2026.0,>=2022.5.0 in /opt/conda/lib/python3.12/site-packages (from fsspec[http]<2026.0,>=2022.5.0->lightning) (2025.3.2)
#7 112.1 Collecting lightning-utilities<2.0,>=0.10.0 (from lightning)
#7 112.1   Downloading lightning_utilities-0.14.3-py3-none-any.whl.metadata (5.6 kB)
#7 112.1 Collecting packaging<25.0,>=20.0 (from lightning)
#7 112.1   Downloading packaging-24.2-py3-none-any.whl.metadata (3.2 kB)
#7 112.1 Requirement already satisfied: torch<4.0,>=2.1.0 in /opt/conda/lib/python3.12/site-packages (from lightning) (2.8.0.dev20250502+rocm6.3)
#7 112.2 Collecting torchmetrics<3.0,>=0.7.0 (from lightning)
#7 112.2   Downloading torchmetrics-1.7.1-py3-none-any.whl.metadata (21 kB)
#7 112.2 Requirement already satisfied: tqdm<6.0,>=4.57.0 in /opt/conda/lib/python3.12/site-packages (from lightning) (4.67.1)
#7 112.2 Requirement already satisfied: typing-extensions<6.0,>=4.4.0 in /opt/conda/lib/python3.12/site-packages (from lightning) (4.13.2)
#7 112.3 Collecting pytorch-lightning (from lightning)
#7 112.3   Downloading pytorch_lightning-2.5.1.post0-py3-none-any.whl.metadata (20 kB)
#7 112.6 Collecting aiohttp!=4.0.0a0,!=4.0.0a1 (from fsspec[http]<2026.0,>=2022.5.0->lightning)
#7 112.6   Downloading aiohttp-3.11.18-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (7.7 kB)
#7 112.6 Requirement already satisfied: setuptools in /opt/conda/lib/python3.12/site-packages (from lightning-utilities<2.0,>=0.10.0->lightning) (80.1.0)
#7 112.6 Requirement already satisfied: filelock in /opt/conda/lib/python3.12/site-packages (from torch<4.0,>=2.1.0->lightning) (3.16.1)
#7 112.6 Requirement already satisfied: sympy>=1.13.3 in /opt/conda/lib/python3.12/site-packages (from torch<4.0,>=2.1.0->lightning) (1.14.0)
#7 112.6 Requirement already satisfied: networkx in /opt/conda/lib/python3.12/site-packages (from torch<4.0,>=2.1.0->lightning) (3.4.2)
#7 112.6 Requirement already satisfied: jinja2 in /opt/conda/lib/python3.12/site-packages (from torch<4.0,>=2.1.0->lightning) (3.1.6)
#7 112.6 Requirement already satisfied: pytorch-triton-rocm==3.3.0+git96316ce5 in /opt/conda/lib/python3.12/site-packages (from torch<4.0,>=2.1.0->lightning) (3.3.0+git96316ce5)
#7 112.6 Requirement already satisfied: numpy>1.20.0 in /opt/conda/lib/python3.12/site-packages (from torchmetrics<3.0,>=0.7.0->lightning) (2.2.5)
#7 112.7 Collecting aiohappyeyeballs>=2.3.0 (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<2026.0,>=2022.5.0->lightning)
#7 112.7   Downloading aiohappyeyeballs-2.6.1-py3-none-any.whl.metadata (5.9 kB)
#7 112.7 Collecting aiosignal>=1.1.2 (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<2026.0,>=2022.5.0->lightning)
#7 112.7   Downloading aiosignal-1.3.2-py2.py3-none-any.whl.metadata (3.8 kB)
#7 112.7 Requirement already satisfied: attrs>=17.3.0 in /opt/conda/lib/python3.12/site-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<2026.0,>=2022.5.0->lightning) (25.3.0)
#7 112.8 Collecting frozenlist>=1.1.1 (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<2026.0,>=2022.5.0->lightning)
#7 112.8   Downloading frozenlist-1.6.0-cp312-cp312-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (16 kB)
#7 112.9 Collecting multidict<7.0,>=4.5 (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<2026.0,>=2022.5.0->lightning)
#7 113.0   Downloading multidict-6.4.3-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (5.3 kB)
#7 113.0 Collecting propcache>=0.2.0 (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<2026.0,>=2022.5.0->lightning)
#7 113.0   Downloading propcache-0.3.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (10 kB)
#7 113.2 Collecting yarl<2.0,>=1.17.0 (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<2026.0,>=2022.5.0->lightning)
#7 113.2   Downloading yarl-1.20.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (72 kB)
#7 113.2 Requirement already satisfied: idna>=2.0 in /opt/conda/lib/python3.12/site-packages (from yarl<2.0,>=1.17.0->aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<2026.0,>=2022.5.0->lightning) (3.10)
#7 113.2 Requirement already satisfied: mpmath<1.4,>=1.1.0 in /opt/conda/lib/python3.12/site-packages (from sympy>=1.13.3->torch<4.0,>=2.1.0->lightning) (1.3.0)
#7 113.2 Requirement already satisfied: MarkupSafe>=2.0 in /opt/conda/lib/python3.12/site-packages (from jinja2->torch<4.0,>=2.1.0->lightning) (3.0.2)
#7 113.3 Downloading lightning-2.5.1.post0-py3-none-any.whl (819 kB)
#7 113.3    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 819.0/819.0 kB 79.2 MB/s eta 0:00:00
#7 113.3 Downloading lightning_utilities-0.14.3-py3-none-any.whl (28 kB)
#7 113.3 Downloading packaging-24.2-py3-none-any.whl (65 kB)
#7 113.3 Downloading torchmetrics-1.7.1-py3-none-any.whl (961 kB)
#7 113.3    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 961.5/961.5 kB 460.5 MB/s eta 0:00:00
#7 113.3 Downloading aiohttp-3.11.18-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (1.7 MB)
#7 113.3    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.7/1.7 MB 263.5 MB/s eta 0:00:00
#7 113.3 Downloading multidict-6.4.3-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (223 kB)
#7 113.3 Downloading yarl-1.20.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (349 kB)
#7 113.3 Downloading aiohappyeyeballs-2.6.1-py3-none-any.whl (15 kB)
#7 113.4 Downloading aiosignal-1.3.2-py2.py3-none-any.whl (7.6 kB)
#7 113.4 Downloading frozenlist-1.6.0-cp312-cp312-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl (316 kB)
#7 113.4 Downloading propcache-0.3.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (245 kB)
#7 113.4 Downloading pytorch_lightning-2.5.1.post0-py3-none-any.whl (823 kB)
#7 113.4    ━━━━━━━━━━━━━━━��━━━━━━━━━━━━━━━━━━━━━━━ 823.1/823.1 kB 509.0 MB/s eta 0:00:00
#7 113.6 Installing collected packages: propcache, packaging, multidict, frozenlist, aiohappyeyeballs, yarl, lightning-utilities, aiosignal, torchmetrics, aiohttp, pytorch-lightning, lightning
#7 113.7   Attempting uninstall: packaging
#7 113.7     Found existing installation: packaging 25.0
#7 113.7     Uninstalling packaging-25.0:
#7 113.8       Successfully uninstalled packaging-25.0
#7 115.6 
#7 115.6 Successfully installed aiohappyeyeballs-2.6.1 aiohttp-3.11.18 aiosignal-1.3.2 frozenlist-1.6.0 lightning-2.5.1.post0 lightning-utilities-0.14.3 multidict-6.4.3 packaging-24.2 propcache-0.3.1 pytorch-lightning-2.5.1.post0 torchmetrics-1.7.1 yarl-1.20.0
#7 DONE 138.1s

#8 [5/5] RUN pip install --pre --no-cache-dir pyrsmi &&     pip install --pre --no-cache-dir git+https://github.com/mlflow/mlflow.git &&     fix-permissions "/opt/conda" &&     fix-permissions "/home/jovyan"
#8 0.595 Collecting pyrsmi
#8 0.626   Downloading pyrsmi-0.2.0-py2.py3-none-any.whl.metadata (5.7 kB)
#8 0.637 Downloading pyrsmi-0.2.0-py2.py3-none-any.whl (12 kB)
#8 0.896 Installing collected packages: pyrsmi
#8 0.922 Successfully installed pyrsmi-0.2.0
#8 1.347 Collecting git+https://github.com/mlflow/mlflow.git
#8 1.347   Cloning https://github.com/mlflow/mlflow.git to /tmp/pip-req-build-cj1wym1v
#8 1.350   Running command git clone --filter=blob:none --quiet https://github.com/mlflow/mlflow.git /tmp/pip-req-build-cj1wym1v
#8 18.16   Resolved https://github.com/mlflow/mlflow.git to commit 291f44c53d4c52f1e8a4601f00764fc09e64e0b9
#8 18.16   Running command git submodule update --init --recursive -q
#8 18.20   Installing build dependencies: started
#8 19.17   Installing build dependencies: finished with status 'done'
#8 19.18   Getting requirements to build wheel: started
#8 19.71   Getting requirements to build wheel: finished with status 'done'
#8 19.71   Preparing metadata (pyproject.toml): started
#8 20.02   Preparing metadata (pyproject.toml): finished with status 'done'
#8 20.11 Collecting Flask<4 (from mlflow==3.0.0.dev0)
#8 20.14   Downloading flask-3.1.0-py3-none-any.whl.metadata (2.7 kB)
#8 20.15 Requirement already satisfied: Jinja2<4,>=2.11 in /opt/conda/lib/python3.12/site-packages (from mlflow==3.0.0.dev0) (3.1.6)
#8 20.15 Requirement already satisfied: alembic!=1.10.0,<2 in /opt/conda/lib/python3.12/site-packages (from mlflow==3.0.0.dev0) (1.15.2)
#8 20.17 Collecting cachetools<6,>=5.0.0 (from mlflow==3.0.0.dev0)
#8 20.18   Downloading cachetools-5.5.2-py3-none-any.whl.metadata (5.4 kB)
#8 20.18 Requirement already satisfied: click<9,>=7.0 in /opt/conda/lib/python3.12/site-packages (from mlflow==3.0.0.dev0) (8.1.8)
#8 20.18 Requirement already satisfied: cloudpickle<4 in /opt/conda/lib/python3.12/site-packages (from mlflow==3.0.0.dev0) (3.1.1)
#8 20.21 Collecting databricks-sdk<1,>=0.20.0 (from mlflow==3.0.0.dev0)
#8 20.22   Downloading databricks_sdk-0.52.0-py3-none-any.whl.metadata (39 kB)
#8 20.25 Collecting docker<8,>=4.0.0 (from mlflow==3.0.0.dev0)
#8 20.25   Downloading docker-7.1.0-py3-none-any.whl.metadata (3.8 kB)
#8 20.32 Collecting fastapi<1 (from mlflow==3.0.0.dev0)
#8 20.33   Downloading fastapi-0.115.12-py3-none-any.whl.metadata (27 kB)
#8 20.33 Requirement already satisfied: gitpython<4,>=3.1.9 in /opt/conda/lib/python3.12/site-packages (from mlflow==3.0.0.dev0) (3.1.44)
#8 20.36 Collecting graphene<4 (from mlflow==3.0.0.dev0)
#8 20.36   Downloading graphene-3.4.3-py2.py3-none-any.whl.metadata (6.9 kB)
#8 20.38 Collecting gunicorn<24 (from mlflow==3.0.0.dev0)
#8 20.39   Downloading gunicorn-23.0.0-py3-none-any.whl.metadata (4.4 kB)
#8 20.39 Requirement already satisfied: importlib_metadata!=4.7.0,<9,>=3.7.0 in /opt/conda/lib/python3.12/site-packages (from mlflow==3.0.0.dev0) (8.6.1)
#8 20.41 Collecting markdown<4,>=3.3 (from mlflow==3.0.0.dev0)
#8 20.42   Downloading markdown-3.8-py3-none-any.whl.metadata (5.1 kB)
#8 20.42 Requirement already satisfied: matplotlib<4 in /opt/conda/lib/python3.12/site-packages (from mlflow==3.0.0.dev0) (3.10.1)
#8 20.42 Requirement already satisfied: numpy<3 in /opt/conda/lib/python3.12/site-packages (from mlflow==3.0.0.dev0) (2.2.5)
#8 20.44 Collecting opentelemetry-api<3,>=1.9.0 (from mlflow==3.0.0.dev0)
#8 20.45   Downloading opentelemetry_api-1.32.1-py3-none-any.whl.metadata (1.6 kB)
#8 20.47 Collecting opentelemetry-sdk<3,>=1.9.0 (from mlflow==3.0.0.dev0)
#8 20.48   Downloading opentelemetry_sdk-1.32.1-py3-none-any.whl.metadata (1.6 kB)
#8 20.48 Requirement already satisfied: packaging<26 in /opt/conda/lib/python3.12/site-packages (from mlflow==3.0.0.dev0) (24.2)
#8 20.48 Requirement already satisfied: pandas<3 in /opt/conda/lib/python3.12/site-packages (from mlflow==3.0.0.dev0) (2.2.3)
#8 20.48 Requirement already satisfied: protobuf<7,>=3.12.0 in /opt/conda/lib/python3.12/site-packages (from mlflow==3.0.0.dev0) (5.29.3)
#8 20.54 Collecting pyarrow<20,>=4.0.0 (from mlflow==3.0.0.dev0)
#8 20.55   Downloading pyarrow-19.0.1-cp312-cp312-manylinux_2_28_x86_64.whl.metadata (3.3 kB)
#8 20.55 Requirement already satisfied: pydantic<3,>=1.10.8 in /opt/conda/lib/python3.12/site-packages (from mlflow==3.0.0.dev0) (2.11.3)
#8 20.55 Requirement already satisfied: pyyaml<7,>=5.1 in /opt/conda/lib/python3.12/site-packages (from mlflow==3.0.0.dev0) (6.0.2)
#8 20.55 Requirement already satisfied: requests<3,>=2.17.3 in /opt/conda/lib/python3.12/site-packages (from mlflow==3.0.0.dev0) (2.32.3)
#8 20.55 Requirement already satisfied: scikit-learn<2 in /opt/conda/lib/python3.12/site-packages (from mlflow==3.0.0.dev0) (1.6.1)
#8 20.55 Requirement already satisfied: scipy<2 in /opt/conda/lib/python3.12/site-packages (from mlflow==3.0.0.dev0) (1.15.2)
#8 20.55 Requirement already satisfied: sqlalchemy<3,>=1.4.0 in /opt/conda/lib/python3.12/site-packages (from mlflow==3.0.0.dev0) (2.0.40)
#8 20.57 Collecting sqlparse<1,>=0.4.0 (from mlflow==3.0.0.dev0)
#8 20.58   Downloading sqlparse-0.5.3-py3-none-any.whl.metadata (3.9 kB)
#8 20.58 Requirement already satisfied: typing-extensions<5,>=4.0.0 in /opt/conda/lib/python3.12/site-packages (from mlflow==3.0.0.dev0) (4.13.2)
#8 20.60 Collecting uvicorn<1 (from mlflow==3.0.0.dev0)
#8 20.61   Downloading uvicorn-0.34.2-py3-none-any.whl.metadata (6.5 kB)
#8 20.61 Requirement already satisfied: Mako in /opt/conda/lib/python3.12/site-packages (from alembic!=1.10.0,<2->mlflow==3.0.0.dev0) (1.3.10)
#8 20.65 Collecting google-auth~=2.0 (from databricks-sdk<1,>=0.20.0->mlflow==3.0.0.dev0)
#8 20.66   Downloading google_auth-2.40.1-py2.py3-none-any.whl.metadata (6.2 kB)
#8 20.66 Requirement already satisfied: urllib3>=1.26.0 in /opt/conda/lib/python3.12/site-packages (from docker<8,>=4.0.0->mlflow==3.0.0.dev0) (2.4.0)
#8 20.69 Collecting starlette<0.47.0,>=0.40.0 (from fastapi<1->mlflow==3.0.0.dev0)
#8 20.69   Downloading starlette-0.46.2-py3-none-any.whl.metadata (6.2 kB)
#8 20.71 Collecting Werkzeug>=3.1 (from Flask<4->mlflow==3.0.0.dev0)
#8 20.72   Downloading werkzeug-3.1.3-py3-none-any.whl.metadata (3.7 kB)
#8 20.73 Collecting itsdangerous>=2.2 (from Flask<4->mlflow==3.0.0.dev0)
#8 20.74   Downloading itsdangerous-2.2.0-py3-none-any.whl.metadata (1.9 kB)
#8 20.74 Requirement already satisfied: blinker>=1.9 in /opt/conda/lib/python3.12/site-packages (from Flask<4->mlflow==3.0.0.dev0) (1.9.0)
#8 20.75 Requirement already satisfied: gitdb<5,>=4.0.1 in /opt/conda/lib/python3.12/site-packages (from gitpython<4,>=3.1.9->mlflow==3.0.0.dev0) (4.0.12)
#8 20.75 Requirement already satisfied: smmap<6,>=3.0.1 in /opt/conda/lib/python3.12/site-packages (from gitdb<5,>=4.0.1->gitpython<4,>=3.1.9->mlflow==3.0.0.dev0) (5.0.2)
#8 20.77 Collecting pyasn1-modules>=0.2.1 (from google-auth~=2.0->databricks-sdk<1,>=0.20.0->mlflow==3.0.0.dev0)
#8 20.78   Downloading pyasn1_modules-0.4.2-py3-none-any.whl.metadata (3.5 kB)
#8 20.79 Collecting rsa<5,>=3.1.4 (from google-auth~=2.0->databricks-sdk<1,>=0.20.0->mlflow==3.0.0.dev0)
#8 20.80   Downloading rsa-4.9.1-py3-none-any.whl.metadata (5.6 kB)
#8 20.82 Collecting graphql-core<3.3,>=3.1 (from graphene<4->mlflow==3.0.0.dev0)
#8 20.83   Downloading graphql_core-3.2.6-py3-none-any.whl.metadata (11 kB)
#8 20.84 Collecting graphql-relay<3.3,>=3.1 (from graphene<4->mlflow==3.0.0.dev0)
#8 20.85   Downloading graphql_relay-3.2.0-py3-none-any.whl.metadata (12 kB)
#8 20.85 Requirement already satisfied: python-dateutil<3,>=2.7.0 in /opt/conda/lib/python3.12/site-packages (from graphene<4->mlflow==3.0.0.dev0) (2.9.0.post0)
#8 20.86 Requirement already satisfied: zipp>=3.20 in /opt/conda/lib/python3.12/site-packages (from importlib_metadata!=4.7.0,<9,>=3.7.0->mlflow==3.0.0.dev0) (3.21.0)
#8 20.86 Requirement already satisfied: MarkupSafe>=2.0 in /opt/conda/lib/python3.12/site-packages (from Jinja2<4,>=2.11->mlflow==3.0.0.dev0) (3.0.2)
#8 20.86 Requirement already satisfied: contourpy>=1.0.1 in /opt/conda/lib/python3.12/site-packages (from matplotlib<4->mlflow==3.0.0.dev0) (1.3.2)
#8 20.86 Requirement already satisfied: cycler>=0.10 in /opt/conda/lib/python3.12/site-packages (from matplotlib<4->mlflow==3.0.0.dev0) (0.12.1)
#8 20.86 Requirement already satisfied: fonttools>=4.22.0 in /opt/conda/lib/python3.12/site-packages (from matplotlib<4->mlflow==3.0.0.dev0) (4.57.0)
#8 20.86 Requirement already satisfied: kiwisolver>=1.3.1 in /opt/conda/lib/python3.12/site-packages (from matplotlib<4->mlflow==3.0.0.dev0) (1.4.8)
#8 20.86 Requirement already satisfied: pillow>=8 in /opt/conda/lib/python3.12/site-packages (from matplotlib<4->mlflow==3.0.0.dev0) (11.1.0)
#8 20.86 Requirement already satisfied: pyparsing>=2.3.1 in /opt/conda/lib/python3.12/site-packages (from matplotlib<4->mlflow==3.0.0.dev0) (3.2.3)
#8 20.88 Collecting deprecated>=1.2.6 (from opentelemetry-api<3,>=1.9.0->mlflow==3.0.0.dev0)
#8 20.89   Downloading Deprecated-1.2.18-py2.py3-none-any.whl.metadata (5.7 kB)
#8 20.91 Collecting opentelemetry-semantic-conventions==0.53b1 (from opentelemetry-sdk<3,>=1.9.0->mlflow==3.0.0.dev0)
#8 20.92   Downloading opentelemetry_semantic_conventions-0.53b1-py3-none-any.whl.metadata (2.5 kB)
#8 20.92 Requirement already satisfied: pytz>=2020.1 in /opt/conda/lib/python3.12/site-packages (from pandas<3->mlflow==3.0.0.dev0) (2025.2)
#8 20.92 Requirement already satisfied: tzdata>=2022.7 in /opt/conda/lib/python3.12/site-packages (from pandas<3->mlflow==3.0.0.dev0) (2025.2)
#8 20.93 Requirement already satisfied: annotated-types>=0.6.0 in /opt/conda/lib/python3.12/site-packages (from pydantic<3,>=1.10.8->mlflow==3.0.0.dev0) (0.7.0)
#8 20.93 Requirement already satisfied: pydantic-core==2.33.1 in /opt/conda/lib/python3.12/site-packages (from pydantic<3,>=1.10.8->mlflow==3.0.0.dev0) (2.33.1)
#8 20.93 Requirement already satisfied: typing-inspection>=0.4.0 in /opt/conda/lib/python3.12/site-packages (from pydantic<3,>=1.10.8->mlflow==3.0.0.dev0) (0.4.0)
#8 20.94 Requirement already satisfied: six>=1.5 in /opt/conda/lib/python3.12/site-packages (from python-dateutil<3,>=2.7.0->graphene<4->mlflow==3.0.0.dev0) (1.17.0)
#8 20.94 Requirement already satisfied: charset_normalizer<4,>=2 in /opt/conda/lib/python3.12/site-packages (from requests<3,>=2.17.3->mlflow==3.0.0.dev0) (3.4.2)
#8 20.94 Requirement already satisfied: idna<4,>=2.5 in /opt/conda/lib/python3.12/site-packages (from requests<3,>=2.17.3->mlflow==3.0.0.dev0) (3.10)
#8 20.94 Requirement already satisfied: certifi>=2017.4.17 in /opt/conda/lib/python3.12/site-packages (from requests<3,>=2.17.3->mlflow==3.0.0.dev0) (2025.1.31)
#8 20.96 Collecting pyasn1>=0.1.3 (from rsa<5,>=3.1.4->google-auth~=2.0->databricks-sdk<1,>=0.20.0->mlflow==3.0.0.dev0)
#8 20.97   Downloading pyasn1-0.6.1-py3-none-any.whl.metadata (8.4 kB)
#8 20.97 Requirement already satisfied: joblib>=1.2.0 in /opt/conda/lib/python3.12/site-packages (from scikit-learn<2->mlflow==3.0.0.dev0) (1.5.0)
#8 20.97 Requirement already satisfied: threadpoolctl>=3.1.0 in /opt/conda/lib/python3.12/site-packages (from scikit-learn<2->mlflow==3.0.0.dev0) (3.6.0)
#8 20.98 Requirement already satisfied: greenlet>=1 in /opt/conda/lib/python3.12/site-packages (from sqlalchemy<3,>=1.4.0->mlflow==3.0.0.dev0) (3.2.1)
#8 20.99 Requirement already satisfied: anyio<5,>=3.6.2 in /opt/conda/lib/python3.12/site-packages (from starlette<0.47.0,>=0.40.0->fastapi<1->mlflow==3.0.0.dev0) (4.9.0)
#8 20.99 Requirement already satisfied: sniffio>=1.1 in /opt/conda/lib/python3.12/site-packages (from anyio<5,>=3.6.2->starlette<0.47.0,>=0.40.0->fastapi<1->mlflow==3.0.0.dev0) (1.3.1)
#8 20.99 Requirement already satisfied: h11>=0.8 in /opt/conda/lib/python3.12/site-packages (from uvicorn<1->mlflow==3.0.0.dev0) (0.16.0)
#8 21.07 Collecting wrapt<2,>=1.10 (from deprecated>=1.2.6->opentelemetry-api<3,>=1.9.0->mlflow==3.0.0.dev0)
#8 21.08   Downloading wrapt-1.17.2-cp312-cp312-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (6.4 kB)
#8 21.12 Downloading cachetools-5.5.2-py3-none-any.whl (10 kB)
#8 21.13 Downloading databricks_sdk-0.52.0-py3-none-any.whl (700 kB)
#8 21.15    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 700.2/700.2 kB 74.2 MB/s eta 0:00:00
#8 21.16 Downloading docker-7.1.0-py3-none-any.whl (147 kB)
#8 21.16 Downloading fastapi-0.115.12-py3-none-any.whl (95 kB)
#8 21.17 Downloading flask-3.1.0-py3-none-any.whl (102 kB)
#8 21.18 Downloading google_auth-2.40.1-py2.py3-none-any.whl (216 kB)
#8 21.19 Downloading graphene-3.4.3-py2.py3-none-any.whl (114 kB)
#8 21.20 Downloading graphql_core-3.2.6-py3-none-any.whl (203 kB)
#8 21.21 Downloading graphql_relay-3.2.0-py3-none-any.whl (16 kB)
#8 21.22 Downloading gunicorn-23.0.0-py3-none-any.whl (85 kB)
#8 21.22 Downloading markdown-3.8-py3-none-any.whl (106 kB)
#8 21.23 Downloading opentelemetry_api-1.32.1-py3-none-any.whl (65 kB)
#8 21.24 Downloading opentelemetry_sdk-1.32.1-py3-none-any.whl (118 kB)
#8 21.25 Downloading opentelemetry_semantic_conventions-0.53b1-py3-none-any.whl (188 kB)
#8 21.26 Downloading pyarrow-19.0.1-cp312-cp312-manylinux_2_28_x86_64.whl (42.1 MB)
#8 21.47    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 42.1/42.1 MB 202.5 MB/s eta 0:00:00
#8 21.48 Downloading rsa-4.9.1-py3-none-any.whl (34 kB)
#8 21.49 Downloading sqlparse-0.5.3-py3-none-any.whl (44 kB)
#8 21.49 Downloading starlette-0.46.2-py3-none-any.whl (72 kB)
#8 21.50 Downloading uvicorn-0.34.2-py3-none-any.whl (62 kB)
#8 21.51 Downloading Deprecated-1.2.18-py2.py3-none-any.whl (10.0 kB)
#8 21.52 Downloading wrapt-1.17.2-cp312-cp312-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl (89 kB)
#8 21.53 Downloading itsdangerous-2.2.0-py3-none-any.whl (16 kB)
#8 21.54 Downloading pyasn1-0.6.1-py3-none-any.whl (83 kB)
#8 21.55 Downloading pyasn1_modules-0.4.2-py3-none-any.whl (181 kB)
#8 21.56 Downloading werkzeug-3.1.3-py3-none-any.whl (224 kB)
#8 21.63 Building wheels for collected packages: mlflow
#8 21.63   Building wheel for mlflow (pyproject.toml): started
#8 23.15   Building wheel for mlflow (pyproject.toml): finished with status 'done'
#8 23.15   Created wheel for mlflow: filename=mlflow-3.0.0.dev0-py3-none-any.whl size=6265880 sha256=a0c97c79ea783a25270616934c043ba4c866836af244f5cedaa285612c1a378b
#8 23.15   Stored in directory: /tmp/pip-ephem-wheel-cache-d75xwi7h/wheels/c5/60/be/e77a7fe75b7fe2337825d798a03b67202eca3fd9a8da2f9437
#8 23.16 Successfully built mlflow
#8 23.44 Installing collected packages: wrapt, Werkzeug, uvicorn, sqlparse, pyasn1, pyarrow, markdown, itsdangerous, gunicorn, graphql-core, cachetools, starlette, rsa, pyasn1-modules, graphql-relay, Flask, docker, deprecated, opentelemetry-api, graphene, google-auth, fastapi, opentelemetry-semantic-conventions, databricks-sdk, opentelemetry-sdk, mlflow
#8 23.71   Attempting uninstall: pyarrow
#8 23.71     Found existing installation: pyarrow 20.0.0
#8 23.71     Uninstalling pyarrow-20.0.0:
#8 24.29       Successfully uninstalled pyarrow-20.0.0
#8 27.83 
#8 27.85 Successfully installed Flask-3.1.0 Werkzeug-3.1.3 cachetools-5.5.2 databricks-sdk-0.52.0 deprecated-1.2.18 docker-7.1.0 fastapi-0.115.12 google-auth-2.40.1 graphene-3.4.3 graphql-core-3.2.6 graphql-relay-3.2.0 gunicorn-23.0.0 itsdangerous-2.2.0 markdown-3.8 mlflow-3.0.0.dev0 opentelemetry-api-1.32.1 opentelemetry-sdk-1.32.1 opentelemetry-semantic-conventions-0.53b1 pyarrow-19.0.1 pyasn1-0.6.1 pyasn1-modules-0.4.2 rsa-4.9.1 sqlparse-0.5.3 starlette-0.46.2 uvicorn-0.34.2 wrapt-1.17.2
#8 DONE 31.2s

#9 exporting to image
#9 exporting layers
#9 exporting layers 111.2s done
#9 writing image sha256:8774017a0893cd6182f7584efc441da047e016df05d66f4eabe4deb649c95adc done
#9 naming to docker.io/library/jupyter-mlflow done
#9 DONE 111.2s




<Result cmd='docker build -t jupyter-mlflow -f style_transfer/docker/Dockerfile.jupyter-torch-mlflow-rocm .' exited=0>
```

</div>

Leave that cell running, and in the meantime，On the compute instance, install rclone:

Open an SSH sesson on your server. From your local terminal, run

```bash
ssh -i ~/.ssh/id_rsa_chameleon_35 cc@A.B.C.D
```

## Prepare data and training code

### Mount the object store to compute instance

Now that our data is safely inside the object store, we can use it anywhere - on a VM, on a bare metal site, on multiple compute instances at once, even outside of Chameleon - to train or evaluate a model. We would not have to repeat the ETL pipeline each time we want to use the data.

If working on a brand-new compute instance, we need to download `rclone` and create the rclone configuration file at `~/.config/rclone.conf`

Leave that cell running, and in the meantime, open an SSH sesson on your server. From your local terminal, run

```
ssh -i ~/.ssh/id_rsa_chameleon cc@A.B.C.D(change it to proper floating IP)
```

```bash
# run on node
curl https://rclone.org/install.sh | sudo bash
```

We also need to modify the configuration file for FUSE (Filesystem in USErspace: the interface that allows user space applications to mount virtual filesystems), so that object store containers mounted by our user will be availabe to others, including Docker containers:

```bash
# run on node
# this line makes sure user_allow_other is un-commented in /etc/fuse.conf
sudo sed -i '/^#user_allow_other/s/^#//' /etc/fuse.conf
```

Next, create a configuration file for rclone with the ID and secret from the application credential you just generated:

```bash
# run on node
mkdir -p ~/.config/rclone
nano  ~/.config/rclone/rclone.conf
```

Paste the following into the config file, but substitute your own application credential ID and secret.

You will also need to substitute your own user ID. You can find it using “Identity” > “Users” in the Horizon GUI; it is an alphanumeric string (not the human-readable user name).

```
[chi_tacc]
type = swift
user_id = YOUR_ID
application_credential_id = CREDENTIAL_ID
application_credential_secret = SECRET
auth = https://chi.tacc.chameleoncloud.org:5000/v3
region = CHI@TACC
```

Use Ctrl+O and Enter to save the file, and Ctrl+X to exit `nano`.

To test it, run

```bash
# run on node27829a1ac66f487aaf82cd92bfa047cf
rclone lsd chi_tacc:
```

and verify that you see your container listed. This confirms that rclone can authenticate to the object store.

mkdir -p ~/project35The next step is to create a mount point for the data in the local filesystem:

```bash
# run on node
mkdir -p ~/project35
```

Now finally, we can use rclone mount to mount the object store at the mount point (substituting your own netID in the command below).

```bash
# run on node
rclone mount chi_tacc:object-persist-project35 ~/project35 \--read-only --allow-other --daemon
```

Here,

`chi_tacc` tells rclone which section of its configuration file to use for authentication information
`object-persist-project35` tells it what object store container to mount
`~/project35` says where to mount it
Since we only intend to read the data, we can mount it in read-only mode and it will be slightly faster; and we are also protected from accidental writes. We also specified `--allow-other` so that we can use the mount from Docker, and `--daemon` means the rclone process will be started in the background.

(If need to umount,just do `umount ~/project35`)

Run

```bash
# run on node
ls project35/
```

and confirm that we can now see the img data directories.
our data directories would be:

```
project35/train
project35/val
project35/test
project35/random_inputs/random_train
project35/random_inputs/random_val
project35/random_inputs/random_test
```

### (Optional) (From local) check the working path

`ls`

`ls -l style_transfer`

`exit`

#### load the dataset to server

In local Terminal, run
`scp -i ~/.ssh/id_rsa_chameleon -r path/img-dataset cc@A.B.C.D:~/style_transfer/`

## Start the tracking server

The YAML configuration is at: docker/docker-compose-mlflow.yaml

From your local terminal, run

```bash
ssh -i ~/.ssh/id_rsa_chameleon cc@A.B.C.D
```

to ssh into the node.

### Start MLFlow tracking server system

Now we are ready to get it started. Bring up our MLFlow system with:

```bash
# run on node
docker compose -f style_transfer/docker/docker-compose-mlflow.yaml up -d
```

which will pull each container image, then start them.

When it is finished, the output of

```bash
# run on node
docker ps
```

should show that the `minio`, `postgres`, and `mlflow` containers are running.

### Access dashboards for the MLFlow tracking server system

Both MLFlow and MinIO include a browser-based dashboard. Let’s open these to make sure that we can find our way around them.

The MinIO dashboard runs on port 9001. In a browser, open

```
http://A.B.C.D:9001
```

Log in with the credentials we specified in the Docker Compose YAML:

- Username: `your-access-key`
- Password: `your-secret-key`

Then,

- Click on the “Buckets” section and note the `mlflow-artifacts` storage bucket that we created as part of the Docker Compose.
- Click on “Monitoring \> Metrics” and note the dashboard that shows the storage system health. MinIO works as a distributed object store with many advanced capabilities, although we are not using them; this dashboard lets operators keep an eye on system status.

Next, look at the MLFlow UI. This runs on port 8000. In a browser, open

```
http://A.B.C.D:8000
```

The UI shows a list of tracked “experiments”, and experiment “runs”. (A “run” corresponds to one instance of training a model; an “experiment” groups together related runs.) Since we have not yet used MLFlow, for now we will only see a “Default” experiment and no runs.

### Start a Jupyter server

Finally, start the Jupyter server container, inside which will run experiments that are tracked in MLFlow. Make sure the container image build, from the previous section, is now finished:

```bash
# run on node
docker image list
```

The command to run will depend on what type of GPU node you are using -

If you are using an AMD GPU (node type `gpu_mi100`), run

```bash
# run on node IF it is a gpu_mi100
HOST_IP=$(curl --silent http://169.254.169.254/latest/meta-data/public-ipv4 )
docker run  -d --rm  -p 8888:8888 \
    --device=/dev/kfd --device=/dev/dri \
    --group-add video --group-add $(getent group | grep render | cut -d':' -f 3) \
    --shm-size 16G \
    -v /home/cc/style_transfer:/home/jovyan/work \
    -e MLFLOW_TRACKING_URI=http://${HOST_IP}:8000/ \
    -e IMG_DATA_DIR=/home/jovyan/work/img-dataset \
    --name jupyter \
    jupyter-mlflow
```

Note that we intially get `HOST_IP`, the floating IP assigned to your instance, as a variable; then use it to specify the `MLFLOW_TRACKING_URI` inside the container. Training jobs inside the container will access the MLFlow tracking server using its public IP address.

Then, run

```
docker logs jupyter
```

and look for a line like

```
http://127.0.0.1:8888/lab?token=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

Paste this into a browser tab, but in place of `127.0.0.1`, substitute the floating IP assigned to the instance, to open the Jupyter notebook interface.

In the file browser on the left side, open the `work` directory.

Open a terminal (“File \> New \> Terminal”) inside the Jupyter server environment, and in this terminal, run

```bash
# runs on jupyter container inside node
env
```

to see environment variables. Confirm that the `MLFLOW_TRACKING_URI` is set, with the correct floating IP address.

### Run a non-MLFlow training job

Open a terminal inside this environment (“File \> New \> New Terminal”) and `cd` to the `work` directory. Our repository has already been cloned to the directory [vision-to-vintage](https://github.com/M0n4GPT/vision-to-vintage):

```bash
# run in a terminal inside jupyter container
cd ~/work
ls
```

In the `work` directory, open `train_style_transfer.py`, and view it directly there.

Then, run `train_style_transfer.py`:

```bash
# run in a terminal inside jupyter container
cd ~/work
python3 train_style_transfer.py \
    --data_root "$IMG_DATA_DIR" \
    --global_batch_size 32 \
    --micro_batch_size 8 \
    --epochs 5 \
    --precision fp32 \
    --strategy none \
    --export_path ./stylizer.pt
```

(note that the location of the dataset has been specified in an environment variable passed to the container.)

### Add MLFlow logging to Pytorch code

With the non MLFlow version it’s difficult to track, compare, version, and reproduce all of the experiments that you run with small changes. To address this, at the organization level, We set up a tracking server that all teams can use to track their experiments. Moving forward, the training scripts should log all the relevant details of each training run to MLFlow.

Switch to the `mlflow` branch of the training job, open the `train_style_transfer_mlflow.py`.

The `train_style_transfer_mlflow.py` script has already been augmented with MLFlow tracking code. Run the following to see a comparison betweeen the original and the modified training script.

```bash
# run in a terminal inside jupyter container, from the "work" directory
git diff --color-words train_style_transfer.py train_style_transfer_mlflow.py
```

(press `q` after you have finished reviewing this diff.)

The changes include:

**Add imports for MLFlow**:

```python
import mlflow
import mlflow.pytorch
```

MLFlow includes framework-specific modules for many machine learning frameworks, including [Pytorch](https://mlflow.org/docs/latest/python_api/mlflow.pytorch.html), [scikit-learn](https://mlflow.org/docs/latest/python_api/mlflow.sklearn.html), [Tensorflow](https://mlflow.org/docs/latest/python_api/mlflow.tensorflow.html), [HuggingFace/transformers](https://mlflow.org/docs/latest/python_api/mlflow.transformers.html), and many more. In this example, most of the functions we will use come from base `mlflow`, but we will use an `mlflow.pytorch`-specific function to save the Pytorch model.

**Configure MLFlow**:

The main configuration that is required for MLFlow tracking is to tell the MLFlow client where to send everything we are logging! By default, MLFlow assumes that you want to log to a local directory named `mlruns`. Since we want to log to a remote tracking server, you’ll have to override this default.

One way to specify the location of the tracking server would be with a call to `set_tracking_uri`, e.g.

```python
mlflow.set_tracking_uri("http://129.B.C.D:8000/")
```

In these experiments, we will instead specify the location of the tracking server with the `MLFLOW_TRACKING_URI` environment variable, which we have already passed to the container.

(A list of other environment variables that MLFLow uses is available in [its documentation](https://mlflow.org/docs/latest/python_api/mlflow.environment_variables.html). )

We also set the “experiment”. In MLFlow, an “experiment” is a group of related “runs”, e.g. different attempts to train the same type of model. If we don’t specify any experiment, then MLFlow logs to a “default” experiment; but we will specify that runs of this code should be organized inside the “food11-classifier” experiment.

```python
mlflow.set_experiment("style-trans")
```

**Start a run**:

In MLFlow, each time we train a model, we start a new run. Before we start training, we call

```python
mlflow.start_run()
```

or, we can put all the training inside a

```python
with mlflow.start_run():
    # ... do stuff
```

block. In this example, we actually start a run inside a

```python
try: 
    mlflow.end_run() # end pre-existing run, if there was one
except:
    pass
finally:
    mlflow.start_run()
```

block, since we are going to interrupt training runs with Ctrl+C, and without “gracefully” ending the run, we may not be able to start a new run.

**Track system metrics**:

Also, when we called `start_run`, we passed a `log_system_metrics=True` argument. This directs MLFlow to automatically start tracking and logging details of the host on which the experiment is running: CPU utilization and memory, GPU utilization and memory, etc.

Note that to automatically log GPU metrics, we must have installed `pyrsmi` (for AMD GPUs) or `pynvml` (for NVIDIA GPUs) - we installed these libraries inside the container image already. (But if we would build a new container image, we’d want to remember that.)

Besides for the details that are tracked automatically, we also decided to get the output of `rocm-smi` (for AMD GPUs) or `nvidia-smi` (for NVIDIA GPUs), and save the output as a text file in the tracking server. This type of logged item is called an artifact - unlike some of the other data that we track, which is more structured, an artifact can be any kind of file.

We used

```python
mlflow.log_text(gpu_info, "gpu-info.txt")
```

to save the contents of the `gpu_info` variable as a text file artifact named `gpu-info.txt`.

**Log hyperparameters**:

Of course, we will want to save all of the hyperparameters associated with our training run, so that we can go back later and identify optimal values. Since we have already saved all of our hyperparameters as a dictionary at the beginning, we can just call

```python
mlflow.log_params(config)
```

passing that entire dictionary. This practice of defining hyperparameters in one place (a dictionary, an external configuration file) rather than hard-coding them throughout the code, is less error-prone but also easier for tracking.

**Log metrics during training**:

Finally, the thing we most want to track: the metrics of our model during training! We use `mlflow.log_metrics` inside each training run:

```python
mlflow.log_metrics(
        {"epoch_time": t_e,
            "content_loss": l_c.item(),
            "style_loss": l_s.item(),
            "total_loss": loss.item(),
            }, step=e)
```

**Log model checkpoints**:

We additionally log a model checkpoint at the end of each epoch if the validation loss has improved:

```python
mlflow.log_artifact("./stylizer.pt", artifact_path="model")
```

The model *and* many details about it will be saved as an artifact in MLFlow.

and finally, we finish our run with

```python
mlflow.end_run()
```

## Experiment 1 Run Pytorch code with MLFlow logging

To test this code, open `train_style_transfer_mlflow.py` , change the `### Configure MLFlow mlflow.set_tracking_uri("http://129.114.C.D:8000/") ` into proper floating ip, then run

```bash
# run in a terminal inside jupyter container, from the "work/gourmetgram-train" directory
python3 train_style_transfer_mlflow.py \
    --data_root "$IMG_DATA_DIR" \
    --global_batch_size 32 \
    --micro_batch_size 8 \
    --epochs 5 \
    --precision fp32 \
    --strategy none \
    --export_path ./stylizer.pt
```

(Note that we already passed the `MLFLOW_TRACKING_URI` and `$IMG_DATA_DIR` to the container, so we do not need to specify this environment variable again when launching the training script.)

While this is running, in another tab in your browser, open the URL

```
http://A.B.C.D:8000/
```

where in place of `A.B.C.D`, substitute the floating IP address assigned to *your* instance. You will see the MLFlow browser-based interface. Now, in the list of experiments on the left side, you should see the new experiment. Click on it, and make sure you see your run listed. (It will be assigned a random name, since we did not specify the run name.)

Click on your run to see an overview. Note that in the “Details” field of the “Source” table. As the training script runs, you can see a “Parameters” table and a “Metrics” table on this page, populated with values logged from the experiment.

- Look at the “Parameters” table, and note that the hyperparameters in the `config` dictionary, which we logged with `log_params`, are all there.
- Look at the “Metrics” section, and note that (at least) the most recent value of each of the system metrics appear there. Once an epoch has passed, model metrics will also appear there.

Click on the “System metrics” tab for a visual display of the system metrics over time. In particular, look at the time series chart for the `gpu_0_utilization_percentage` metric, which logs the utilization of the first GPU over time. Wait until a few minutes of system metrics data has been logged. (use the “Refresh” button in the top right to update the display.)

## Experiment 2 speed up strategy, squeeze out more speed-ups:

change the `DataLoader` as follows, bumping up workers (and adding a couple more useful flags) to keep your GPUs fed:

```diff
-   loader = DataLoader(
-       ds,
-       batch_size=args.micro_batch_size,
-       sampler=sampler,
-       shuffle=not distributed,
-       num_workers=4,
-       pin_memory=True
-   )

+   loader = DataLoader(
+       ds,
+       batch_size=args.micro_batch_size,
+       sampler=sampler,
+       shuffle=not distributed,
+       num_workers=16,                # ↑ more parallelism
+       pin_memory=True,               # keep this on
+       prefetch_factor=2,             # number of batches to prefetch per worker
+   )
```

Now, run the training script again with

```bash
# run in a terminal inside the jupyter container, from inside the "work/" directory
python3 train_style_transfer_mlflow.py \
    --data_root "$IMG_DATA_DIR" \
    --global_batch_size 32 \
    --micro_batch_size 8 \
    --epochs 5 \
    --precision fp32 \
    --strategy none \
    --export_path ./stylizer.pt
```

In the MLFlow interface, find this new run, and open its overview. Write a note to yourself, to remind yourself later what the objective behind this experiment was; click on the pencil icon next to “Description” and then put text in the input field.

Note the difference between these training runs in:

- the utilization of GPU 0 (logged as `gpu_0_utilization_percentage`, under system metrics)
- and the time per epoch (logged as `epoch_time`, under model metrics)

# Large-scale model training

## Training strategies for large models

### Experiment 3: Baseline

As a baseline, let's try an epoch of training style transfer model, using full precision and a batch size of 128:

```bash
# run in a terminal inside the jupyter container, from inside the "work/" directory
python3 train_style_transfer_mlflow.py \
    --data_root "$IMG_DATA_DIR" \
    --global_batch_size 128 \
    --micro_batch_size 128 \
    --epochs 5 \
    --precision fp32 \
    --strategy none \
    --export_path ./stylizer.pt
```

This is using about 15.30GB GPU memoryfor each epoch.

### Experiment 4: Reduced batch size

But with a smaller batch size, it fits easily:
Make a note of the training time and memory.

```bash
# run in a terminal inside the jupyter container, from inside the "work/" directory
python3 train_style_transfer_mlflow.py \
    --data_root "$IMG_DATA_DIR" \
    --global_batch_size 32 \
    --micro_batch_size 32 \
    --epochs 5 \
    --precision fp32 \
    --strategy none \
    --export_path ./stylizer.pt
```

### Experiment 5: Gradient accumulation

By using gradient accumulation to "step" only after a few "micro batches", we can train with a larger effective "global" batch size, with minimal effect on the memory required:

```bash
# run in a terminal inside the jupyter container, from inside the "work/" directory
python3 train_style_transfer_mlflow.py \
    --data_root "$IMG_DATA_DIR" \
    --global_batch_size 128 \
    --micro_batch_size 32 \
    --epochs 5 \
    --precision fp32 \
    --strategy none \
    --export_path ./stylizer.pt
```

### Experiment 6: Mixed precision

With mixed precision, we get back some of the lost precision in the results, at the cost of some additional memory and time:

```bash
# run in a terminal inside the jupyter container, from inside the "work/" directory
python3 train_style_transfer_mlflow.py \
    --data_root "$IMG_DATA_DIR" \
    --global_batch_size 128 \
    --micro_batch_size 32 \
    --epochs 5 \
    --precision amp \
    --strategy none \
    --export_path ./stylizer.pt
```

## Use distributed training to increase velocity (Train a large model on multiple GPUs - 2x gpu_mi100)

### Confirm ROCm-built PyTorch & RCCL support

```bash
# run in a terminal inside the jupyter container, from inside the "work/" directory
python3 - << 'EOF'
import torch
print("Build backend:", torch.version.hip or torch.version.cuda)
print("NCCL/RCCL available:", torch.distributed.is_nccl_available())
print("CUDA/ROCm available:", torch.cuda.is_available(),
      "Device count:", torch.cuda.device_count())
EOF
```

should see the output:

```
Build backend: 6.3.42131-fa1d09cbd
NCCL/RCCL available: True
CUDA/ROCm available: True Device count: 2
```

### Verify ROCm tools

```bash
# run in a terminal inside the jupyter container, from inside the "work/" directory
which rocm-smi && rocm-smi --showid
```

You should see GPU info, proving ROCm user-space tools are installed. See the output:

```
============================ ROCm System Management Interface ============================
=========================================== ID ===========================================
GPU[0]          : Device Name:          Arcturus GL-XL [Instinct MI100]
GPU[0]          : Device ID:            0x738c
GPU[0]          : Device Rev:           0x01
GPU[0]          : Subsystem ID:         0x0c34
GPU[0]          : GUID:                 51219
GPU[1]          : Device Name:          Arcturus GL-XL [Instinct MI100]
GPU[1]          : Device ID:            0x738c
GPU[1]          : Device Rev:           0x01
GPU[1]          : Subsystem ID:         0x0c34
GPU[1]          : GUID:                 45163
==========================================================================================
================================== End of ROCm SMI Log ===================================
```

### Experiment 7: train model on 2x gpu_mi100 with DDP

After all the check above, we are ready to run strategies for training a large model using distributed processes across multiple GPUs

```bash
# run in a terminal inside the jupyter container, from inside the "work/" directory

python -m torch.distributed.launch \                                                                                                   --nproc_per_node=2 train_style_transfer_muti.py \
      --data_root "$IMG_DATA_DIR" \
      --global_batch_size 128 \
      --micro_batch_size 32 \
      --epochs 5 \
      --precision amp \
      --strategy ddp \
      --export_path ./stylizer_ddp.pt
```

### Experiment 8: train model on 2x gpu_mi100 with FSDP

With DDP, we have a larger effective batch size (since 2 GPUs process a batch in parallel), but no memory savings. With FSDP, we can shard optimizer state, gradients, and parameters across GPUs, to also reduce the memory required.

```bash
# run in a terminal inside the jupyter container, from inside the "work/" directory

python -m torch.distributed.launch \
      --nproc_per_node=2 train_style_transfer_muti.py \
  --data_root "$IMG_DATA_DIR" \
  --global_batch_size 128 \
  --micro_batch_size 32 \
  --epochs 5 \
  --precision amp \
  --strategy fsdp \
  --export_path ./stylizer_fsdp.pt
```

note:

Why there's only a tiny GPU‐memory win when you switch to FSDP:

Activations matter more: During training, intermediate feature maps (activations) typically consume far more GPU memory than the model weights, and FSDP does not shard those by default.

Frozen encoder bug: Early on, I froze the VGG-19 encoder (set `requires_grad=False`) and then wrapped the entire model in FSDP with `use_orig_params=False`, causing a “uniform requires_grad” error. To unblock that, you black-listed the encoder so FSDP only sharded the CNN decoder.

Encoder dominates the parameters: VGG-19 accounts for ~143 M of ~145 M parameters, while the decoder has much small parameter size. By ignoring the encoder, you left ~572 MB of weights fully replicated on each GPU and only shard a samll part.

### Experiment 9: train model on 2x gpu_mi100 with FSDP (modified)

Change your FSDP wrap to:

```python
from torch.distributed.fsdp import FullyShardedDataParallel as FSDP
from torch.distributed.fsdp import CPUOffload, ShardingStrategy

# … including the diff

if args.strategy == 'fsdp':
    model = FSDP(
        model,
        cpu_offload=CPUOffload(False),
        sharding_strategy=ShardingStrategy.FULL_SHARD,
        flatten_parameters=False,   # DO NOT collapse into one flat buffer
        use_orig_params=True,       # keep each nn.Parameter intact
        # ignored_modules={enc},   # do not shard the frozen encoder
    )
```

With these two flags:
Each Conv2d.weight stays a 4-D tensor, so conv2d calls work correctly.
All weights (including your frozen encoder!) get individually sharded across GPUs, so you still get the parameter-memory benefit.

```bash
# run in a terminal inside the jupyter container, from inside the "work/" directory

python -m torch.distributed.launch \
      --nproc_per_node=2 train_style_transfer_fsdp.py \
  --data_root "$IMG_DATA_DIR" \
  --global_batch_size 128 \
  --micro_batch_size 32 \
  --epochs 5 \
  --precision amp \
  --strategy fsdp \
  --export_path ./stylizer_fsdp_modi.pt
```


