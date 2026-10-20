# Exercise 1: Kubernetes Getting Started (Hello Pod)

## Objective
Deploy an Nginx web server application as a Pod on a local Kubernetes cluster using Minikube and expose it via a NodePort Service for browser access.

## Prerequisites
- Docker Desktop
- Minikube
- kubectl CLI

## Implementation Files
- `pod.yaml`: Kubernetes Pod manifest running the `nginx` container on port 80.
- `service.yaml`: Kubernetes Service manifest of type `NodePort` exposing the `hello-k8s` Pod.

## Steps to Execute

1. **Start Minikube**:
   ```bash
   minikube start --driver=docker
   ```

2. **Deploy the Pod and Service**:
   ```bash
   kubectl apply -f pod.yaml
   kubectl apply -f service.yaml
   ```

3. **Verify Deployment**:
   ```bash
   kubectl get pods
   kubectl get services
   ```

4. **Access the Application**:
   ```bash
   minikube service hello-k8s
   ```
   This opens the default browser displaying the "Welcome to nginx!" welcome page.

## Clean Up
```bash
kubectl delete -f service.yaml
kubectl delete -f pod.yaml
```
