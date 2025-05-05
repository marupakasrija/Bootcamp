# Bootcamp Setup Task: ex-tools-1

Demonstrates how to set up an Ubuntu Virtual Machine on Azure and deploy a basic web server using NGINX.

## 🌐 Live Demo
[Click here to view](http://20.78.1.73)

## 📝 Project Overview
This project showcases the deployment of a simple web page on an Azure Virtual Machine running Ubuntu 24.04 with the NGINX web server.

## ✅ Setup Steps

### 1. Creating an Ubuntu Virtual Machine on Azure
- Created a VM through the Azure portal.
- Selected **Ubuntu 24.04** as the operating system.
- Configured the VM with a **public IP address** for browser access.
- Generated an **SSH key pair** for secure access.

### 2. SSH Connection to the VM
Connected to the VM via SSH using the private key generated during VM creation:

```bash
ssh -i "webserver_key.pem" azureuser@20.78.1.73
```

### 3. Installing the NGINX Web Server
After connecting to the VM, installed NGINX to serve static content:

```bash
sudo apt update
sudo apt install nginx -y
```

### 4. Deploying a Custom HTML Page
Replaced the default NGINX web page with a custom HTML page:

```bash
sudo nano /var/www/html/index.html
```

### 5. Verifying Server Accessibility
- Confirmed NGINX was running properly.
- Accessed the public IP [20.78.1.73](http://20.78.1.73) in a browser.
- Successfully loaded the custom HTML page.

## 💻 Complete Command Reference

```bash
# SSH into the VM using the private key
ssh -i "webserver_key.pem" azureuser@20.78.1.73

# Update package lists
sudo apt update

# Install NGINX
sudo apt install nginx -y

# Edit the default HTML page
sudo nano /var/www/html/index.html

# Check NGINX service status
sudo systemctl status nginx
```


## 📸 Screenshots
*Add screenshots of your Azure portal, VM dashboard, terminal, and deployed website here.*
![Editing bootcamp_ex-tools-1_readme md at master · marupakasrija_bootcamp - Google Chrome 03-05-2025 22_14_39](https://github.com/user-attachments/assets/d3d7c670-8ace-4ddc-adea-29c65ae80a74)

![Welcome - M Srija Reddy - Google Chrome 03-05-2025 20_50_45](https://github.com/user-attachments/assets/bc85df22-9b2b-4748-bb78-38c66d95b121)
