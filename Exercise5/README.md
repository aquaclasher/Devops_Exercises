# Exercise 5: Docker Security with AppArmor and Python

## Objective
Understand how to secure Docker containers using Linux AppArmor profiles and the Docker SDK for Python. Implement and apply an AppArmor security profile that confines a Flask web application, restricting access to sensitive system paths (e.g., `/etc/`) and blocking unauthorized binary executions (e.g., `/bin/bash`).

## Prerequisites
- Linux host or virtual machine with AppArmor enabled (`sudo aa-status`)
- Docker installed and running
- Python 3 with `pip`
- `apparmor-utils` installed:
  ```bash
  sudo apt-get update
  sudo apt-get install -y apparmor-utils
  ```

## Implementation Files
- `app.py`: Flask web application running on port 5000.
- `Dockerfile`: Container image specification based on `python:3.8-slim`.
- `my-apparmor-profile`: AppArmor security profile defining directory restrictions, network allowances, and binary execution blocks.
- `apply_apparmor.py`: Python automation script using Docker SDK to build the image, run the container with the security profile, inspect `HostConfig.SecurityOpt`, and stop the container.
- `test_restricted_actions.py`: Python script verifying security confinement by attempting restricted actions (`cat /etc/passwd` and executing `/bin/bash`).
- `requirements.txt`: Python dependencies (`flask`, `docker`).

## Steps to Execute

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Build the Container Image
```bash
docker build -t flask-apparmor .
```

### Step 3: Load the AppArmor Profile
Copy the profile to the system AppArmor directory and load it into the Linux kernel:
```bash
sudo cp my-apparmor-profile /etc/apparmor.d/my-apparmor-profile
sudo apparmor_parser -r /etc/apparmor.d/my-apparmor-profile
```

Verify that the profile is active:
```bash
sudo aa-status | grep my-apparmor-profile
```

### Step 4: Run Container with AppArmor Profile (Docker CLI)
```bash
docker run -d --name flask-secure --security-opt="apparmor=my-apparmor-profile" -p 5000:5000 flask-apparmor
```
Verify the endpoint responds:
```bash
curl http://127.0.0.1:5000/
docker stop flask-secure && docker rm flask-secure
```

### Step 5: Apply and Verify AppArmor via Docker SDK
Run the automated script to build, deploy, and inspect the security configuration:
```bash
python3 apply_apparmor.py
```
**Expected Output:**
```text
Building image from Dockerfile...
Running container with AppArmor profile...
Container started: <container_id>
Inspecting container to verify AppArmor profile...
AppArmor profile applied: ['apparmor=my-apparmor-profile']
Stopping container...
```

### Step 6: Test Restricted Actions
Run the verification test script:
```bash
python3 test_restricted_actions.py
```
**Expected Output:**
```text
Container started: <container_id>
Attempt to read /etc/passwd: Exit Code 1, Output: cat: /etc/passwd: Permission denied
Attempt to execute /bin/bash: Exit Code 126, Output:
Container stopped
```
- **Exit Code 1 on `/etc/passwd`**: Confirms read access to `/etc/**` is blocked by AppArmor policy.
- **Exit Code 126 on `/bin/bash`**: Confirms shell binary execution is blocked by AppArmor policy.

---

## Questions & Answers

**Q1: What is the purpose of using AppArmor with Docker containers?**  
**A1:** AppArmor provides Mandatory Access Control (MAC) to enforce security confinement on containerized processes, restricting their access to system files, capabilities, network resources, and binaries even if the container is breached or running as root.

**Q2: How do AppArmor profiles help secure a Docker container?**  
**A2:** Profiles define explicit whitelists and blacklists for file paths, network operations, raw capabilities, and execution permissions. This limits the blast radius of any exploit to only the explicitly allowed operations.

**Q3: Why is it important to restrict access to sensitive directories such as `/etc/` and `/var/`?**  
**A3:** Directories like `/etc/` contain critical authentication data, system credentials, and configuration files, while `/var/` holds logs and runtime data. Restricting access prevents attackers from exfiltrating credentials or tampering with system state.

**Q4: What other capabilities can you restrict using AppArmor profiles?**  
**A4:** AppArmor can restrict network sockets (raw, inet, packet), binding to privileged ports, POSIX capabilities (e.g., `CAP_SYS_ADMIN`, `CAP_NET_ADMIN`), inter-process communication (IPC), and execution of specific shells/interpreters.

**Q5: How can you verify if an AppArmor profile is successfully applied to a Docker container?**  
**A5:** By inspecting the container using `docker inspect <container>` or via the Docker SDK (`container.attrs['HostConfig']['SecurityOpt']`), which lists the active `apparmor=<profile_name>` assignment.
