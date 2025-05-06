# Object Store Setup (CHI@TACC)

This document outlines the steps followed to set up object storage on Chameleon Cloud (CHI@TACC) for the Vision-to-Vintage project. The object store will persist our artwork dataset for training and evaluation.

---

## ✅ Step-by-Step Procedure

### 1. Access Horizon GUI for CHI@TACC
- Go to [chameleoncloud.org](https://www.chameleoncloud.org)
- Navigate to: **Experiment** → **CHI@TACC**
- Log in if prompted
- Ensure the correct project is selected (check the top-left drop-down)

### 2. Create Object Store Container
- On the left menu: **Object Store** → **Containers** → **Create Container**
- Name: `object-persist-[your-netid]` (e.g., `object-persist-sk1234`)
- Leave other settings as default
- Click **Submit**

### 3. Create Application Credential
- Go to: **Identity** → **Application Credentials**
- Click **Create Application Credential**
  - Name: `data-persist`
  - Expiration: End of semester (UTC)
- Save the **Application Credential ID** and **Secret**
- Also **Download the OpenRC file** for backup

---

### 4. Install rclone on Compute Instance
SSH into your compute instance (e.g., `node-persist-[netid]`) and run:

```bash
curl https://rclone.org/install.sh | sudo bash
```

### 5. Enable User Access for FUSE
Ensure `user_allow_other` is enabled in `/etc/fuse.conf`:

```bash
sudo sed -i '/^#user_allow_other/s/^#//' /etc/fuse.conf
```

---

### 6. Configure rclone
Run:

```bash
mkdir -p ~/.config/rclone
nano ~/.config/rclone/rclone.conf
```

Paste the following template (replace values):

```ini
[chi_tacc]
type = swift
user_id = YOUR_USER_ID
application_credential_id = APP_CRED_ID
application_credential_secret = APP_CRED_SECRET
auth = https://chi.tacc.chameleoncloud.org:5000/v3
region = CHI@TACC
```

- `user_id`: Found via Horizon → Identity → Users → your user ID (not username)
- Save with Ctrl+O and exit with Ctrl+X

---

### 7. Test rclone Authentication

```bash
rclone lsd chi_tacc:
```

If your container (e.g., `object-persist-sk1234`) is listed, authentication was successful ✅

---

### ⏳ Next Steps
- Upload the `artwork_dataset.zip` to this object store
- Mount the object store as a filesystem in the compute instance
- Use this persistent data for model training and evaluation
