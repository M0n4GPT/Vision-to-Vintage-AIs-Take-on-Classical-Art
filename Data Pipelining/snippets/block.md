::: {.cell .markdown}

## Utilizing Block Storage for Persistent Data Management

we leverage block storage volumes on Chameleon Cloud, which offer persistent storage independent of any single compute instance. This approach allows us to:
* Create a block storage volume at KVM@TACC
* Attach it to a compute instance
* Format and mount it with a filesystem
* Utilize it as a Docker volume for containerized applications
* Detach and reattach it to new instances as needed

By integrating block storage into our workflow, we ensure that critical data remains intact across sessions, facilitating a more robust and flexible research environment.
:::

::: {.cell .markdown}

### Block storage using the Horizon GUI

First, let's try creating a block storage volume from the OpenStack Horizon GUI. Open the GUI for KVM@TACC:

* from the [Chameleon website](https://chameleoncloud.org/hardware/)
* click "Experiment" > "KVM@TACC"
* log in if prompted to do so
* check the project drop-down menu near the top left (which shows e.g. "CHI-XXXXXX"), and make sure the correct project is selected.

In the menu sidebar on the left side, click on "Volumes" > "Volumes" and then, "Create Volume". You will be prompted to set up your volume step by step using a graphical "wizard".

* Specify the name as <code>block-persist-<b>project35</b></code>
* Specify the size as 5 GiB.
* Leave other settings at their defaults, and click "Create Volume".

Next, it's time to to attach the block storage volume to the compute instance we created earlier. From  "Volumes" > "Volumes", next to *your* volume, click the ▼ in the menu on the right and choose "Manage Attachments". In the "Attach to Instance" menu, choose your compute instance. Then, click "Attach Volume".

Now, the "Volumes" overview page in the Horizon GUI should show something like for your volume:

```
| Name                | Description | Size | Status | Group | Type     | Attached To                     | Availability Zone | Bootable | Encrypted |
|---------------------|-------------|------|--------|-------|----------|---------------------------------|-------------------|----------|-----------|
| block-persist-project35 | -           | 5GiB | In-use | -     | ceph-ssd | /dev/vdb on node-persist-netID  | nova              | No       | No        |
```

On the instance, let's confirm that we can see the block storage volume. Run

```bash
lsblk
```

and verify that `vdb` appears in the output.

The volume is essentially a raw disk. Before we can use it **for the first time** after creating it, we need to partition the disk, create a filesystem on the partition, and mount it. In subsequent uses, we will only need to mount it.

> **Note**: if the volume already had data on it, creating a filesystem on it would erase all its data! This procedure is *only* for the initial setup of a volume, before it has any data on it.

First, we create a partition with an `ext4` filesystem, occupying the entire volume:

```bash
sudo parted -s /dev/vdb mklabel gpt
sudo parted -s /dev/vdb mkpart primary ext4 0% 100%
```

Verify that we now have the partition `vdb1` in the output of 

```bash
lsblk
```

Next, we format the partition:

```bash
sudo mkfs.ext4 /dev/vdb1
```

Finally, we can create a directory in the local filesystem, mount the partition to that directory:

```bash
sudo mkdir -p /mnt/block
sudo mount /dev/vdb1 /mnt/block
```

and change the owner of that directory to the `cc` user:

```bash
sudo chown -R cc /mnt/block
sudo chgrp -R cc /mnt/block
```

Run

```bash
df -h
```

and verify that the output includes a line with `/dev/vdb1` mounted on `/mnt/block`:

```
Filesystem      Size  Used Avail Use% Mounted on
/dev/vdb1       2.0G   24K  1.9G   1% /mnt/block
```

:::


::: {.cell .markdown}


