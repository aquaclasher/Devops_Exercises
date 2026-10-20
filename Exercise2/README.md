# Exercise 2: Deploy a Flask App on Minikube Using kubectl and YAML

## Objective
Set up a single-node Kubernetes cluster using Minikube, containerize a Python Flask application, deploy it with Kubernetes manifests, and expose it via a NodePort Service.

## Prerequisites
- Docker Desktop
- Minikube
- kubectl CLI

## Implementation Files
- `app.py`: Simple Flask web application listening on `0.0.0.0:15000`.
- `requirements.txt`: Python package dependencies (`Flask`).
- `Dockerfile`: Container image specification based on `python:3.8-slim`.
- `flask-deployment.yaml`: Combined manifest containing the Kubernetes `Deployment` (1 replica, `imagePullPolicy: Never`) and `Service` (`type: NodePort`, mapping port 15000 to targetPort 15000).

## Steps to Execute

1. **Start Minikube**:
   ```bash
   minikube start --driver=docker
   ```

2. **Build and Load the Docker Image**:
   ```bash
   docker build -t flask-app:latest .
   minikube image load flask-app:latest
   ```

3. **Deploy the Application**:
   ```bash
   kubectl apply -f flask-deployment.yaml
   ```

4. **Verify Deployment & Pods**:
   ```bash
   kubectl get deployments
   kubectl get pods -l app=flask-app
   kubectl get services
   kubectl logs deployment/flask-app
   ```

5. **Access the Service**:
   ```bash
   minikube service flask-app-service --url
   ```
   Open the returned URL in your browser or make a request using `curl`:
   ```bash
   curl <service-url>
   ```
   Expected response: `Hello from Flask on Kubernetes!`

## Clean Up
```bash
kubectl delete -f flask-deployment.yaml
```

---

## Questions & Answers

**Q1: What is the purpose of `minikube service flask-app-service --url`?**  
**A1:** To provide the URL for accessing the `flask-app-service` running inside Minikube.

**Q2: What happens when you run `minikube service flask-app-service --url`?**  
**A2:** Minikube checks if the service is running, generates an accessible host tunnel/URL, and displays it in the terminal.

**Q3: Why is `targetPort` used in Kubernetes Service configuration?**  
**A3:** To specify the port number on which the container application is listening.

**Q4: What is the difference between `port` and `targetPort` in Kubernetes Service configuration?**  
**A4:** `port` is the exposed port of the Kubernetes Service, while `targetPort` is the container port where traffic is forwarded.

**Q5: How do you access a Flask application running in Minikube?**  
**A5:** Use `minikube service <service-name> --url` to obtain the access URL.

**Q6: Why does the terminal need to remain open when using the Docker driver on Linux/Windows with Minikube?**  
**A6:** Because the Docker driver maintains an active tunnel process between host and the Minikube network.

**Q7: What is the benefit of using the `--url` flag with the `minikube service` command?**  
**A7:** It outputs the reachable HTTP URL directly without automatically opening a browser window.

**Q8: What command is used to expose a service in Kubernetes?**  
**A8:** `kubectl expose` or `kubectl apply -f <service.yaml>` is used to expose a service in Kubernetes.

**Q9: How does Minikube help in local Kubernetes testing?**  
**A9:** Minikube provisions a local single-node Kubernetes cluster, allowing testing and development of manifests without a full production cloud cluster.

**Q10: What is the role of `kubectl` in this setup?**  
**A10:** `kubectl` is the Kubernetes CLI used to interact with the cluster API to deploy applications, inspect status, view logs, and manage resources.
