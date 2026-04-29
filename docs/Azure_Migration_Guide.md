# EduBoost SA — Azure Migration Guide (Dev/Test)

This guide outlines the process of moving your development testing environment from WSL to an Azure VM to alleviate local resource constraints.

## 🏗 Architecture Overview

- **Local (WSL)**: Code development and Git commits.
- **Git (GitHub)**: Source of truth.
- **Azure (VM)**: High-performance environment for running Docker, ML models, and integration tests.

---

## 🚀 Step 1: Provision Azure Infrastructure

You can deploy the pre-configured Dev Box using the provided Bicep template.

1. **Install Azure CLI**: `curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash`
2. **Login**: `az login`
3. **Deploy Infrastructure**:
   ```bash
   # Create a resource group
   az group create --name EduBoost-Dev-RG --location southafricanorth

   # Deploy the VM (replace <password> with a strong one)
   az deployment group create \
     --resource-group EduBoost-Dev-RG \
     --template-file bicep/azure_dev_box.bicep \
     --parameters adminPasswordOrKey='<password>'
   ```
4. **Get Public IP**: The deployment output will show `publicIP`. Save this.

---

## 🛠 Step 2: Configure the Azure VM

Once the VM is running, SSH into it and install the Docker stack.

1. **SSH into VM**: `ssh eduboost@<public-ip>`
2. **Install Docker & Compose**:
   ```bash
   sudo apt-get update
   sudo apt-get install -y docker.io docker-compose
   sudo usermod -aG docker $USER
   # Log out and log back in for group changes to take effect
   ```

---

## 🔄 Step 3: Development Workflow

Maintain your development in WSL, but run tests in Azure.

1. **Local (WSL)**: Make changes and push to Git.
   ```bash
   git add .
   git commit -m "feat: your new feature"
   git push origin main
   ```

2. **Remote (Azure)**: Pull changes and rebuild.
   ```bash
   ssh eduboost@<public-ip>
   
   # Clone the repo (first time only)
   git clone https://github.com/<your-username>/edo-boost-main.git
   cd edo-boost-main

   # Pull and Run
   git pull origin main
   docker-compose up -d --build
   ```

---

## 🧹 Step 4: Cost Management

To save costs when not testing:
- **Stop the VM**: `az vm deallocate --resource-group EduBoost-Dev-RG --name eduboost-dev-box`
- **Start the VM**: `az vm start --resource-group EduBoost-Dev-RG --name eduboost-dev-box`

*Note: You only pay for storage while the VM is deallocated.*
