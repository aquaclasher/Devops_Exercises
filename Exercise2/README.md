# Exercise 2: Flask on Minikube

This exercise packages a Flask application into a Docker image, deploys one replica to Minikube, and exposes it with a Kubernetes `NodePort` Service.

## Prerequisites

- Docker Desktop running
- Minikube profile running
- kubectl

## Run on Windows PowerShell

```powershell
minikube start --driver=docker
docker build -t flask-app:latest .
minikube image load flask-app:latest
kubectl apply -f flask-deployment.yaml
kubectl rollout status deployment/flask-app
minikube service flask-app-service --url
```

Open the URL returned by the final command. It should respond with:

```text
Hello from Flask on Kubernetes!
```

## Verify

```powershell
kubectl get deployments
kubectl get pods -l app=flask-app
kubectl get services
kubectl logs deployment/flask-app
```

## How it works

`app.py` listens on container port `15000`. The Service selects Pods labelled `app: flask-app`, accepts traffic on service port `15000`, and forwards it to the same container `targetPort`.

`imagePullPolicy: Never` makes Kubernetes use only the locally loaded `flask-app:latest` image. That is why `minikube image load` is required after building with Docker Desktop.

## Clean up

```powershell
kubectl delete -f flask-deployment.yaml
```
